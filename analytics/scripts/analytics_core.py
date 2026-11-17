"""Shared, privacy-conscious data processing for PhishLab Analytics."""
from __future__ import annotations
import io
import re
from pathlib import Path
from typing import Any
import pandas as pd

RECIPIENT_COLUMNS = [
    "campaign_name", "scenario", "recipient_code", "status",
    "email_sent", "email_opened", "link_clicked", "email_reported",
]
EVENT_COLUMNS = ["campaign_name", "recipient_code", "event_time", "event_type"]
TRUE_VALUES = {"1", "true", "yes", "y", "on", "completed", "reported"}

def _clean_header(value: Any) -> str:
    text = str(value).replace("\ufeff", "").strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")

def read_csv(source: Any) -> pd.DataFrame:
    """Read a CSV path or bytes with UTF-8 BOM and common Windows fallback."""
    if isinstance(source, (bytes, bytearray)):
        source = io.BytesIO(source)
    try:
        frame = pd.read_csv(source, encoding="utf-8-sig", sep=None, engine="python")
    except UnicodeDecodeError:
        if hasattr(source, "seek"):
            source.seek(0)
        frame = pd.read_csv(source, encoding="cp1252", sep=None, engine="python")
    if frame.empty and len(frame.columns) == 0:
        raise ValueError("CSV không có tiêu đề cột.")
    frame.columns = [_clean_header(c) for c in frame.columns]
    return frame

def _find_column(frame: pd.DataFrame, *names: str) -> str | None:
    for name in names:
        key = _clean_header(name)
        if key in frame.columns:
            return key
    return None

def _text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()

def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if pd.isna(value):
        return False
    return str(value).strip().lower() in TRUE_VALUES

def normalize_event_type(value: Any) -> str:
    text = _text(value).lower().replace("_", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    mapping = {
        "sent": "Email Sent", "email sent": "Email Sent",
        "opened": "Email Opened", "email opened": "Email Opened",
        "clicked": "Clicked Link", "clicked link": "Clicked Link", "link clicked": "Clicked Link",
        "email reported": "Email Reported", "reported email": "Email Reported",
    }
    return mapping.get(text, _text(value)[:80])

def _status_flags(status: str) -> dict[str, bool]:
    value = status.strip().lower()
    return {
        "sent": value in {"email sent", "email opened", "clicked link", "email reported"},
        "opened": value == "email opened",
        "clicked": value == "clicked link",
        "reported": value == "email reported",
    }

def _make_codes(ids: pd.Series | None, count: int) -> list[str]:
    codes = []
    for i in range(count):
        value = _text(ids.iloc[i]) if ids is not None else ""
        codes.append(value if value and value.lower() not in {"nan", "none"} else f"R{i+1:04d}")
    seen, result = {}, []
    for code in codes:
        seen[code] = seen.get(code, 0) + 1
        result.append(code if seen[code] == 1 else f"{code}-{seen[code]}")
    return result

def normalize_campaign(
    results: pd.DataFrame,
    events: pd.DataFrame | None = None,
    campaign_name: str = "PhishLab Campaign",
    scenario: str = "Chưa phân loại",
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Normalize Gophish Results and optional Raw Events, dropping personal fields."""
    if results.empty:
        raise ValueError("Results CSV không có bản ghi người nhận.")
    email_col = _find_column(results, "email", "email_address")
    id_col = _find_column(results, "id", "recipient_code", "user_id")
    status_col = _find_column(results, "status", "result_status")
    reported_col = _find_column(results, "reported", "email_reported")
    if email_col is None and id_col is None:
        raise ValueError("Không tìm thấy cột email hoặc id trong Results CSV.")
    if status_col is None and (events is None or events.empty):
        raise ValueError("Không tìm thấy cột status; hãy cung cấp status hoặc Raw Events.")
    codes = _make_codes(results[id_col] if id_col else None, len(results))
    email_to_code = {}
    if email_col:
        for i, email in enumerate(results[email_col].tolist()):
            key = _text(email).casefold()
            if key:
                email_to_code[key] = codes[i]

    event_flags: dict[str, set[str]] = {code: set() for code in codes}
    event_rows: list[dict[str, str]] = []
    warnings: list[str] = []
    if events is not None and not events.empty:
        e_email = _find_column(events, "email", "email_address")
        e_id = _find_column(events, "id", "recipient_code", "user_id")
        e_time = _find_column(events, "time", "timestamp", "event_time", "date")
        e_type = _find_column(events, "message", "event", "event_type", "action")
        if e_type is None:
            warnings.append("Raw Events không có cột message/event; bỏ qua sự kiện.")
        elif e_email is None and e_id is None:
            warnings.append("Raw Events không có cột email/id để ghép người nhận.")
        else:
            for _, row in events.iterrows():
                code = ""
                if e_email:
                    code = email_to_code.get(_text(row.get(e_email, "")).casefold(), "")
                if not code and e_id:
                    candidate = _text(row.get(e_id, ""))
                    if candidate in event_flags:
                        code = candidate
                event_type = normalize_event_type(row.get(e_type, ""))
                if not code or not event_type:
                    continue
                event_flags.setdefault(code, set()).add(event_type)
                event_rows.append({
                    "campaign_name": campaign_name,
                    "recipient_code": code,
                    "event_time": _text(row.get(e_time, "")) if e_time else "",
                    "event_type": event_type,
                })

    rows = []
    for i, (_, row) in enumerate(results.iterrows()):
        code = codes[i]
        status = _text(row.get(status_col, "")) if status_col else ""
        fallback = _status_flags(status)
        flags = event_flags.get(code, set())
        rows.append({
            "campaign_name": campaign_name,
            "scenario": scenario,
            "recipient_code": code,
            "status": status,
            "email_sent": ("Email Sent" in flags) or fallback["sent"],
            "email_opened": ("Email Opened" in flags) or fallback["opened"],
            "link_clicked": ("Clicked Link" in flags) or fallback["clicked"],
            "email_reported": ("Email Reported" in flags) or fallback["reported"] or (to_bool(row.get(reported_col)) if reported_col else False),
        })
    recipients = pd.DataFrame(rows, columns=RECIPIENT_COLUMNS)
    event_frame = pd.DataFrame(event_rows, columns=EVENT_COLUMNS)
    if events is None or events.empty:
        warnings.append("Chưa có Raw Events CSV: chỉ số mở/nhấp/báo cáo được suy ra từ status cuối trong Results và có thể thiếu lịch sử sự kiện.")
    return recipients, event_frame, warnings

def normalize_quiz_summary(frame: pd.DataFrame) -> dict[str, Any]:
    """Accept aggregate quiz totals only; never join quiz answers to recipient identities."""
    if frame.empty:
        raise ValueError("Quiz summary CSV không có dữ liệu.")
    started_col = _find_column(frame, "participants_started", "training_started", "started_count")
    completed_col = _find_column(frame, "completed_count", "training_completed", "participants_completed")
    average_col = _find_column(frame, "average_score", "avg_score", "quiz_average", "average_quiz_score")
    if started_col is None or completed_col is None:
        raise ValueError("Quiz summary cần participants_started và completed_count.")
    row = frame.iloc[0]
    started = pd.to_numeric(row[started_col], errors="coerce")
    completed = pd.to_numeric(row[completed_col], errors="coerce")
    if pd.isna(started) or pd.isna(completed) or started < 0 or completed < 0 or completed > started:
        raise ValueError("Số người bắt đầu/hoàn thành quiz không hợp lệ.")
    average = pd.to_numeric(row[average_col], errors="coerce") if average_col else pd.NA
    if pd.notna(average) and not 0 <= float(average) <= 100:
        raise ValueError("average_score phải từ 0 đến 100.")
    return {
        "participants_started": int(started),
        "completed_count": int(completed),
        "average_score": float(average) if pd.notna(average) else None,
    }

def calculate_metrics(frame: pd.DataFrame, quiz_summary: dict[str, Any] | None = None) -> dict[str, Any]:
    total = int(len(frame))
    sent = int(frame["email_sent"].map(to_bool).sum()) if total else 0
    opened = int(frame["email_opened"].map(to_bool).sum()) if total else 0
    clicked = int(frame["link_clicked"].map(to_bool).sum()) if total else 0
    reported = int(frame["email_reported"].map(to_bool).sum()) if total else 0
    def rate(n: int, d: int) -> float | None:
        return round(n / d * 100, 2) if d else None
    started = quiz_summary["participants_started"] if quiz_summary else None
    completed = quiz_summary["completed_count"] if quiz_summary else None
    average = quiz_summary["average_score"] if quiz_summary else None
    return {
        "total_recipients": total, "emails_sent": sent, "emails_opened": opened,
        "links_clicked": clicked, "emails_reported": reported,
        "training_started": started, "training_started_proxy": clicked if quiz_summary is None else None,
        "training_completed": completed, "average_quiz_score": round(average, 2) if average is not None else None,
        "send_rate": rate(sent, total), "open_rate": rate(opened, sent),
        "click_rate": rate(clicked, sent), "report_rate": rate(reported, sent),
        "training_completion_rate": rate(completed, started) if quiz_summary else None,
    }

def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip()).strip("_").lower()
    return value or "campaign"

def discover_clean_campaigns(directory: str | Path) -> list[Path]:
    path = Path(directory)
    return sorted(path.glob("*_recipients_clean.csv")) if path.exists() else []
