---
url: "https://vnstocks.com/docs/vnstock/api-dat-lenh-giao-dich-dnse"
title: "API đặt lệnh giao dịch với DNSE | Vnstock"
---

Toggle Sidebar

### Mục lục

DNSE API

DNSE là một trong 4 công ty chứng khoán có cung cấp API giao dịch cho khách hàng phổ thông bên cạnh SSI, TCBS và BSC (hiện tại hạn chế đăng ký mới).
API giao dịch của DNSE cho phép thực hiện đọc thông tin liên quan đến tài khoản và đặt lệnh đối với cả giao dịch cơ sở lẫn phái sinh. Tài liệu HTTPS API chính thức cập nhật công khai trên website của DNSE [tại đây](https://hdsd.dnse.com.vn/san-pham-dich-vu/api-lightspeed)

Vnstock cung cấp phương thức kết nối API hoàn chỉnh với DNSE để cộng đồng có thể từng bước làm quen với hình thức tự động hoá giao dịch với thuật toán.

Để bắt đầu sử dụng, các bạn cần cài đặt gói thư viện vnstock mới nhất có hỗ trợ đầy đủ các chức năng cho DNSE Lightspeed API. Từ các hàm python này, các bạn có thể xây dựng bot giao dịch/web app dễ dàng từ môi trường cloud hoặc máy tính cá nhân.

## Đăng nhập và xác thực

### Khởi tạo DNSE Client

Để có thể sử dụng các chức năng của DNSE API, trước hết bạn cần khởi tạo một đối tượng DNSE Client, theo đó các hàm chức năng sẽ là các phương thức của đối tượng Client này. Chúng ta gán Client này với biến `client` cho ngắn gọn để gọi trong các bước tiếp theo.

Python

```python
from vnstock.connector.dnse import Trade
client = Trade()
```

### Đăng nhập hệ thống

JWT token

Tại bước này, bạn sử dụng tên đăng nhập và mật khẩu của tài khoản giao dịch DNSE để tạo ra JWT token - là mã xác thực được tạo ra khi bạn đăng nhập vào hệ thống API của DNSE. JWT token cho phép bạn đọc các thông tin về tài khoản (Xác thực cấp 1), để thực hiện đặt lệnh, sửa thông tin hệ thống thì cần dùng kết hợp với mã OTP được cấp qua email hoặc SmartOTP trên app EntradeX (xác thực cấp 2).

Bạn sử dụng đoạn mã sau để đăng nhập hệ thống API.

Python

```python
user_name = "TÊN_ĐĂNG_NHẬP_TÀI_KHOẢN_DNSE"
password = "MẬT_KHẨU_TÀI_KHOẢN_DNSE"
client.login(user_name, password)
```

Sau bước này, mã JWT token được tạo ra để sử dụng trong các bước tiếp theo.

### Xác thực giao dịch

Xác thực cấp 2 với OTP

Để thực hiện các thao tác liên quan đến giao dịch hoặc thay đổi thông tin trên tài khoản DNSE, bạn cần sử dụng mã OTP để thực hiện xác thực cấp 2. Mã OTP có thể là mã SmartOTP lấy từ app EntradeX trên smartphone hoặc mã được gửi qua email. Sau khi thực hiện bước xác thực OTP với hệ thống, một mã `trading token` được tạo ra và có hiệu lực trong 8 tiếng cho phép bạn thực hiện các bước giao dịch trong suốt ngày làm việc.

Khi nào sử dụng SmartOTP, emailOTP?

- SmartOTP là phương thức xác thực mặc định khi bạn mở tài khoản DNSE, có thể sử dụng để thực hiện toàn bộ nhu cầu giao dịch của bạn.
- emailOTP được các nhà đầu tư lựa chọn khi muốn xây dựng bot giao dịch tự động hoàn toàn. Khi đó, bạn sử dụng một email chuyên biệt (khuyên dùng Gmail) đăng ký với DNSE để nhận OTP, trích xuất OTP với API từ Google và xác thực hệ thống DNSE hoàn toàn tự động. Lưu ý nhỏ là mã OTP gửi qua email chỉ tồn tại trong 2 phút.

#### Yêu cầu hệ thống gửi OTP qua email

Bỏ qua bước này nếu bạn chọn sử dụng SmartOTP thay vì email OTP. Dòng lệnh sau giúp bạn yêu cầu hệ thống gửi OTP qua email, mã OTP này dùng để tạo `trading token` cho phép thực hiện giao dịch.

Python

```python
client.email_otp()
```

Sau khi nhận mã OTP qua email, bạn sử dụng cho bước tiếp theo. Bạn cũng có thể tự động hóa quá trình trích xuất OTP này và nạp cho bước tiếp theo bằng cách sử dụng Gmail API. Tham khảo thêm thông tin [tại đây](https://developers.google.com/gmail/api/guides?hl=vi)

#### Tạo mã trading token để giao dịch

Tại bước này, bạn có thể nhập mã OTP để `tạo trading token` bằng mã SmartOTP hoặc email OTP.

Python

```python
trading_token = client.get_trading_token(otp = 'MÃ_OTP_CỦA_BẠN', smart_otp=True)
```

Trong đó:

- `otp` là mã xác thực cấp 2 lấy từ app EntradeX dưới dạng SmartOTP hoặc mã được gửi qua email. Mã này phải được nhập dưới dạng string `'12345'`.
- `smart_otp`: nhận giá trị `True` nếu bạn lấy mã từ app, `False` nếu lấy mã từ email

## Tra cứu thông tin

Tra cứu thông tin với tên đăng nhập và mật khẩu tài khoản

Để sử dụng các hàm tra cứu thông tin, bạn chỉ cần thực hiện xác thực cấp 1 với tên đăng nhập và mật khẩu tài khoản.

### Thông tin tài khoản

Để truy cập thông tin tài khoản của bạn tại DNSE, bạn sử dụng câu lệnh sau:

Python

```python
client.account()
```

Kết quả trả về có dạng:

Shell

```bash
>>> client.account()
id                                                                0123456789
investorId                                                        0123456789
name                                                            	Vũ Thịnh
custodyCode                                                        064C12345
email                                                   support@vnstocks.com
unverifiedEmail                                         support@vnstocks.com
mobile                                                            0123456789
status                                                                ACTIVE
createdDate                                         2023-01-01T00:00:00.007Z
modifiedDate                                        2023-01-01T00:00:00.007Z
enId                                        xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx
identificationCode                                          0123456789010101
identificationDate                                      2021-01-01T00:00:00Z
identificationExpiredDate                               2100-01-01T00:00:00Z
identificationPlace                                      Cục CS QLHC về TTXH
birthday                                                XXXX-XX-XXT00:00:00Z
address                                   vnstock chào đón các nhà đầu tư 😁
gender                                                                  MALE
flexCustomerId                                                    000000000
smartOtpRegistrationId                                               xxxxx
userApproveType                                                AUTO_APPROVED
referralCode                                                          xxxxxx
referralUrl                                         https://s.dnse.vn/xxxxxx
avatarUrl                           https://lh3.googleusercontent.com/xyzxyz
needToChangePassword                                                   True
registeredSmartOtp                                                     False
isEmailVerified                                                        False
```

### Thông tin tiểu khoản

Tiểu khoản

Mỗi một tài khoản mở tại DNSE được cấu trúc thành các tiểu khoản (tài khoản con) cho phép sử dụng để giao dịch chứng khoán cơ sở hoặc phái sinh.

Để tra cứu thông tin các tiểu khoản trong tài khoản của bạn, sử dụng hàm sau:

Python

```python
client.sub_accounts()
```

### Thông tin số dư tài khoản

Cho phép tra cứu thông tin tiền số dư tiền theo mã tiểu khoản của bạn.

Python

```python
client.account_balance (sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN')
```

### Danh sách gói vay

Gói vay

Gói vay là khái niệm của DNSE định nghĩa để hỗ trợ phân biệt các tỷ lệ ký quỹ khi đặt lệnh (margin, không margin). Mã gói vay được sử dụng khi đặt lệnh (nếu có).

Python

```python
client.loan_packages(sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='stock')
```

Trong đó:

- `sub_account`: là mã tiểu khoản trên tài khoản DNSE của bạn.
- `asset_type`: nhập `stock` cho giao dịch cơ sở, `derivative` cho giao dịch phái sinh.

### Sức mua, sức bán

Lấy thông tin sức mua sức bán tối đa theo tiểu khoản, mã, giá và gói vay

Python

```python
client.trade_capacities(symbol='VIC', price=41600, sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='stock', loan_package_id=None)
```

Trong đó:

- `symbol`: là tên mã cổ phiếu hoặc mã hợp đồng phái sinh, ví dụ `VN30F2311`
- `price`: giá, đơn vị là đồng.
- `sub_account`: là mã tiểu khoản của bạn sử dụng để giao dịch, lấy từ hàm `sub_accounts`
- `asset_type`: nhận một trong hai giá trị là `stock` cho cổ phiếu hoặc `derivative` cho phái sinh.
- `loan_package_id`: mã gói vay, lấy từ danh sách gói vay áp dụng với tài khoản của bạn.

## Đặt lệnh, sửa lệnh, hủy lệnh

### Đặt lệnh

Python

```python
sub_account = "MÃ_TIỂU_KHOẢN_CỦA_BẠN"
symbol = "VIC"
side = "buy"
quantity = 100
price = 41600
order_type = 'LO'
loan_package_id = None  # Thay thế với mã gói vay thực tế của bạn
asset_type = 'stock'

client.place_order(account, symbol, side, quantity, price, order_type, loan_package_id, asset_type)
```

hoặc sử dụng dạng rút gọn

Python

```python
client.place_order('MÃ_TIỂU_KHOẢN_CỦA_BẠN', 'VIC', 'buy', 500, 41600, 'LO', None, 'stock')
```

Trong đó:

- `sub_account`: là mã tiểu khoản của bạn sử dụng để giao dịch, lấy từ hàm `sub_accounts`
- `symbol`: là tên mã cổ phiếu hoặc mã hợp đồng phái sinh, ví dụ `VN30F2311`
- `side`: loại lệnh mua `buy` hay bán `sell`
- `quantity`: số lượng hợp đồng, cổ phiếu giao dịch
- `price`: giá, đơn vị là đồng.
- `order_type`: Loại lệnh, sử dụng 1 trong các giá trị `LO`, `MP`, `MTL`, `ATO`, `ATC`, `MOK`, `MAK`
- `loan_package_id`: mã gói vay, lấy từ danh sách gói vay áp dụng với tài khoản của bạn.
- `asset_type`: nhận một trong hai giá trị là `stock` cho cổ phiếu hoặc `derivative` cho phái sinh.

### Sổ lệnh

Cho phép liệt kê các lệnh đã đặt trong sổ lệnh. Áp dụng cho cả giao dịch cơ sở và phái sinh.

Để liệt kê danh sách lệnh trong sổ lệnh, bạn sử dụng dòng lệnh sau đối với giao dịch cơ sở

Python

```python
client.order_list(sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='stock')
```

hoặc sử dụng lệnh sau cho phái sinh

Python

```python
client.order_list(sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='derivative')
```

Trong đó:

- `sub_account`: là mã tiểu khoản tương ứng cho giao dịch cơ sở/phái sinh cần tra cứu
- `asset_type`: nhận giá trị là `stock` cho giao dịch cơ sở, và `derivative` cho giao dịch phái sinh.

### Chi tiết lệnh

Tra cứu thông tin chi tiết của một lệnh bất kỳ thuộc mã tiểu khoản của bạn. Áp dụng cho cả giao dịch cơ sở và phái sinh.

Python

```python
client.order_detail(order_id='MÃ_LỆNH_CỦA_BẠN', sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='stock')
```

Trong đó:

- `order_id`: mã lệnh đặt, thông tin lấy từ `Sổ lệnh`
- `sub_account`: là mã tiểu khoản của bạn sử dụng để giao dịch, lấy từ hàm `sub_accounts`
- `asset_type`: nhận một trong hai giá trị là `stock` cho cổ phiếu hoặc `derivative` cho phái sinh.

### Hủy lệnh

Cho phép hủy lệnh bất kỳ theo id từ một tiểu khoản của bạn. Áp dụng cho cả giao dịch cơ sở và phái sinh.

Python

```python
client.cancel_order (order_id='MÃ_LỆNH_CỦA_BẠN', sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='stock')
```

Trong đó:

- `order_id`: mã lệnh đặt, thông tin lấy từ `Sổ lệnh`
- `sub_account`: là mã tiểu khoản của bạn sử dụng để giao dịch, lấy từ hàm `sub_accounts`
- `asset_type`: nhận một trong hai giá trị là `stock` cho cổ phiếu hoặc `derivative` cho phái sinh.

### Deal nắm giữ

Trả về danh sách các deal bạn đang nắm giữ. Áp dụng cho cả giao dịch cơ sở và phái sinh.

Python

```python
client.deals_list (sub_account='MÃ_TIỂU_KHOẢN_CỦA_BẠN', asset_type='stock')
```

Trong đó:

- `sub_account`: là mã tiểu khoản của bạn sử dụng để giao dịch, lấy từ hàm `sub_accounts`
- `asset_type`: nhận một trong hai giá trị là `stock` cho cổ phiếu hoặc `derivative` cho phái sinh.

#### Tags

[api giao dịch](https://vnstocks.com/blog/tag/api-giao-dich) [bot phái sinh](https://vnstocks.com/blog/tag/bot-phai-sinh) [dnse api](https://vnstocks.com/blog/tag/dnse-api)

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập