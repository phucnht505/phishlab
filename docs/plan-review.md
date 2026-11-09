# PHISHLAB
# KẾ HOẠCH VÀ BIÊN BẢN THEO DÕI CỦA MEMBER 01
**Tên đề tài:** PhishLab – Hệ thống mô phỏng và đánh giá nhận thức người dùng trước các cuộc tấn công Phishing
**Phụ trách:** Member 01 – Project Lead / Analyst
**Phiên bản:** 1.0
---
## 1. Mục đích
Tài liệu này dùng để theo dõi công việc quản lý dự án của Member 01, bao gồm:
- Theo dõi tiến độ thực hiện project.
- Kiểm tra tình trạng hoàn thành các milestone.
- Điều phối giữa các thành viên.
- Review code và tài liệu trước khi tích hợp.
- Ghi nhận vấn đề phát sinh.
- Theo dõi kết quả kiểm thử tích hợp.
- Tổng hợp tình hình thực hiện để phục vụ báo cáo.
Các trạng thái được sử dụng:
| Trạng thái | Ý nghĩa |
|---|---|
| NOT STARTED | Chưa bắt đầu |
| IN PROGRESS | Đang thực hiện |
| PENDING REVIEW | Đang chờ review |
| BLOCKED | Đang bị vướng |
| COMPLETED | Đã hoàn thành và có bằng chứng |
## 2. Phạm vi công việc của Member 01
| STT | Công việc | Sản phẩm / Kết quả |
|---|---|---|
| 1 | Phân tích yêu cầu | `requirements.md` |
| 2 | Xây dựng Use Case | `use-case.md` |
| 3 | Thiết kế kiến trúc | `architecture.md` |
| 4 | Lập và theo dõi kế hoạch | Tài liệu kế hoạch tiến độ |
| 5 | Điều phối thành viên | Ghi nhận tiến độ và vấn đề |
| 6 | Review code | Kết quả review Pull Request |
| 7 | Điều phối tích hợp | Ghi nhận kết quả tích hợp module |
| 8 | Viết phần báo cáo được giao | Tổng quan, mục tiêu và kiến trúc |
## 3. Kế hoạch triển khai tổng thể
Kế hoạch tham khảo của project là 2 tuần, tương đương 14 ngày làm việc.
| Giai đoạn | Thời gian dự kiến | Công việc chính | Kết quả cần đạt |
|---|---|---|---|
| Giai đoạn 1 – Phân tích và thiết kế | Ngày 1–2 | Chốt yêu cầu, Use Case, kiến trúc và phân chia task | Requirements và Architecture được thống nhất |
| Giai đoạn 2 – Xây dựng môi trường | Ngày 3–4 | Cài đặt Gophish, MailHog, cấu hình SMTP và mạng lab | Môi trường lab gửi nhận email được |
| Giai đoạn 3 – Xây dựng chức năng | Ngày 5–7 | Email template, landing page, quiz và script xử lý dữ liệu | Các module MVP được xây dựng |
| Giai đoạn 4 – Tích hợp và kiểm thử | Ngày 8–10 | Kết nối module, chạy chiến dịch thử nghiệm, kiểm tra tracking và báo cáo | MVP hoạt động đầu cuối |
| Giai đoạn 5 – Đánh giá và hoàn thiện | Ngày 11–13 | Chạy chiến dịch nội bộ được phê duyệt, phân tích dữ liệu, hoàn thiện báo cáo và demo | Project có báo cáo và demo |
Lịch trên là kế hoạch tham khảo. Nhóm cập nhật tiến độ theo deadline thực tế và tình trạng hoàn thành từng module.
## 4. Theo dõi milestone
| Milestone | Điều kiện hoàn thành | Bằng chứng cần lưu | Trạng thái |
|---|---|---|---|
| M1 – Requirements và Architecture | Tài liệu yêu cầu và kiến trúc được thống nhất | Requirements, Use Case, Architecture và ý kiến review | IN PROGRESS |
| M2 – Lab Environment | Gophish và MailHog gửi nhận email được trong lab | Cấu hình lab, ảnh giao diện MailHog và kết quả gửi thử | NOT STARTED |
| M3 – Email và Training | Có ít nhất 3 mẫu email và trang đào tạo | Các file template, landing page và ảnh hiển thị | NOT STARTED |
| M4 – Campaign Tracking | Một chiến dịch thử nghiệm chạy và ghi nhận sự kiện | Kết quả campaign và file CSV xuất từ Gophish | NOT STARTED |
| M5 – Report và Demo | Có báo cáo và demo hoàn chỉnh | Dashboard, báo cáo, checklist và video/ảnh demo | NOT STARTED |
**Quy tắc cập nhật:** Chỉ chuyển một milestone sang COMPLETED khi có sản phẩm hoặc bằng chứng kiểm tra được. Không đánh dấu hoàn thành chỉ vì đã lên kế hoạch.
## 5. Theo dõi công việc của sáu thành viên
| Thành viên | Phần việc | Sản phẩm bàn giao | Nội dung Member 01 cần theo dõi |
|---|---|---|---|
| Member 01 | Project Lead / Analyst | Requirements, Use Case, Architecture, kế hoạch và báo cáo được giao | Tiến độ chung, review và tích hợp |
| Member 02 | Infrastructure / Gophish | Cấu hình Gophish, MailHog, nhóm thử nghiệm, campaign và tracking | Kiểm tra môi trường và dữ liệu tracking |
| Member 03 | Frontend / Training | Email templates, landing pages và training portal | Review template, giao diện và luồng đào tạo |
| Member 04 | Data / Dashboard | Analytics, dashboard và báo cáo dữ liệu | Review công thức, biểu đồ và độ chính xác số liệu |
| Member 05 | Documentation | README, deployment guide, tài liệu tham khảo và báo cáo định dạng | Kiểm tra tính nhất quán tài liệu |
| Member 06 | QA / Demo Support | CSV giả lập, checklist, ảnh/video và slide demo | Theo dõi lỗi kiểm thử và kết quả demo |
## 6. Quy trình quản lý tiến độ
### 6.1. Cập nhật tiến độ
Khi theo dõi từng thành viên, ghi nhận các nội dung:
- Công việc đã hoàn thành.
- Công việc đang thực hiện.
- Công việc chưa bắt đầu.
- Khó khăn hoặc vấn đề đang gặp.
- Công việc cần thành viên khác hỗ trợ.
- Sản phẩm hoặc bằng chứng đã bàn giao.
### 6.2. Mẫu cập nhật tiến độ
| Thành viên | Công việc | Trạng thái | Vấn đề | Bước tiếp theo |
|---|---|---|---|---|
| Member 01 | Tài liệu phân tích và thiết kế | Đang thực hiện | Chờ thống nhất tài liệu | Hoàn thành và rà soát |
| Member 02 | Gophish / MailHog | Chưa cập nhật | Chưa có kết quả xác nhận | Kiểm tra môi trường lab |
| Member 03 | Template / Training | Chưa cập nhật | Chưa có sản phẩm xác nhận | Bàn giao template và trang đào tạo |
| Member 04 | Analytics / Dashboard | Chưa cập nhật | Chưa có dữ liệu nguồn xác nhận | Chuẩn bị quy trình xử lý CSV |
| Member 05 | Documentation | Chưa cập nhật | Chưa có tài liệu bàn giao xác nhận | Chuẩn bị README và deployment guide |
| Member 06 | QA / Demo | Chưa cập nhật | Chưa có kết quả kiểm thử xác nhận | Chuẩn bị checklist và dữ liệu giả lập |
Bảng trên là trạng thái ban đầu để bắt đầu theo dõi, không phải kết quả xác nhận tiến độ thực tế của các thành viên. Member 01 cần cập nhật theo tình hình làm việc của nhóm.
## 7. Quy trình Review Code
### 7.1. Mục đích
Đảm bảo code được bàn giao đúng chức năng, có thể tích hợp và không làm ảnh hưởng đến các module khác.
### 7.2. Quy trình review
1. Thành viên hoàn thành công việc trên branch riêng.
2. Thành viên kiểm tra chức năng trước khi tạo Pull Request.
3. Thành viên tạo Pull Request vào branch đích mà nhóm thống nhất.
4. Member 01 kiểm tra mô tả thay đổi và phạm vi file.
5. Kiểm tra code có đúng task được giao hay không.
6. Kiểm tra cách module kết nối với các thành phần liên quan.
7. Kiểm tra hướng dẫn chạy và kết quả test được cung cấp.
8. Ghi nhận lỗi hoặc yêu cầu chỉnh sửa nếu cần.
9. Thành viên cập nhật code và yêu cầu review lại.
10. Chỉ chấp nhận merge khi thay đổi đáp ứng các điều kiện review và kiểm thử của nhóm.
### 7.3. Checklist Review Code
| STT | Nội dung kiểm tra | Kết quả |
|---|---|---|
| 1 | Pull Request có mô tả rõ mục đích và nội dung thay đổi | Chưa review |
| 2 | Thay đổi đúng phạm vi task được giao | Chưa review |
| 3 | File được đặt đúng thư mục trong repository | Chưa review |
| 4 | Không chứa API key, mật khẩu hoặc dữ liệu nhạy cảm | Chưa review |
| 5 | Không chứa email hoặc thông tin cá nhân thật không cần thiết | Chưa review |
| 6 | Không có chức năng thu thập mật khẩu, OTP, cookie hoặc session token | Chưa review |
| 7 | Có hướng dẫn chạy hoặc cấu hình cần thiết | Chưa review |
| 8 | Có kết quả kiểm thử tương ứng với thay đổi | Chưa review |
| 9 | Không làm hỏng chức năng hoặc module liên quan | Chưa review |
| 10 | Đã xử lý các góp ý review | Chưa review |
### 7.4. Mẫu ghi nhận Pull Request
| Trường | Nội dung |
|---|---|
| PR ID / Link | Chưa cập nhật |
| Thành viên gửi PR | Chưa cập nhật |
| Module | Chưa cập nhật |
| Branch nguồn | Chưa cập nhật |
| Branch đích | Chưa cập nhật |
| Nội dung thay đổi | Chưa cập nhật |
| Kết quả kiểm tra | Chưa review |
| Góp ý cần sửa | Chưa cập nhật |
| Kết quả review cuối | PENDING REVIEW |
| Người review | Member 01 |
## 8. Quy trình tích hợp hệ thống
### 8.1. Nguyên tắc
- Tích hợp theo từng module, không chờ tất cả module hoàn thành mới kiểm tra.
- Xác định đầu vào và đầu ra giữa các thành phần.
- Kiểm tra từng kết nối sau khi tích hợp.
- Lưu bằng chứng kiểm thử.
- Không merge thay đổi chưa qua review theo quy trình nhóm.
### 8.2. Danh sách kiểm tra tích hợp
| STT | Thành phần | Nội dung kiểm tra | Kết quả cần đạt |
|---|---|---|---|
| 1 | Gophish – MailHog | Kết nối SMTP và gửi email thử nghiệm | MailHog nhận được email |
| 2 | Email Template – Gophish | Template được hiển thị đúng | Nội dung email đúng mẫu |
| 3 | Gophish – Landing Page | Liên kết chuyển đến trang đào tạo | Trang đào tạo truy cập được |
| 4 | Tracking – Campaign | Sự kiện mở và nhấp được ghi nhận khi tracking hoạt động | Có kết quả tracking |
| 5 | Training Portal – Quiz | Tính điểm và hiển thị kết quả | Điểm được tính đúng |
| 6 | Gophish – Analytics | Đọc dữ liệu CSV | File được xử lý hợp lệ |
| 7 | Analytics – Dashboard | Đối chiếu số liệu và biểu đồ | Số liệu khớp dữ liệu nguồn |
| 8 | Toàn hệ thống | Thực hiện luồng demo đầu cuối | Các thành phần hoạt động theo thiết kế |
### 8.3. Mẫu ghi nhận lỗi tích hợp
| Mã lỗi | Thành phần | Mô tả | Người phụ trách | Trạng thái | Cách xử lý |
|---|---|---|---|---|---|
| INT-01 | Chưa xác định | Chưa ghi nhận lỗi | Chưa phân công | Chưa kiểm tra | Chưa có |
Khi phát sinh lỗi thực tế, thêm dòng mới và cập nhật người phụ trách, trạng thái cùng cách xử lý.
## 9. Biên bản review và tích hợp
### 9.1. Biên bản Review
| Trường | Nội dung |
|---|---|
| Ngày review | Chưa cập nhật |
| PR được review | Chưa cập nhật |
| Thành viên gửi | Chưa cập nhật |
| Người review | Member 01 |
| Phạm vi review | Chưa cập nhật |
| Kết quả | PENDING REVIEW |
| Các vấn đề phát hiện | Chưa có dữ liệu |
| Hướng xử lý | Cập nhật sau khi review |
| Kết luận | Chưa thực hiện review |
### 9.2. Biên bản tích hợp
| Trường | Nội dung |
|---|---|
| Ngày tích hợp | Chưa cập nhật |
| Các module tham gia | Chưa cập nhật |
| Branch / PR liên quan | Chưa cập nhật |
| Kết quả kiểm tra | Chưa có dữ liệu |
| Vấn đề phát sinh | Chưa có dữ liệu |
| Người phụ trách xử lý | Chưa phân công |
| Kết luận | Chưa thực hiện tích hợp |
### 9.3. Lịch sử cập nhật
| Ngày | Người cập nhật | Nội dung thay đổi | Bằng chứng |
|---|---|---|---|
| Chưa cập nhật | Member 01 | Khởi tạo kế hoạch theo dõi và biểu mẫu review | File kế hoạch này |
## 10. Nguyên tắc quản lý Git
Nhóm sử dụng GitHub Flow:
1. Mỗi thành viên làm việc trên branch riêng.
2. Đặt tên branch theo module hoặc nhiệm vụ.
3. Commit với nội dung ngắn gọn, mô tả đúng thay đổi.
4. Push branch lên GitHub.
5. Tạo Pull Request.
6. Review trước khi merge vào `main`.
7. Kiểm tra lại sau khi tích hợp.
**Một số mẫu commit:**
```text
docs: add system architecture
docs: add use case specification
feat: add three email templates
feat: create training landing page
feat: implement training quiz
feat: add campaign result processing
test: add campaign integration test
docs: add deployment guide and README
```
Member 01 có trách nhiệm theo dõi Pull Request, kiểm tra chất lượng thay đổi và phối hợp giải quyết xung đột khi tích hợp.
## 11. Đánh giá tình trạng công việc Member 01
| Hạng mục | Trạng thái ban đầu |
|---|---|
| Requirements | Đã được thành viên phụ trách soạn |
| Use Case | Cần hoàn thành và rà soát |
| Architecture | Cần hoàn thành và rà soát |
| Kế hoạch tiến độ | Đã có kế hoạch tham khảo |
| Biểu mẫu review code | Đã chuẩn bị trong tài liệu |
| Review Pull Request thực tế | Chờ các thành viên bàn giao |
| Kiểm thử tích hợp thực tế | Chờ các module được triển khai |
| Nội dung báo cáo được giao | Cần hoàn thiện và cập nhật theo kết quả thực tế |
**Nguyên tắc:** Không đánh dấu review code hoặc tích hợp là hoàn thành khi chưa có Pull Request, code và kết quả kiểm thử thực tế.
---
**Phụ trách:** Member 01 – Project Lead / Analyst