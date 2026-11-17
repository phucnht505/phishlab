# PhishLab – Analytics (Member 04)

Module này nhập CSV xuất từ Gophish, chuẩn hóa/ẩn danh dữ liệu người nhận, tính chỉ số chiến dịch, tạo biểu đồ, Excel report và dashboard web.

## 1. Cấu trúc

```text
analytics/
├── data/
│   ├── sample_gophish_results.csv
│   ├── sample_gophish_events.csv
│   ├── sample_quiz_summary.csv
│   └── processed/             # dữ liệu đã chuẩn hóa (tự tạo)
├── output/                    # Excel/CSV/JSON/PNG sinh ra
├── scripts/
│   ├── analytics_core.py
│   ├── import_results.py
│   ├── clean_data.py
│   └── generate_report.py
└── requirements.txt

dashboard/
└── app.py
```

## 2. Cài đặt (Windows PowerShell)

Chạy từ thư mục gốc của repository:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\analytics\requirements.txt
```

## 3. Xuất dữ liệu từ Gophish

Trong Gophish, mở **Campaigns**, chọn campaign đã chạy và dùng chức năng **Export CSV**. Cần hai file:

- **Results CSV**: thông tin kết quả theo người nhận, thường có `id`, `email`, `status` và một số trường khác.
- **Raw Events CSV**: lịch sử sự kiện, module đọc `email`, `time`, `message`. Cột `details` bị bỏ qua.

Không đưa các CSV chứa email/thông tin người tham gia thật lên Git. Chỉ chạy trong môi trường lab đã được phê duyệt.

## 4. Import và ẩn danh

```powershell
python .\analytics\scripts\import_results.py `
  --results .\analytics\data\campaign_results.csv `
  --events .\analytics\data\campaign_events.csv `
  --campaign-name "PhishLab-Internal-Demo-01" `
  --scenario "IT"
```

`--events` là tùy chọn, nhưng nên cung cấp để có lịch sử sự kiện đầy đủ hơn. Script dùng email trong bộ nhớ để ghép Raw Events với Results; file đầu ra chỉ giữ mã `recipient_code`, trạng thái và cờ sự kiện. Không ghi email, IP, tên, vị trí địa lý hoặc `details` ra dữ liệu đã chuẩn hóa.

## 5. Quiz summary (tổng hợp, không định danh)

Hiện tại `training_portal/js/quiz.js` phát sự kiện trình duyệt `phishlab:quiz-completed` với điểm, tổng câu, phần trăm và thời điểm; file frontend chưa ghi CSV hoặc gửi dữ liệu về máy chủ. Vì vậy module Analytics nhận **số liệu tổng hợp cấp chiến dịch** thay vì liên kết từng điểm quiz với người nhận.

CSV quiz summary cần dạng:

```csv
participants_started,completed_count,average_score
20,16,75.5
```

Số liệu trong ví dụ chỉ minh họa định dạng, không phải kết quả thực nghiệm. Sau khi có CSV tổng hợp thực tế, import kèm:

```powershell
python .\analytics\scripts\import_results.py `
  --results .\analytics\data\campaign_results.csv `
  --events .\analytics\data\campaign_events.csv `
  --quiz-summary .\analytics\data\quiz_summary.csv `
  --campaign-name "PhishLab-Internal-Demo-01" `
  --scenario "IT"
```

Không đưa câu trả lời hoặc điểm gắn với email/người nhận vào file tổng hợp. Nếu chưa có số liệu quiz thực tế, để trống; dashboard không tự bịa Training Completion.

## 6. Làm sạch và tạo báo cáo

```powershell
python .\analytics\scripts\clean_data.py
python .\analytics\scripts\generate_report.py
```

Đầu ra tại `analytics/output/`:
- `campaign_summary.csv` và `campaign_summary.json`.
- `campaign_report.xlsx` gồm Campaign Summary và Anonymized Recipients.
- `charts/interaction_overview.png`.
- `charts/campaign_comparison.png` khi có nhiều campaign.

## 7. Chạy Dashboard

```powershell
streamlit run .\dashboard\app.py
```

Tải Results CSV, Raw Events CSV và Quiz summary CSV (nếu đã có). Sau đó nhấn **Phân tích dữ liệu**. Có thể tải dữ liệu ẩn danh dưới dạng CSV hoặc báo cáo Excel.

## 8. Công thức

| Chỉ số | Công thức |
|---|---|
| Send Rate | Email gửi thành công / Tổng người nhận × 100% |
| Open Rate | Người có sự kiện mở / Email gửi thành công × 100% |
| Click Rate | Người nhấp liên kết / Email gửi thành công × 100% |
| Report Rate | Người báo cáo email / Email gửi thành công × 100% |
| Training Completion | Người hoàn thành quiz / Người bắt đầu quiz × 100% |

Open Rate chỉ mang tính tham khảo do tracking pixel có thể bị chặn hoặc tự tải. Email Sent không có nghĩa email chắc chắn đã vào Inbox. Khi thiếu Raw Events, các trạng thái mở/nhấp/báo cáo được suy ra từ status cuối trong Results CSV và có thể thiếu lịch sử.

## 9. Kiểm thử

Tại thư mục gốc:

```powershell
python -m unittest discover -s tests -v
```

CSV `sample_*.csv` chỉ chứa dữ liệu giả lập với domain `.test`, không phải kết quả chiến dịch thật.

## 10. An toàn

- Không thu thập mật khẩu, OTP, cookie hoặc session token.
- Không đọc/xuất trường `details` từ Raw Events.
- Không lưu email hoặc thông tin định danh trong dashboard/báo cáo.
- Dữ liệu thật và báo cáo phát sinh cần được giữ local, không commit lên Git.
