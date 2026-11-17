"""Streamlit dashboard for PhishLab anonymized campaign analytics."""
from __future__ import annotations
import io, sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics" / "scripts"))
from analytics_core import calculate_metrics, normalize_campaign, normalize_quiz_summary, read_csv

st.set_page_config(page_title="PhishLab Analytics", page_icon="📊", layout="wide")
st.title("PhishLab Analytics Dashboard")
st.caption("Thống kê chiến dịch mô phỏng phishing trong môi trường lab.")

with st.sidebar:
    st.header("Dữ liệu chiến dịch")
    campaign_name = st.text_input("Tên chiến dịch", "PhishLab Internal Demo")
    scenario = st.selectbox("Kịch bản", ["IT", "Delivery", "HR", "Khác"])
    results_upload = st.file_uploader("Gophish Results CSV (bắt buộc)", type=["csv"])
    events_upload = st.file_uploader("Gophish Raw Events CSV (khuyến nghị)", type=["csv"])
    quiz_upload = st.file_uploader("Quiz summary CSV (tùy chọn)", type=["csv"])
    analyze = st.button("Phân tích dữ liệu", type="primary", use_container_width=True)

st.info("Dữ liệu hiển thị đã loại bỏ email và trường details. Không sử dụng mật khẩu, OTP, cookie hoặc session token.")

if analyze:
    if results_upload is None:
        st.error("Vui lòng tải Results CSV.")
        st.stop()
    try:
        results = read_csv(results_upload.getvalue())
        events = read_csv(events_upload.getvalue()) if events_upload else None
        quiz = normalize_quiz_summary(read_csv(quiz_upload.getvalue())) if quiz_upload else None
        recipients, event_rows, warnings = normalize_campaign(results, events, campaign_name, scenario)
        st.session_state["recipients"] = recipients
        st.session_state["events"] = event_rows
        st.session_state["quiz"] = quiz
        st.session_state["warnings"] = warnings
    except Exception as exc:
        st.error(f"Không thể phân tích file: {exc}")
        st.stop()

if "recipients" not in st.session_state:
    st.subheader("Bắt đầu phân tích")
    st.write("Tải Results CSV từ Gophish. Bổ sung Raw Events để thống kê sự kiện đầy đủ hơn.")
    st.code("Gophish → Campaigns → chọn campaign → Export CSV", language="text")
    st.stop()

recipients = st.session_state["recipients"]
events = st.session_state["events"]
metrics = calculate_metrics(recipients, st.session_state.get("quiz"))

st.subheader(campaign_name)
cols = st.columns(5)
for col, (label, value) in zip(cols, [
    ("Người nhận", metrics["total_recipients"]),
    ("Email gửi", metrics["emails_sent"]),
    ("Email mở", metrics["emails_opened"]),
    ("Nhấp liên kết", metrics["links_clicked"]),
    ("Báo cáo email", metrics["emails_reported"]),
]):
    col.metric(label, value)

st.subheader("Tỷ lệ tương tác")
rate_cols = st.columns(4)
for col, label, key in zip(rate_cols, ["Send Rate", "Open Rate", "Click Rate", "Report Rate"],
                           ["send_rate", "open_rate", "click_rate", "report_rate"]):
    value = metrics[key]
    col.metric(label, "—" if value is None else f"{value:.2f}%")

st.subheader("Biểu đồ tương tác")
chart = pd.DataFrame({
    "Sự kiện": ["Sent", "Opened", "Clicked", "Reported"],
    "Số người": [metrics["emails_sent"], metrics["emails_opened"], metrics["links_clicked"], metrics["emails_reported"]],
}).set_index("Sự kiện")
st.bar_chart(chart)

st.subheader("Hiệu quả đào tạo")
a, b, c = st.columns(3)
a.metric("Bắt đầu quiz", "—" if metrics["training_started"] is None else metrics["training_started"])
b.metric("Hoàn thành quiz", "—" if metrics["training_completed"] is None else metrics["training_completed"])
c.metric("Điểm quiz trung bình", "—" if metrics["average_quiz_score"] is None else f"{metrics['average_quiz_score']:.2f}/100")
completion = metrics["training_completion_rate"]
st.metric("Training Completion", "—" if completion is None else f"{completion:.2f}%")
if st.session_state.get("quiz") is None:
    st.caption(f"Chưa có quiz aggregate. Lượt nhấp ({metrics['training_started_proxy']}) chỉ là proxy, không chứng minh trang đào tạo đã tải.")
else:
    st.caption("Quiz data là tổng hợp cấp chiến dịch; không liên kết điểm hoặc câu trả lời với từng người nhận.")

st.subheader("Danh sách tương tác đã ẩn danh")
st.dataframe(recipients, use_container_width=True, hide_index=True)
st.download_button("Tải CSV đã ẩn danh", recipients.to_csv(index=False).encode("utf-8-sig"),
                   "phishlab_anonymized_results.csv", "text/csv")

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    pd.DataFrame([{ "campaign_name": campaign_name, "scenario": scenario, **metrics }]).to_excel(writer, sheet_name="Campaign Summary", index=False)
    recipients.to_excel(writer, sheet_name="Anonymized Recipients", index=False)
    if not events.empty:
        events.to_excel(writer, sheet_name="Events", index=False)
st.download_button("Tải báo cáo Excel", buffer.getvalue(), "phishlab_campaign_report.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if st.session_state.get("warnings"):
    st.subheader("Lưu ý dữ liệu")
    for warning in st.session_state["warnings"]:
        st.warning(warning)

with st.expander("Công thức và giới hạn chỉ số"):
    st.markdown("""
    - Send Rate = Email gửi thành công / Tổng người nhận × 100%.
    - Open Rate = Người có sự kiện mở / Email gửi thành công × 100%. Chỉ mang tính tham khảo vì tracking pixel có thể bị chặn hoặc tự tải.
    - Click Rate = Người nhấp liên kết / Email gửi thành công × 100%.
    - Report Rate = Người báo cáo email / Email gửi thành công × 100%. Chỉ tính khi nguồn ghi nhận sự kiện này.
    - Training Completion = Người hoàn thành quiz / Người bắt đầu quiz × 100%. Cần cung cấp Quiz summary tổng hợp thực tế.
    - Email gửi thành công không đồng nghĩa email chắc chắn đã vào Inbox.
    """)
