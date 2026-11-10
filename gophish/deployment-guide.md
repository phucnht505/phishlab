# PHISHLAB – HƯỚNG DẪN CÀI ĐẶT VÀ TRIỂN KHAI

> Tài liệu hướng dẫn thiết lập môi trường PhishLab trên máy Windows bằng Docker, khởi chạy Gophish, cấu hình SMTP sandbox, nạp các tài nguyên mô phỏng và kiểm tra luồng hoạt động.  
> **Phạm vi:** Chỉ sử dụng trong môi trường lab được phép, với tài khoản và địa chỉ email giả lập. Không sử dụng tài liệu này để gửi email ra Internet hoặc thu thập thông tin đăng nhập thật.

---

## 1. Giới thiệu

PhishLab là hệ thống mô phỏng và đánh giá nhận thức người dùng trước các tình huống Phishing. Hệ thống tận dụng Gophish để quản lý chiến dịch và ghi nhận sự kiện tương tác; các trang đào tạo, bài kiểm tra và phần xử lý báo cáo được tổ chức trong source code của project.

Tài liệu này tập trung vào việc cài đặt và khởi chạy môi trường. Những nội dung về thiết kế, yêu cầu chức năng và kiến trúc tổng thể được trình bày trong các tài liệu tương ứng của project.

### 1.1. Các thành phần

| Thành phần | Vai trò |
|---|---|
| Docker Desktop | Chạy các dịch vụ được đóng gói dưới dạng container trên Windows. |
| Gophish | Quản lý email template, landing page, nhóm người nhận, campaign và tracking. |
| MailHog | SMTP sandbox dùng để nhận email thử nghiệm trong lab, không chuyển email đến hộp thư bên ngoài. |
| `email_templates/` | Lưu các mẫu email HTML của project để quản lý phiên bản và nạp vào Gophish khi cần. |
| `landing_pages/` | Lưu mã nguồn trang đích mô phỏng/trang đào tạo để nạp vào Gophish. |
| `training_portal/` | Chứa trang đào tạo và quiz do nhóm phát triển, nếu được triển khai độc lập với landing page của Gophish. |
| `analytics/` | Chứa script xử lý dữ liệu campaign và tạo báo cáo. |

### 1.2. Lưu ý về các thư mục template

Các file trong `email_templates/` và `landing_pages/` là **tài nguyên source code**, không phải các dịch vụ tự chạy trong Docker. Việc đặt file vào repository không làm Gophish tự động nhận diện hoặc nạp chúng.

Để sử dụng một mẫu trong chiến dịch, người vận hành cần mở giao diện Gophish và tạo/import nội dung tương ứng tại:

- **Email Templates**: tạo template mới rồi dán/import nội dung HTML từ file trong `email_templates/`.
- **Landing Pages**: tạo landing page mới rồi dán/import nội dung HTML từ file trong `landing_pages/`.

Cách làm này giúp nhóm lưu trữ, chỉnh sửa và review template bằng Git; Gophish vẫn là nơi lưu cấu hình được sử dụng trong campaign.

---

## 2. Yêu cầu môi trường

### 2.1. Phần mềm cần có

| Phần mềm | Mục đích |
|---|---|
| Windows 10/11 | Hệ điều hành triển khai theo môi trường demo của nhóm. |
| Docker Desktop | Quản lý và chạy container. |
| Git | Clone source code và cập nhật project. |
| Trình duyệt web | Truy cập Gophish Admin, MailHog và Training Portal. |
| Python | Chạy các script phân tích dữ liệu nếu project có sử dụng. |

### 2.2. Kiểm tra Docker

Mở PowerShell và chạy:

```powershell
docker --version
docker info
```

Các lệnh cần trả về thông tin phiên bản và trạng thái Docker Engine. Nếu `docker info` báo không kết nối được Docker daemon, hãy mở Docker Desktop và đợi Docker Engine khởi động hoàn tất rồi thử lại.

### 2.3. Kiểm tra cấu trúc project

Mở PowerShell tại thư mục chứa project. Cấu trúc tham khảo:

```text
PhishLab/
├── README.md
├── docs/
│   └── deployment-guide.md
├── gophish/
│   ├── email_templates/
│   ├── landing_pages/
│   ├── sample_groups/
│   └── deployment-guide.md
├── training_portal/
├── analytics/
└── tests/
```

Tên thư mục thực tế có thể khác đôi chút tùy repository hiện tại. Hãy dùng đúng tên và vị trí file đang có trong source code; không tự tạo thêm thư mục chỉ vì ví dụ trên có đề cập.

---

## 3. Lấy source code

Nếu máy chưa có source code, clone repository của nhóm:

```powershell
git clone <REPOSITORY_URL>
cd <REPOSITORY_FOLDER>
```

Thay `<REPOSITORY_URL>` bằng URL repository Git thực tế và `<REPOSITORY_FOLDER>` bằng tên thư mục được tạo sau khi clone.

Nếu source code đã có trên máy, chỉ cần mở PowerShell tại thư mục gốc của project và kiểm tra:

```powershell
git status
dir
```

Không đưa các thông tin nhạy cảm như mật khẩu quản trị, API key, SMTP credential hoặc dữ liệu cá nhân của người tham gia lên Git.

---

## 4. Khởi chạy Gophish bằng Docker

### 4.1. Kiểm tra container hiện có

Trước khi tạo container mới, kiểm tra xem Gophish đã được cài đặt/chạy trên máy hay chưa:

```powershell
docker ps -a --filter "ancestor=gophish/gophish"
```

Có thể xem tên container, image, trạng thái và ánh xạ cổng bằng:

```powershell
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

Nếu đã có container Gophish, không tạo thêm container trùng lặp. Nếu container đang dừng, khởi động lại bằng tên container hiển thị trong cột `NAMES`:

```powershell
docker start <GOPHISH_CONTAINER_NAME>
```

### 4.2. Truy cập Gophish Admin

Theo cấu hình lab tham khảo của project, địa chỉ quản trị thường là:

```text
https://127.0.0.1:3333
```

Địa chỉ này chỉ sử dụng được khi cổng Admin trong container đã được ánh xạ ra cổng `3333` trên máy host. Nếu cấu hình Docker hiện tại ánh xạ sang cổng khác, hãy thay `3333` bằng **host port** hiển thị trong cột `PORTS` của `docker ps`.

Khi đăng nhập lần đầu:

1. Mở cửa sổ terminal/log nơi Gophish khởi động hoặc xem log container để tìm thông tin đăng nhập ban đầu theo cấu hình image đang sử dụng.
2. Truy cập trang Admin qua HTTPS.
3. Nếu trình duyệt cảnh báo chứng chỉ tự ký trong môi trường localhost, chỉ tiếp tục khi đã xác nhận đúng địa chỉ lab của chính mình.
4. Đổi mật khẩu quản trị ngay sau lần đăng nhập đầu tiên.
5. Không chia sẻ thông tin đăng nhập hoặc đưa mật khẩu vào repository.

> **Quan trọng:** Không ánh xạ Gophish Admin ra địa chỉ IP công khai và không mở cổng quản trị ra Internet. Chỉ cho phép truy cập từ máy triển khai hoặc mạng lab được kiểm soát.

### 4.3. Kiểm tra cổng dịch vụ

Kế hoạch triển khai ban đầu sử dụng các cổng tham khảo sau:

| Dịch vụ | Cổng tham khảo trên máy host | Mục đích |
|---|---:|---|
| Gophish Admin | `3333` | Giao diện quản trị Gophish. |
| Gophish Phishing/Landing | `8080` | Địa chỉ phục vụ landing page trong lab. |
| MailHog SMTP | `1025` | Nhận email từ Gophish. |
| MailHog Web | `8025` | Giao diện xem email thử nghiệm. |

Các giá trị này **không thay thế cấu hình Docker thực tế**. Cần kiểm tra cột `PORTS` trong `docker ps` để xác định host port và container port đang được sử dụng.

---

## 5. Khởi chạy MailHog (SMTP sandbox)

MailHog được dùng để kiểm tra luồng gửi email. Email thử nghiệm được hiển thị trong giao diện MailHog thay vì chuyển đến hộp thư thật bên ngoài.

### 5.1. Kiểm tra MailHog

Chạy:

```powershell
docker ps -a --filter "ancestor=mailhog/mailhog"
```

Nếu MailHog chưa có container, nhóm có thể chạy container riêng bằng lệnh tham khảo trên Windows PowerShell:

```powershell
docker run -d `
  --name mailhog `
  -p 127.0.0.1:1025:1025 `
  -p 127.0.0.1:8025:8025 `
  mailhog/mailhog
```

Nếu Docker báo container tên `mailhog` đã tồn tại, không tạo thêm container cùng tên. Kiểm tra container cũ bằng `docker ps -a`; nếu container đang dừng thì có thể khởi động bằng:

```powershell
docker start mailhog
```

### 5.2. Truy cập giao diện MailHog

Nếu cổng Web đã được ánh xạ host port `8025`, mở:

```text
http://127.0.0.1:8025
```

Email được Gophish gửi thành công đến SMTP sandbox sẽ xuất hiện trong giao diện này.

### 5.3. Cấu hình kết nối SMTP giữa Gophish và MailHog

Địa chỉ SMTP phụ thuộc vào nơi Gophish và MailHog đang chạy:

| Cách triển khai | SMTP Host cần cấu hình trong Gophish |
|---|---|
| Gophish chạy trực tiếp trên Windows; MailHog publish cổng `1025` ra host | `127.0.0.1:1025` |
| Gophish và MailHog là hai container độc lập | Hai container phải có đường mạng kết nối được; dùng tên DNS/container trong Docker network chung hoặc cấu hình host gateway phù hợp. Không mặc định dùng `127.0.0.1:1025`. |

**Lý do cần chú ý:** Khi Gophish chạy bên trong container, `127.0.0.1` trỏ về chính container Gophish, không phải container MailHog hoặc máy Windows. Vì vậy, cấu hình `127.0.0.1:1025` có thể đúng với Gophish chạy trực tiếp trên Windows nhưng sai khi Gophish chạy trong Docker.

Nếu hai container chưa nằm trong cùng một Docker network, cần điều chỉnh cấu hình network của các container theo thiết lập thực tế trước khi kiểm tra gửi email. Không tự ý đổi hostname nếu chưa xác định được tên container và network.

---

## 6. Cấu hình Gophish trên giao diện quản trị

Sau khi Gophish truy cập được, đăng nhập bằng tài khoản quản trị và cấu hình lần lượt các thành phần dưới đây.

### 6.1. Tạo Sending Profile

1. Mở **Sending Profiles**.
2. Chọn **New Profile**.
3. Điền thông tin theo môi trường SMTP sandbox đã thiết lập.

| Trường | Giá trị tham khảo |
|---|---|
| Name | `PhishLab-SMTP` |
| Interface Type | `SMTP` |
| From | `Security Lab <training@phishlab.test>` |
| Host | Theo mục 5.3; ví dụ `127.0.0.1:1025` chỉ khi phù hợp với network thực tế. |
| Username | Để trống nếu MailHog không yêu cầu xác thực. |
| Password | Để trống nếu MailHog không yêu cầu xác thực. |
| Ignore Certificate Errors | Không bật nếu không cần. |

Nhấn **Send Test Email**. Sau đó mở MailHog và kiểm tra email thử nghiệm có xuất hiện hay không.

Nếu không nhận được email, kiểm tra lại SMTP Host, cổng SMTP, trạng thái container MailHog và kết nối network giữa hai container.

### 6.2. Tạo nhóm người nhận giả lập

1. Mở **Users & Groups**.
2. Chọn **New Group**.
3. Đặt tên nhóm, ví dụ `PhishLab-Demo-Group`.
4. Thêm người nhận thử nghiệm bằng dữ liệu giả lập hoặc import CSV.

Ví dụ CSV:

```csv
First Name,Last Name,Email,Position
User,Demo01,demo01@phishlab.test,Student
User,Demo02,demo02@phishlab.test,Student
User,Demo03,demo03@phishlab.test,Student
User,Demo04,demo04@phishlab.test,Student
User,Demo05,demo05@phishlab.test,Student
```

Lưu file CSV dưới định dạng UTF-8. Chỉ sử dụng địa chỉ giả lập thuộc phạm vi lab, ví dụ domain `.test`; không import danh sách email thật nếu chưa có phê duyệt và quy trình xử lý dữ liệu phù hợp.

### 6.3. Nạp Email Template từ source code

1. Mở **Email Templates**.
2. Chọn **New Template**.
3. Đặt tên template, ví dụ `IT-Maintenance-Demo`.
4. Mở file HTML tương ứng trong `gophish/email_templates/` (hoặc đúng thư mục template hiện có trong repository).
5. Sao chép nội dung HTML vào trình soạn thảo của Gophish.
6. Lưu template và gửi email kiểm tra vào MailHog.

Nếu nội dung email cần cá nhân hóa theo người nhận, giữ các biến template của Gophish mà source code đang sử dụng. Ví dụ `{{.FirstName}}` là biến tên người nhận và `{{.URL}}` là URL tracking do Gophish tạo cho email trong campaign. Không thay `{{.URL}}` bằng một URL cố định nếu cần Gophish theo dõi lượt nhấp.

Lặp lại các bước trên cho những kịch bản email còn lại trong source code.

### 6.4. Nạp Landing Page từ source code

1. Mở **Landing Pages**.
2. Chọn **New Page**.
3. Đặt tên trang, ví dụ `PhishLab-Awareness`.
4. Mở file HTML tương ứng trong `gophish/landing_pages/` (hoặc đúng thư mục landing page hiện có trong repository).
5. Sao chép nội dung HTML vào trình soạn thảo của Gophish.
6. Lưu và dùng chức năng xem trước để kiểm tra giao diện.

**Thiết lập an toàn bắt buộc:**

- `Capture Submitted Data`: **OFF**.
- `Capture Passwords`: **OFF**.
- Không tạo form yêu cầu đăng nhập.
- Không yêu cầu người tham gia nhập mật khẩu, OTP, cookie hoặc session token.
- Trang đích cần hiển thị nội dung giải thích/đào tạo, không giả lập bước thu thập thông tin xác thực.

### 6.5. Vai trò của Training Portal và Quiz

Nếu project có thư mục `training_portal/`, đây là phần giao diện đào tạo/quiz do nhóm tự phát triển. Nó không tự động được Gophish chạy chỉ vì thư mục nằm trong repository.

Cách triển khai cụ thể phụ thuộc vào cách project kết nối landing page với Training Portal:

- Nếu landing page đã chứa toàn bộ nội dung đào tạo, sử dụng landing page đó theo luồng Gophish.
- Nếu landing page chuyển hướng hoặc liên kết sang Training Portal, cần khởi chạy/host Training Portal theo cấu hình hiện tại của project và kiểm tra URL liên kết.
- Không tự thay đổi URL liên kết nếu chưa xác định cách ứng dụng đang phục vụ file và tài nguyên tĩnh.

---

## 7. Tạo và chạy Campaign thử nghiệm

Chỉ chạy campaign với nhóm người nhận giả lập trong môi trường lab.

### 7.1. Tạo campaign

1. Mở **Campaigns**.
2. Chọn **New Campaign**.
3. Điền thông tin tương ứng với các thành phần đã tạo.

| Trường | Giá trị tham khảo |
|---|---|
| Name | `PhishLab-Internal-Demo-01` |
| Email Template | Template đã nạp ở mục 6.3. |
| Landing Page | Landing page đã nạp ở mục 6.4. |
| URL | Địa chỉ phishing/landing của Gophish có thể truy cập trong lab. |
| Sending Profile | `PhishLab-SMTP` hoặc profile SMTP thực tế đã kiểm tra thành công. |
| Groups | `PhishLab-Demo-Group` hoặc nhóm dữ liệu giả lập tương ứng. |

Địa chỉ `127.0.0.1` chỉ truy cập được từ chính máy đang chạy dịch vụ. Nếu người kiểm thử sử dụng máy khác trong mạng lab, phải cấu hình URL bằng địa chỉ IP nội bộ có thể truy cập được và được firewall cho phép. Không sử dụng địa chỉ Internet công khai.

### 7.2. Kiểm tra luồng campaign

Trước khi chạy, rà soát:

- Sending Profile đã gửi test email thành công.
- MailHog đang hoạt động.
- Email Template được chọn đúng.
- Landing Page được chọn đúng.
- Nhóm người nhận chỉ chứa tài khoản giả lập.
- URL trỏ đến địa chỉ lab có thể truy cập.
- Các tùy chọn thu thập dữ liệu và mật khẩu đều tắt.

Sau khi xác nhận, khởi chạy campaign. Mở MailHog để xem email, mở email thử nghiệm, nhấp liên kết mô phỏng và xác nhận người dùng được chuyển đến trang đào tạo.

### 7.3. Kiểm tra tracking và xuất kết quả

Trên Gophish, mở campaign vừa chạy và kiểm tra các sự kiện được ghi nhận, chẳng hạn:

- Email Sent.
- Email Opened (phụ thuộc cơ chế tải tracking image của email client).
- Clicked Link.

Sau đó sử dụng chức năng xuất kết quả CSV của Gophish để phục vụ phần phân tích dữ liệu. Không xem Open Rate là số liệu tuyệt đối vì email client có thể chặn hoặc tự động tải tracking image.

---

## 8. Chạy Training Portal và phần Analytics

### 8.1. Training Portal (nếu triển khai độc lập)

Nếu `training_portal/` là một trang HTML/CSS/JavaScript tĩnh và máy đã cài Python, có thể chạy web server tĩnh để kiểm tra giao diện.

Mở PowerShell tại thư mục gốc repository:

```powershell
python -m http.server 5500 --directory .\training_portal
```

Sau đó truy cập:

```text
http://127.0.0.1:5500
```

Dừng web server bằng `Ctrl + C` trong cửa sổ PowerShell.

Lệnh trên chỉ phù hợp với trang tĩnh. Nếu Training Portal hiện tại sử dụng framework, bundler, backend hoặc script khởi chạy riêng, hãy dùng lệnh được định nghĩa trong `package.json`, README hoặc tài liệu kỹ thuật của module đó; không thay thế bằng web server tĩnh.

### 8.2. Analytics và báo cáo

Thư mục `analytics/` chứa phần xử lý dữ liệu và tạo báo cáo. Quy trình tổng quát:

1. Xuất kết quả campaign từ Gophish dưới dạng CSV.
2. Đặt file CSV vào đúng thư mục input mà script của project quy định.
3. Chạy các script theo thứ tự được ghi trong README hoặc hướng dẫn của module Analytics.
4. Kiểm tra dữ liệu đầu ra và đối chiếu số liệu với CSV gốc trên Gophish.

Nếu repository có `requirements.txt`, cài dependency trong virtual environment theo hướng dẫn của project. Ví dụ tạo môi trường ảo trên Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sau đó, chỉ chạy lệnh cài dependency khi đã xác nhận file dependency của project tồn tại:

```powershell
python -m pip install -r requirements.txt
```

Nếu dependency file nằm trong một thư mục con, thay đường dẫn cho đúng vị trí. Không tự thêm package hoặc tự đoán lệnh chạy script khi chưa kiểm tra source code hiện tại.

---

## 9. Kiểm tra sau cài đặt

Sử dụng checklist sau để xác nhận môi trường đã sẵn sàng cho demo.

| Mã | Nội dung kiểm tra | Kết quả mong đợi |
|---|---|---|
| INS-01 | Docker Engine hoạt động | Các lệnh `docker info` thực thi thành công. |
| INS-02 | Gophish container hoạt động | Container ở trạng thái `Up`. |
| INS-03 | Gophish Admin | Truy cập được bằng host port đã ánh xạ. |
| INS-04 | MailHog hoạt động | Container ở trạng thái `Up` và mở được giao diện Web. |
| INS-05 | SMTP | Gophish gửi test email và MailHog nhận được. |
| INS-06 | Recipient Group | Import được danh sách người nhận giả lập. |
| INS-07 | Email Template | Template đã được nạp và hiển thị đúng trong email test. |
| INS-08 | Landing Page | Trang hiển thị đúng nội dung đào tạo. |
| INS-09 | Campaign | Campaign thử nghiệm chạy với nhóm giả lập. |
| INS-10 | Tracking | Gophish ghi nhận được sự kiện nhấp liên kết khi thực hiện kiểm thử. |
| INS-11 | Data Safety | Không có mật khẩu, OTP hoặc session token được thu thập. |
| INS-12 | Export | Xuất được CSV để phục vụ Analytics. |
| INS-13 | Training Portal/Quiz | Mở được quiz và kết quả hiển thị đúng theo thiết kế hiện tại. |
| INS-14 | Analytics | Báo cáo/biểu đồ tạo được và khớp với dữ liệu nguồn. |

---

## 10. Xử lý một số lỗi thường gặp

### 10.1. Không truy cập được Gophish Admin

Kiểm tra:

```powershell
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

- Container có đang chạy không?
- Host port có được ánh xạ đúng không?
- Địa chỉ truy cập có dùng đúng host port không?
- Log container có thông báo lỗi khởi động không?

Xem log bằng:

```powershell
docker logs <GOPHISH_CONTAINER_NAME>
```

### 10.2. Gophish không gửi được email đến MailHog

Kiểm tra:

1. MailHog container có đang chạy không?
2. SMTP Host có đúng với topology Docker không?
3. Gophish và MailHog có kết nối được qua Docker network không?
4. Cổng SMTP đang dùng có đúng là cổng nội bộ `1025` không?
5. Sending Profile có đang dùng đúng profile vừa kiểm tra không?

Lưu ý quan trọng: nếu Gophish chạy trong container, `127.0.0.1` là loopback của container Gophish. Không dùng giá trị này để trỏ sang container MailHog khác.

### 10.3. Email không xuất hiện trong MailHog

- Xem kết quả Send Test Email trong Gophish.
- Kiểm tra log Gophish và MailHog.
- Kiểm tra lại SMTP hostname, port và network.
- Xác nhận campaign đang sử dụng đúng Sending Profile.

### 10.4. Nhấp liên kết nhưng không đến được Landing Page

- Kiểm tra URL trong campaign.
- Kiểm tra host port của Gophish Phishing Server.
- Nếu dùng máy khác, không sử dụng `127.0.0.1` của máy chủ làm địa chỉ truy cập từ máy người nhận.
- Kiểm tra firewall trong phạm vi mạng lab.

### 10.5. Không thấy template trong Gophish

File HTML nằm trong source code không tự động xuất hiện trong giao diện Gophish. Hãy vào **Email Templates** hoặc **Landing Pages** và thực hiện thao tác tạo mới/nạp nội dung thủ công như mục 6.3 và 6.4.

## 11. Dừng hệ thống và bảo toàn dữ liệu

Nếu chạy container độc lập, có thể dừng bằng:

```powershell
docker stop <GOPHISH_CONTAINER_NAME>
docker stop <MAILHOG_CONTAINER_NAME>
```

Chỉ dừng các container thực sự thuộc project. Trước khi xóa container hoặc volume, cần xác định vị trí dữ liệu Gophish đang được mount/persist trong Docker configuration.

---

## 12. Nguyên tắc an toàn khi vận hành

1. Chỉ thử nghiệm trên máy cá nhân hoặc mạng lab được phê duyệt.
2. Chỉ dùng người nhận giả lập trong quá trình kiểm thử kỹ thuật.
3. Không gửi email mô phỏng tới người ngoài phạm vi được cho phép.
4. Không công khai Gophish Admin hoặc SMTP sandbox ra Internet.
5. Không thu thập mật khẩu, OTP, cookie hoặc session token.
6. Tắt `Capture Submitted Data` và `Capture Passwords` trên Landing Page.
7. Không commit mật khẩu, API key, database, file cấu hình nhạy cảm hoặc dữ liệu người tham gia lên Git.
8. Khi triển khai demo với người tham gia thật, phải có sự phê duyệt, thông báo/phạm vi thử nghiệm và biện pháp bảo vệ dữ liệu phù hợp.

---

## 13. Thông tin cần đối chiếu trước khi phát hành tài liệu

Một số thông số phụ thuộc trực tiếp vào cấu hình Docker và source code phiên bản hiện tại. Người phụ trách triển khai cần rà soát và cập nhật các mục sau trước khi chốt tài liệu:

| Nội dung | Cần đối chiếu ở đâu |
|---|---|
| URL repository | Trang Git repository của nhóm. |
| Tên thư mục gốc | Thư mục source code sau khi clone. |
| Tên container Gophish | Cột `NAMES` của `docker ps`. |
| Tên container MailHog | Cột `NAMES` của `docker ps`. |
| Host port và container port | Cột `PORTS` của `docker ps`. |
| Docker network | `docker network inspect`. |
| Đường dẫn lưu database/config Gophish | Thông tin mount của container. |
| Tên và vị trí email template | Source code thực tế trong repository. |
| Tên và vị trí landing page | Source code thực tế trong repository. |
| Lệnh chạy Training Portal | README/package script hoặc cấu hình triển khai hiện tại. |
| Dependency và lệnh chạy Analytics | `requirements.txt`, README và source code Analytics. |

> **Ghi chú phiên bản:** Các cổng `3333`, `8080`, `1025`, `8025` và tên service `mailhog` trong tài liệu là giá trị tham khảo theo kế hoạch lab. Chỉ giữ nguyên trong bản phát hành cuối nếu chúng khớp với ánh xạ cổng và tên service trong cấu hình hiện tại của project.
