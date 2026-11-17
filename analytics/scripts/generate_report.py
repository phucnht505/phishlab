"""Generate campaign summaries, charts and Excel report."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from analytics_core import calculate_metrics, discover_clean_campaigns, slugify

def load_data(directory: Path) -> pd.DataFrame:
    paths = discover_clean_campaigns(directory)
    if not paths:
        raise FileNotFoundError(f"Khong tim thay *_recipients_clean.csv trong {directory}")
    return pd.concat([pd.read_csv(p, encoding="utf-8-sig") for p in paths], ignore_index=True)

def load_quiz(directory: Path) -> dict[str, dict]:
    result = {}
    for path in directory.glob("*_quiz_summary.json"):
        result[path.name.replace("_quiz_summary.json", "")] = json.loads(path.read_text(encoding="utf-8"))
    return result

def build_summary(data: pd.DataFrame, quiz_summaries: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for name, group in data.groupby("campaign_name", dropna=False):
        m = calculate_metrics(group, quiz_summaries.get(slugify(str(name))))
        m["campaign_name"] = name
        scenarios = group["scenario"].dropna().astype(str).unique().tolist()
        m["scenario"] = ", ".join(scenarios)
        rows.append(m)
    return pd.DataFrame(rows)

def make_charts(summary: pd.DataFrame, output: Path) -> list[Path]:
    chart_dir = output / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    total = {c: summary[c].fillna(0).sum() for c in
             ["emails_sent", "emails_opened", "links_clicked", "emails_reported"]}
    labels = ["Sent", "Opened", "Clicked", "Reported"]
    values = [total["emails_sent"], total["emails_opened"], total["links_clicked"], total["emails_reported"]]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values)
    ax.bar_label(bars, padding=3)
    ax.set_title("PhishLab – Campaign Interaction Overview")
    ax.set_ylabel("Recipients")
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    p = chart_dir / "interaction_overview.png"
    fig.savefig(p, dpi=160)
    plt.close(fig)
    paths.append(p)

    if len(summary) > 1:
        x = range(len(summary))
        width = .24
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([i-width for i in x], summary["open_rate"].fillna(0), width, label="Open Rate")
        ax.bar(list(x), summary["click_rate"].fillna(0), width, label="Click Rate")
        ax.bar([i+width for i in x], summary["report_rate"].fillna(0), width, label="Report Rate")
        ax.set_xticks(list(x), summary["campaign_name"], rotation=15, ha="right")
        ax.set_ylabel("Rate (%)")
        ax.set_title("Campaign Comparison")
        ax.legend()
        fig.tight_layout()
        p = chart_dir / "campaign_comparison.png"
        fig.savefig(p, dpi=160)
        plt.close(fig)
        paths.append(p)
    return paths

def main() -> int:
    parser = argparse.ArgumentParser(description="Tao bao cao PhishLab.")
    parser.add_argument("--input-dir", default="analytics/data/processed")
    parser.add_argument("--output-dir", default="analytics/output")
    args = parser.parse_args()
    input_dir, output = Path(args.input_dir), Path(args.output_dir)
    data = load_data(input_dir)
    summary = build_summary(data, load_quiz(input_dir))
    output.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output / "campaign_summary.csv", index=False, encoding="utf-8-sig")
    (output / "campaign_summary.json").write_text(summary.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8")
    with pd.ExcelWriter(output / "campaign_report.xlsx", engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Campaign Summary", index=False)
        data.to_excel(writer, sheet_name="Anonymized Recipients", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for col in ws.columns:
                width = min(max(max(len(str(cell.value or "")) for cell in col) + 2, 12), 34)
                ws.column_dimensions[col[0].column_letter].width = width
    for path in make_charts(summary, output):
        print(f"Bieu do: {path}")
    print(f"Bao cao Excel: {output / 'campaign_report.xlsx'}")
    print(f"CSV tong hop: {output / 'campaign_summary.csv'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
