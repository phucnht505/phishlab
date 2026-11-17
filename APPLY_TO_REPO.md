# Hướng dẫn tích hợp module Member 04 vào repository PhishLab

## Phạm vi thay đổi

Giải nén toàn bộ thư mục trong ZIP vào thư mục gốc `phishlab` (chọn Merge nếu Windows hỏi). Gói chỉ thêm các file:
- `analytics/scripts/`: import, clean, tính metrics, tạo biểu đồ và báo cáo.
- `analytics/data/sample_*.csv`: bộ dữ liệu giả lập `.test`.
- `analytics/requirements.txt`, `analytics/README.md`, `analytics/.gitignore`.
- `dashboard/app.py`, `dashboard/README.md`.
- `tests/test_analytics.py`.


## Cập nhật nhánh Git trước khi chép file

Mở PowerShell tại thư mục repository:

```powershell
git status
git fetch origin
git switch feature/member04_analytic
git merge --ff-only origin/main
```

Nếu `git status` cho thấy có thay đổi chưa commit, hãy commit hoặc sao lưu chúng trước. Nếu `git merge --ff-only` không thực hiện được, dừng lại và kiểm tra lịch sử nhánh, không dùng `reset --hard`.

## Chép source code và kiểm thử

Sau khi giải nén ZIP vào thư mục gốc repository:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\analytics\requirements.txt
python -m unittest discover -s tests -v
```

## Chạy thử bằng dữ liệu giả lập

```powershell
python .\analytics\scripts\import_results.py `
  --results .\analytics\data\sample_gophish_results.csv `
  --events .\analytics\data\sample_gophish_events.csv `
  --quiz-summary .\analytics\data\sample_quiz_summary.csv `
  --campaign-name "PhishLab-Sample-Demo" `
  --scenario "IT"

python .\analytics\scripts\clean_data.py
python .\analytics\scripts\generate_report.py
```

Mở `analytics/output/campaign_report.xlsx` và `analytics/output/charts/interaction_overview.png` để xem đầu ra.

Chạy Dashboard:

```powershell
streamlit run .\dashboard\app.py
```

## Commit và push lên đúng branch

```powershell
git add analytics dashboard tests
git status
git commit -m "feat: implement member 04 analytics dashboard"
git push -u origin feature/member04_analytic
```

Sau đó tạo Pull Request từ `feature/member04_analytic` vào `main`. Không merge trực tiếp vào `main` nếu nhóm đang áp dụng quy trình review.

## Lưu ý Quiz hiện tại

Trong `training_portal/js/quiz.js` trên `main`, quiz phát custom event `phishlab:quiz-completed` ở trình duyệt; hiện chưa thấy cơ chế gửi dữ liệu tổng hợp lên máy chủ hoặc xuất CSV. Vì thế Analytics nhận file Quiz summary aggregate (một dòng số liệu cấp campaign), không nhận điểm từng người và không tự bịa số liệu nếu file này chưa có.
