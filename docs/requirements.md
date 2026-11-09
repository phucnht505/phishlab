# PHISHLAB
# TÀI LIỆU ĐẶC TẢ YÊU CẦU HỆ THỐNG
**Tên đề tài:** PhishLab – Hệ thống mô phỏng và đánh giá nhận thức người dùng trước các cuộc tấn công Phishing
**Tài liệu:** Requirements Specification
**Phiên bản:** 1.0
**Phụ trách:** Member 01 – Project Lead / Analyst
---
## 1. Giới thiệu
### 1.1. Mục đích tài liệu
Tài liệu này mô tả các yêu cầu chức năng, yêu cầu phi chức năng, phạm vi và tiêu chí nghiệm thu của hệ thống PhishLab.
Đây là cơ sở để các thành viên thống nhất chức năng cần triển khai, phân chia công việc, thiết kế kiến trúc, xây dựng use case và kiểm thử hệ thống.
### 1.2. Tổng quan đề tài
PhishLab là hệ thống mô phỏng và đánh giá nhận thức người dùng trước các cuộc tấn công Phishing.
Hệ thống được xây dựng nhằm mô phỏng các tình huống email phishing trong môi trường nội bộ hoặc phòng lab được phê duyệt. Người tham gia tương tác với email mô phỏng, được chuyển đến trang hướng dẫn nhận diện phishing và có thể thực hiện bài kiểm tra nhận thức.
Kết quả tương tác được tổng hợp để đánh giá mức độ nhận diện phishing và đề xuất nội dung đào tạo phù hợp.
### 1.3. Mục tiêu hệ thống
- Kiểm tra khả năng nhận diện email phishing của người tham gia.
- Mô phỏng website phishing nhưng không thu thập thông tin đăng nhập thật.
- Theo dõi các hành vi cần thiết như gửi email, mở email và nhấp vào liên kết mô phỏng.
- Ghi nhận việc hoàn thành nội dung đào tạo và kết quả bài kiểm tra ở dạng phù hợp với phạm vi bảo vệ dữ liệu.
- Tổng hợp kết quả thành báo cáo đánh giá nhận thức an toàn thông tin.
- Đưa ra khuyến nghị và nội dung đào tạo phù hợp.
## 2. Phạm vi hệ thống
### 2.1. Phạm vi triển khai
PhishLab tập trung vào các chức năng sau:
- Sử dụng Gophish để quản lý email template, nhóm người nhận, chiến dịch và theo dõi tương tác.
- Sử dụng MailHog làm SMTP sandbox để nhận email thử nghiệm trong môi trường lab.
- Xây dựng trang đích đào tạo nhận diện phishing.
- Xây dựng bài kiểm tra nhận thức bằng HTML, CSS và JavaScript.
- Sử dụng Python để xử lý và tổng hợp dữ liệu chiến dịch.
- Sử dụng Excel hoặc dashboard để trực quan hóa kết quả và tạo báo cáo.
### 2.2. Ngoài phạm vi
Các nội dung sau không thuộc phạm vi triển khai của PhishLab:
- Thu thập mật khẩu hoặc thông tin đăng nhập thật.
- Thu thập mã OTP, cookie hoặc session token.
- Xây dựng credential harvester.
- Sử dụng phishing reverse proxy hoặc Evilginx2.
- Mô phỏng đăng nhập nhằm chiếm đoạt tài khoản.
- Gửi email phishing đến người nhận bên ngoài phạm vi được phê duyệt.
- Xây dựng lại các chức năng quản lý chiến dịch, người nhận và tracking mà Gophish đã cung cấp.
### 2.3. Môi trường hoạt động
Hệ thống hoạt động trong mạng lab hoặc mạng nội bộ đã được phê duyệt.
Trong MVP, MailHog được sử dụng làm SMTP sandbox để giữ email thử nghiệm trong môi trường lab. Nếu triển khai chiến dịch với người tham gia nội bộ thật, nhóm phải có sự phê duyệt của tổ chức và sử dụng SMTP relay thử nghiệm được cấp phép.
## 3. Tác nhân hệ thống
### 3.1. Admin
Là người quản lý chiến dịch mô phỏng thông qua Gophish.
Các hoạt động chính:
- Quản lý nhóm người nhận thử nghiệm.
- Chọn và quản lý email template.
- Chọn landing page.
- Cấu hình sending profile và chiến dịch.
- Khởi chạy chiến dịch trong phạm vi được phê duyệt.
- Theo dõi kết quả chiến dịch và xuất dữ liệu.
### 3.2. Người tham gia
Là người nhận email mô phỏng trong chiến dịch.
Các hoạt động chính:
- Nhận email trong hộp thư thử nghiệm.
- Mở email.
- Nhấp vào liên kết mô phỏng.
- Xem nội dung hướng dẫn nhận diện phishing.
- Thực hiện bài kiểm tra nhận thức nếu chức năng quiz được triển khai.
### 3.3. Thành viên phân tích dữ liệu
Là thành viên phụ trách xử lý dữ liệu và báo cáo.
Các hoạt động chính:
- Nhận dữ liệu xuất từ Gophish.
- Xử lý và tổng hợp dữ liệu bằng Python.
- Tạo biểu đồ và báo cáo.
- Đối chiếu số liệu dashboard với dữ liệu nguồn.
## 4. Yêu cầu chức năng
Mức độ ưu tiên được chia thành:
- **Bắt buộc:** Chức năng cần có trong phạm vi project.
- **Nên có:** Chức năng được khuyến nghị triển khai nếu đáp ứng được thời gian và nguồn lực.
- **Mở rộng:** Chức năng có thể phát triển thêm sau MVP.
### 4.1. FR01 – Quản lý email mẫu
**Mức độ:** Bắt buộc
**Thành viên phụ trách:** Member 03
**Mô tả:**
Hệ thống cần có các email mẫu phục vụ mô phỏng những tình huống phishing khác nhau.
**Yêu cầu chi tiết:**
- Có ít nhất 3 mẫu email mô phỏng.
- Các mẫu có thể được tạo, chỉnh sửa và lưu trong Gophish.
- Mỗi mẫu đại diện cho một kịch bản khác nhau.
- Nội dung sử dụng tổ chức và tên miền giả lập trong lab.
**Ba kịch bản đề xuất:**
1. Thông báo từ bộ phận IT: thông báo cập nhật quy trình hoặc bảo trì hệ thống nội bộ.
2. Thông báo giao hàng: thông báo có bưu kiện cần xác nhận thông tin giao nhận.
3. Thông báo từ bộ phận nhân sự: thông báo chương trình phúc lợi hoặc sự kiện nội bộ.
### 4.2. FR02 – Quản lý người tham gia
**Mức độ:** Bắt buộc
**Thành viên phụ trách:** Member 02
**Mô tả:**
Hệ thống cần hỗ trợ tạo và quản lý danh sách người nhận thử nghiệm phục vụ chiến dịch.
**Yêu cầu chi tiết:**
- Tạo nhóm người nhận thử nghiệm.
- Thêm người nhận thủ công hoặc nhập từ file CSV.
- Sử dụng dữ liệu giả lập trong quá trình demo.
- Có thể lựa chọn nhóm người nhận khi cấu hình chiến dịch.
### 4.3. FR03 – Quản lý chiến dịch
**Mức độ:** Bắt buộc
**Thành viên phụ trách:** Member 02
**Mô tả:**
Admin sử dụng Gophish để tạo, cấu hình và khởi chạy chiến dịch mô phỏng.
**Yêu cầu chi tiết:**
- Tạo chiến dịch mới.
- Chọn email template.
- Chọn landing page.
- Chọn sending profile.
- Chọn nhóm người nhận.
- Khởi chạy chiến dịch trong môi trường được phê duyệt.
- Xem trạng thái và kết quả chiến dịch.
### 4.4. FR04 – Mô phỏng website và trang đào tạo
**Mức độ:** Bắt buộc
**Thành viên phụ trách:** Member 03
**Mô tả:**
Sau khi người tham gia nhấp vào liên kết trong email mô phỏng, hệ thống chuyển họ đến trang hướng dẫn nhận diện phishing.
**Yêu cầu chi tiết:**
- Trang đích hiển thị thông báo đây là hoạt động mô phỏng phục vụ đào tạo.
- Cung cấp các dấu hiệu nhận diện email phishing.
- Có nội dung hướng dẫn phòng tránh.
- Hiển thị nội dung đào tạo ngay sau khi người tham gia truy cập.
- Không có biểu mẫu đăng nhập.
- Không có trường nhập mật khẩu hoặc OTP.
### 4.5. FR05 – Theo dõi tương tác
**Mức độ:** Bắt buộc
**Thành viên phụ trách:** Member 02
**Mô tả:**
Hệ thống cần ghi nhận những sự kiện tương tác chính trong chiến dịch.
**Yêu cầu chi tiết:**
- Ghi nhận trạng thái gửi email.
- Ghi nhận lượt mở email khi cơ chế tracking hoạt động.
- Ghi nhận lượt nhấp vào liên kết mô phỏng.
- Cho phép xem kết quả tracking trong Gophish.
- Có thể xuất dữ liệu chiến dịch để phục vụ phân tích.
**Lưu ý:** Open Rate chỉ mang tính tham khảo vì cơ chế tracking bằng ảnh có thể bị email client chặn hoặc tự động tải.
### 4.6. FR06 – Báo cáo và thống kê
**Mức độ:** Bắt buộc
**Thành viên phụ trách:** Member 04
**Mô tả:**
Hệ thống cần tổng hợp kết quả chiến dịch để đánh giá mức độ tương tác của người tham gia.
**Yêu cầu chi tiết:**
- Nhận dữ liệu từ file CSV hoặc API của Gophish.
- Xử lý và tổng hợp dữ liệu bằng Python.
- Hiển thị các chỉ số chiến dịch.
- Có biểu đồ thống kê kết quả.
- Hỗ trợ xuất báo cáo CSV, Excel hoặc PDF theo phạm vi triển khai.
### 4.7. FR07 – Đào tạo nhận thức
**Mức độ:** Nên có
**Thành viên phụ trách:** Member 03
**Mô tả:**
Hệ thống cung cấp nội dung đào tạo giúp người tham gia nhận diện và phòng tránh phishing.
**Yêu cầu chi tiết:**
- Trình bày các dấu hiệu nhận biết email phishing.
- Cung cấp khuyến nghị phòng tránh.
- Nội dung dễ hiểu và phù hợp với mục tiêu đào tạo nhận thức.
### 4.8. FR08 – Đánh giá sau đào tạo
**Mức độ:** Nên có
**Thành viên phụ trách:** Member 03 và Member 04
**Mô tả:**
Hệ thống có thể cung cấp bài kiểm tra ngắn để đánh giá khả năng nhận diện phishing sau khi người tham gia hoàn thành nội dung đào tạo.
**Yêu cầu chi tiết:**
- Cung cấp bài kiểm tra nhận diện phishing.
- Tính điểm bài kiểm tra.
- Tổng hợp kết quả phục vụ đánh giá và khuyến nghị.
- Chỉ lưu điểm số tổng hợp, không lưu câu trả lời gắn với danh tính hoặc email cá nhân.
### 4.9. FR09 – Phân quyền quản trị
**Mức độ:** Mở rộng
**Thành viên phụ trách:** Chưa phân công trong phạm vi MVP
**Mô tả:**
Có thể phát triển chức năng giới hạn quyền truy cập dashboard và dữ liệu theo vai trò người dùng.
## 5. Yêu cầu phi chức năng
### 5.1. Bảo mật
- Máy chủ chỉ hoạt động trong mạng lab hoặc mạng nội bộ được phê duyệt.
- Không lưu mật khẩu hoặc OTP.
- Không thu thập cookie hoặc session token.
- Không sử dụng tên miền, thương hiệu hoặc giao diện đăng nhập thật để đánh lừa người dùng bên ngoài phạm vi được phép.
- Hạn chế quyền truy cập dữ liệu người tham gia.
- Gophish phải đặt **Capture Submitted Data = OFF** và **Capture Passwords = OFF**.
- Không tạo biểu mẫu đăng nhập hoặc trường nhập thông tin xác thực.
### 5.2. Hiệu năng
- Hỗ trợ chạy chiến dịch cho một nhóm người dùng thử nghiệm.
- Có thể tổng hợp kết quả nhanh chóng sau khi kết thúc chiến dịch.
### 5.3. Khả năng sử dụng
- Giao diện quản lý đơn giản.
- Có thể xem các chỉ số chiến dịch mà không cần truy vấn cơ sở dữ liệu thủ công.
- Trang đào tạo có nội dung rõ ràng và dễ hiểu.
- Có tài liệu hướng dẫn triển khai và sử dụng.
## 6. Yêu cầu dữ liệu và báo cáo
### 6.1. Các trường dữ liệu
| Trường dữ liệu | Ý nghĩa |
|---|---|
| Campaign ID | Mã chiến dịch |
| Recipient Code | Mã người tham gia đã giả danh |
| Email Sent | Trạng thái gửi email |
| Email Opened | Trạng thái mở email |
| Link Clicked | Trạng thái nhấp liên kết |
| Training Completed | Trạng thái hoàn thành đào tạo |
| Quiz Score | Điểm bài kiểm tra |
| Reported | Trạng thái email được báo cáo qua kênh báo cáo |
Không cần lưu thông tin định danh cá nhân vào dashboard phân tích. Có thể sử dụng mã giả lập thay cho tên và email.
Đối với trường Reported, nhóm cần định nghĩa một kênh báo cáo nội bộ và xác nhận sự kiện trước khi đưa vào báo cáo. Không mặc định Gophish tự động ghi nhận mọi thao tác báo cáo email của người dùng.
### 6.2. Các chỉ số thống kê
| Chỉ số | Công thức |
|---|---|
| Send Rate | Số email gửi thành công / Tổng người nhận × 100% |
| Open Rate | Số lượt mở / Số email gửi thành công × 100% |
| Click Rate | Số người nhấp liên kết / Số email gửi thành công × 100% |
| Report Rate | Số email được báo cáo / Số email gửi thành công × 100% |
| Training Completion | Số người hoàn thành đào tạo / Số người được đưa đến trang đào tạo × 100% |
Open Rate có thể không phản ánh chính xác toàn bộ lượt mở email. Dashboard cần thể hiện đây là chỉ số tham khảo.
### 6.3. Các khu vực dashboard đề xuất
- **Campaign Overview:** Tổng số email, số email gửi thành công và số tương tác.
- **Interaction Analysis:** Tỷ lệ mở, nhấp và báo cáo.
- **Scenario Comparison:** So sánh ba kịch bản IT, giao hàng và HR.
- **Training Effectiveness:** Điểm quiz, tỷ lệ hoàn thành và những dấu hiệu phishing người tham gia còn nhầm lẫn.
## 7. Công nghệ sử dụng
| Công nghệ | Vai trò |
|---|---|
| Gophish | Quản lý chiến dịch, nhóm người nhận, email template và tracking |
| MailHog | SMTP sandbox, giữ email thử nghiệm trong lab |
| HTML/CSS/JavaScript | Xây dựng trang đào tạo và quiz |
| Python | Xử lý dữ liệu và tạo báo cáo |
| Pandas | Làm sạch và tổng hợp dữ liệu |
| Matplotlib | Vẽ biểu đồ |
| Excel | Báo cáo thống kê |
| SQLite | Cơ sở dữ liệu mặc định của Gophish; có thể dùng thêm SQLite riêng cho kết quả quiz tổng hợp |
Nhóm tận dụng các chức năng có sẵn của Gophish thay vì xây dựng lại phần quản lý chiến dịch, người nhận, template và tracking.
## 8. Tiêu chí nghiệm thu
Các tiêu chí dưới đây được dùng để đánh giá những kết quả chính của project:
| Mã | Tiêu chí nghiệm thu | Kết quả cần đạt |
|---|---|---|
| AC01 | Email mẫu | Có ít nhất 3 email mẫu mô phỏng |
| AC02 | Chiến dịch | Có ít nhất 1 chiến dịch chạy trong môi trường lab |
| AC03 | SMTP sandbox | MailHog nhận được email thử nghiệm |
| AC04 | Tracking | Gophish ghi nhận được các sự kiện mở và nhấp khi tracking hoạt động |
| AC05 | Trang đào tạo | Trang đào tạo hiển thị sau khi nhấp liên kết |
| AC06 | Bảo vệ dữ liệu | Không thu thập mật khẩu, OTP hoặc session token |
| AC07 | Báo cáo | Có báo cáo thống kê từ kết quả chiến dịch thực tế |
| AC08 | Đào tạo | Có nội dung khuyến nghị nhận diện và phòng tránh phishing |
| AC09 | Tài liệu và demo | Có tài liệu triển khai, hướng dẫn demo và ảnh/video minh chứng |
## 9. Phân công trách nhiệm liên quan đến yêu cầu
| Thành viên | Vai trò | Trách nhiệm chính |
|---|---|---|
| Member 01 | Project Lead / Analyst | Phân tích yêu cầu, use case, kiến trúc, điều phối và review |
| Member 02 | Infrastructure / Gophish | Cài đặt Gophish, MailHog, nhóm người nhận, campaign và tracking |
| Member 03 | Frontend / Training | Email template, landing page, quiz và nội dung đào tạo |
| Member 04 | Data / Dashboard | Xử lý dữ liệu, biểu đồ, dashboard và báo cáo |
| Member 05 | Documentation | README, deployment guide, tài liệu tham khảo và định dạng báo cáo |
| Member 06 | QA / Demo Support | Dữ liệu giả lập, checklist kiểm thử, ảnh/video và slide demo |
## 10. Giới hạn và lưu ý triển khai
- Project chỉ được sử dụng trong môi trường lab hoặc phạm vi nội bộ được phê duyệt.
- Dữ liệu người nhận trong quá trình demo phải là dữ liệu giả lập.
- MailHog được sử dụng để giữ email thử nghiệm, không gửi email đến hộp thư bên ngoài.
- Nếu triển khai với người tham gia nội bộ thật, cần có phê duyệt và SMTP relay thử nghiệm được cấp phép.
- Không commit API key, SMTP password, file database Gophish hoặc thông tin đăng nhập quản trị lên repository.
- Các thông tin định danh cá nhân không cần thiết không được đưa vào dashboard phân tích.
## 11. Tài liệu liên quan
- `use-case.md` – Mô tả các tác nhân và luồng sử dụng hệ thống.
- `architecture.md` – Mô tả kiến trúc tổng thể và luồng dữ liệu.
- `test-cases.md` – Danh sách trường hợp kiểm thử.
- `deployment-guide.md` – Hướng dẫn triển khai môi trường.
- `final-report.md` – Báo cáo tổng kết project.
---
**Phụ trách:** Member 01 – Project Lead / Analyst