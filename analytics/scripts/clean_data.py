"""Validate and deduplicate anonymized campaign data."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from analytics_core import RECIPIENT_COLUMNS, to_bool

BOOLS = ["email_sent", "email_opened", "link_clicked", "email_reported"]

def clean_file(source: Path, destination: Path) -> dict[str, int]:
    df = pd.read_csv(source, encoding="utf-8-sig")
    missing = [c for c in RECIPIENT_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Thieu cot: {', '.join(missing)}")
    before = len(df)
    df = df[RECIPIENT_COLUMNS].copy()
    df["recipient_code"] = df["recipient_code"].fillna("").astype(str).str.strip()
    df = df[df["recipient_code"] != ""]
    df = df.drop_duplicates(["campaign_name", "recipient_code"], keep="last")
    for col in BOOLS:
        df[col] = df[col].map(to_bool)
    df["status"] = df["status"].fillna("").astype(str).str.strip()
    df.to_csv(destination, index=False, encoding="utf-8-sig")
    return {"before": before, "after": len(df), "removed": before - len(df)}

def main() -> int:
    parser = argparse.ArgumentParser(description="Lam sach du lieu da an danh.")
    parser.add_argument("--input-dir", default="analytics/data/processed")
    parser.add_argument("--output-dir", default="analytics/data/processed")
    args = parser.parse_args()
    src, dest = Path(args.input_dir), Path(args.output_dir)
    files = sorted(src.glob("*_recipients_raw.csv"))
    if not files:
        parser.error(f"Khong tim thay *_recipients_raw.csv trong {src}")
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        out = dest / f.name.replace("_recipients_raw.csv", "_recipients_clean.csv")
        print(f"{f.name} -> {out.name}: {clean_file(f, out)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
