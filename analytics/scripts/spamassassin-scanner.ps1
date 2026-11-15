
param(
    [string]$Recipient = "",
    [string]$MailHogApi = "http://localhost:8025/api/v1/messages",
    [string]$ContainerName = "spamassassin-lab",
    [int]$PollIntervalSeconds = 5,
    [switch]$Once
)

$ErrorActionPreference = "Stop"

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

$DataDirectory = Join-Path $ProjectRoot "analytics\data"
$OutputDirectory = Join-Path $ProjectRoot "analytics\output"

# Recipient filter simulation configuration
$ProfileFile = Join-Path $PSScriptRoot "recipient-filter-profiles.ps1"

if (-not (Test-Path $ProfileFile)) {
    throw "Recipient filter profile file not found: $ProfileFile"
}

. $ProfileFile

if ($null -eq $RecipientProfiles -or $RecipientProfiles.Count -eq 0) {
    throw "RecipientProfiles configuration is empty."
}

# Use separate files to preserve previous scan history
$ProcessedFile = Join-Path $DataDirectory "processed-mailhog-recipient-profiles-ids.txt"
$ReportFile = Join-Path $OutputDirectory "spamassassin-recipient-filter-results.csv"

New-Item -ItemType Directory -Force -Path $DataDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

# --------------------------------------------------
# 2. Initialize processed message IDs
# --------------------------------------------------

$ProcessedIds = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)

if (Test-Path $ProcessedFile) {
    Get-Content $ProcessedFile | ForEach-Object {
        $ids = $_ -split '\s+'

        foreach ($id in $ids) {
            if (-not [string]::IsNullOrWhiteSpace($id)) {
                [void]$ProcessedIds.Add($id.Trim())
            }
        }
    }
}

# --------------------------------------------------
# 3. Helper: get email header
# --------------------------------------------------

function Get-EmailHeader {
    param(
        [object]$Message,
        [string]$HeaderName
    )

    $headers = $Message.Content.Headers

    if ($null -ne $headers) {
        $property = $headers.PSObject.Properties[$HeaderName]

        if ($null -ne $property) {
            return (@($property.Value) -join " ")
        }
    }

    return ""
}

# --------------------------------------------------
# 4. Helper: scan one email
# --------------------------------------------------

function Invoke-SpamAssassinScan {
    param(
        [object]$Message
    )

    $messageId = [string]$Message.ID

    if ([string]::IsNullOrWhiteSpace($messageId)) {
        Write-Warning "Message has no ID. Skipping."
        return $false
    }

    $tempName = "phishlab-$([guid]::NewGuid().ToString('N')).eml"
    $localFile = Join-Path $env:TEMP $tempName
    $containerFile = "/tmp/$tempName"

    try {
        # Save raw email without UTF-8 BOM
        $rawEmail = [string]$Message.Raw.Data

        if ([string]::IsNullOrWhiteSpace($rawEmail)) {
            throw "Email raw data is empty."
        }

        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)

        [System.IO.File]::WriteAllText(
            $localFile,
            $rawEmail,
            $utf8NoBom
        )

        # Copy email into SpamAssassin container
        & docker cp $localFile "${ContainerName}:$containerFile"

        $copyExitCode = $LASTEXITCODE

        if ($copyExitCode -ne 0) {
            throw "docker cp failed with exit code $copyExitCode"
        }

        # Scan email using spamc
        $scanLines = & docker exec $ContainerName bash -lc "spamc -R < '$containerFile'" 2>&1

        $scanExitCode = $LASTEXITCODE
        $scanOutput = ($scanLines | Out-String).Trim()

        if ($scanExitCode -ne 0) {
            throw "SpamAssassin scan failed: $scanOutput"
        }

        # Extract score and required score
        $scoreMatch = [regex]::Match(
            $scanOutput,
            '([-+]?\d+(?:\.\d+)?)/([-+]?\d+(?:\.\d+)?)'
        )

        if (-not $scoreMatch.Success) {
            throw "Could not extract SpamAssassin score. Output: $scanOutput"
        }

        $score = [double]::Parse(
            $scoreMatch.Groups[1].Value,
            [Globalization.CultureInfo]::InvariantCulture
        )

        $requiredScore = [double]::Parse(
            $scoreMatch.Groups[2].Value,
            [Globalization.CultureInfo]::InvariantCulture
        )

        

        # Extract triggered rules when available
        $ruleLines = @(
            $scanOutput -split "`r?`n" |
            Where-Object {
                $_ -match '^\s*[-+]?\d+(?:\.\d+)?\s+[A-Z][A-Z0-9_]+\s+'
            }
        )

        $rules = $ruleLines -join "; "

        
        # --------------------------------------------------
        # Build one result for each recipient
        # --------------------------------------------------

        $recipients = @(
            foreach ($address in @($Message.Raw.To)) {
                $emailMatches = [regex]::Matches(
                    [string]$address,
                    '(?i)[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}'
                )

                foreach ($emailMatch in $emailMatches) {
                    $emailMatch.Value.ToLowerInvariant()
                }
            }
        ) | Sort-Object -Unique

        if ($recipients.Count -eq 0) {
            throw "No valid recipient address found."
        }

        $records = @()

        foreach ($recipientAddress in $recipients) {

            # Only process PhishLab recipients
            if ($recipientAddress -notmatch '@phishlab\.test$') {
                continue
            }

            if (-not [string]::IsNullOrWhiteSpace($Recipient) -and
                $recipientAddress -ne $Recipient.ToLowerInvariant()) {
                continue
            }

            # Get recipient-specific filter profile
            if (-not $RecipientProfiles.ContainsKey($recipientAddress)) {
                Write-Warning "No filter profile found for $recipientAddress. Skipping."
                continue
            }

            $recipientProfile = $RecipientProfiles[$recipientAddress]
            $profileThreshold = [double]$recipientProfile.RequiredScore

            # Classify using the recipient-specific threshold
            if ($score -ge $profileThreshold) {
                $classification = "SPAM"
            }
            else {
                $classification = "NOT_SPAM"
            }

            # Build recipient-specific report record
            $record = [PSCustomObject]@{
                MessageId                 = $messageId
                ReceivedAt                = [string]$Message.Created
                Recipient                 = $recipientAddress
                Sender                    = [string]$Message.Raw.From
                Subject                   = Get-EmailHeader -Message $Message -HeaderName "Subject"
                SpamScore                 = $score
                SpamAssassinRequiredScore = $requiredScore
                RequiredScore             = $profileThreshold
                FilterProfile             = [string]$recipientProfile.Profile
                Classification            = $classification
                Rules                     = $rules
                ScannedAt                 = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            }

            $records += $record
        }

        if ($records.Count -eq 0) {
            throw "No recipient matched a configured filter profile."
        }

        # --------------------------------------------------
        # Export recipient-specific results
        # --------------------------------------------------

        if (Test-Path $ReportFile) {
            $records | Export-Csv -Path $ReportFile `
                -NoTypeInformation -Append -Encoding UTF8
        }
        else {
            $records | Export-Csv -Path $ReportFile `
                -NoTypeInformation -Encoding UTF8
        }

        # Mark processed only after successful report export
        Add-Content -Path $ProcessedFile -Value $messageId -Encoding UTF8
        [void]$ProcessedIds.Add($messageId)

        # --------------------------------------------------
        # Display results
        # --------------------------------------------------

        foreach ($record in $records) {

            $color = if ($record.Classification -eq "SPAM") {
                "Red"
            }
            else {
                "Green"
            }

            Write-Host ""
            Write-Host "Recipient: $($record.Recipient)" -ForegroundColor Cyan
            Write-Host "Filter: $($record.FilterProfile)"
            Write-Host "SpamScore: $($record.SpamScore)"
            Write-Host "RequiredScore: $($record.RequiredScore)"
            Write-Host "Classification: $($record.Classification)" -ForegroundColor $color
        }

        Write-Host ""
        Write-Host "Message scanned successfully: $messageId" -ForegroundColor Cyan

        return $true
    }
    catch {
        Write-Warning "Failed to scan message $messageId : $_"
        return $false
    }
    finally {
        # Remove temporary files
        if (Test-Path $localFile) {
            Remove-Item $localFile -Force -ErrorAction SilentlyContinue
        }

        & docker exec $ContainerName rm -f $containerFile 2>$null | Out-Null
    }
}

# --------------------------------------------------
# 5. Main polling loop
# --------------------------------------------------

Write-Host "========================================"
Write-Host "       PHISHLAB SPAMASSASSIN SCANNER"
Write-Host "========================================"
Write-Host "Recipient : $Recipient"
Write-Host "MailHog   : $MailHogApi"
Write-Host "Container : $ContainerName"
Write-Host "Report    : $ReportFile"
Write-Host ""

do {
    try {
        $messages = Invoke-RestMethod `
            -Uri $MailHogApi `
            -Method Get `
            -TimeoutSec 15

        # Normalize the API response into a flat array of messages.
        $messages = @($messages)

        $targetMessages = @(
            $messages |
            Where-Object {
                $addresses = @($_.Raw.To)

                if ([string]::IsNullOrWhiteSpace($Recipient)) {
                    $internalRecipients = @(
                        $addresses |
                        Where-Object {
                            $_ -match '@phishlab\.test$'
                        }
                    )

                    $internalRecipients.Count -gt 0
                }
                else {
                    $addresses -contains $Recipient
                }
            } |
            Sort-Object Created
        )

        foreach ($message in $targetMessages) {
            $messageId = [string]$message.ID

            if ([string]::IsNullOrWhiteSpace($messageId)) {
                continue
            }

            if ($ProcessedIds.Contains($messageId)) {
                continue
            }

            [void](Invoke-SpamAssassinScan -Message $message)
        }
    }
    catch {
        Write-Warning "MailHog polling error: $_"
    }

    if (-not $Once) {
        Start-Sleep -Seconds $PollIntervalSeconds
    }

} while (-not $Once)

Write-Host ""
Write-Host "Scanner stopped."
