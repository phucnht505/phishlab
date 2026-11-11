
$RecipientProfiles = @{
    "demo01@phishlab.test" = @{
        Profile = "Very Strict"
        RequiredScore = 2.0
    }

    "demo02@phishlab.test" = @{
        Profile = "Strict"
        RequiredScore = 3.0
    }

    "demo03@phishlab.test" = @{
        Profile = "Strict Plus"
        RequiredScore = 4.0
    }

    "demo04@phishlab.test" = @{
        Profile = "Moderate"
        RequiredScore = 4.5
    }

    "demo05@phishlab.test" = @{
        Profile = "Standard"
        RequiredScore = 5.0
    }

    "demo06@phishlab.test" = @{
        Profile = "Standard Plus"
        RequiredScore = 5.5
    }

    "demo07@phishlab.test" = @{
        Profile = "Relaxed"
        RequiredScore = 6.0
    }

    "demo08@phishlab.test" = @{
        Profile = "Lenient"
        RequiredScore = 7.0
    }

    "demo09@phishlab.test" = @{
        Profile = "Very Lenient"
        RequiredScore = 8.0
    }

    "demo10@phishlab.test" = @{
        Profile = "Minimal"
        RequiredScore = 10.0
    }
}
