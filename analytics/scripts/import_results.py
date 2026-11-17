"""Import and anonymize Gophish Results/Raw Events exports."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from analytics_core import normalize_campaign, normalize_quiz_summary, read_csv, slugify  # noqa: E402

def main() -> int:
    parser = argparse.ArgumentParser(description="Nhập CSV Gophish và chuẩn hóa dữ liệu PhishLab.")
    parser.add_argument("--results", required=True, help="Gophish Results CSV.")
    parser.add_argument("--events", help="Gophish Raw Events CSV (khuyến nghị).")
    parser.add_argument("--quiz-summary", help="CSV tổng hợp quiz: participants_started, completed_count, average_score.")
    parser.add_argument("--campaign-name", default="PhishLab Campaign")
    parser.add_argument("--scenario", default="Chưa phân loại", help="IT, Delivery, HR hoặc tên kịch bản khác.")
    parser.add_argument("--output-dir", default="analytics/data/processed")
    args = parser.parse_args()

    recipients, events, warnings = normalize_campaign(
        read_csv(args.results), read_csv(args.events) if args.events else None,
        args.campaign_name, args.scenario
    )
    quiz = normalize_quiz_summary(read_csv(args.quiz_summary)) if args.quiz_summary else None
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    prefix = slugify(args.campaign_name)
    recipients.to_csv(out / f"{prefix}_recipients_raw.csv", index=False, encoding="utf-8-sig")
    events.to_csv(out / f"{prefix}_events_raw.csv", index=False, encoding="utf-8-sig")
    if quiz is not None:
        (out / f"{prefix}_quiz_summary.json").write_text(json.dumps(quiz, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {
        "campaign_name": args.campaign_name, "scenario": args.scenario,
        "recipient_count": len(recipients), "event_count": len(events),
        "quiz_summary": quiz, "warnings": warnings,
        "privacy": "Emails are used in memory only for joining and are not exported. Raw Events details are ignored."
    }
    (out / f"{prefix}_import.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Da nhap {len(recipients)} nguoi nhan, {len(events)} su kien.")
    print(f"Du lieu da an danh: {out}")
    for warning in warnings:
        print(f"CANH BAO: {warning}")
    if quiz is None:
        print("CANH BAO: Chua co Quiz summary; dashboard se de trong Training Completion va diem quiz.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
