---
url: "https://vnstocks.com/docs/vnstock-pipeline/ket-noi-du-lieu-realtime"
title: "Kết nối dữ liệu realtime | Vnstock"
---

Toggle Sidebar

### Mục lục

## Giới thiệu

Vnstock Pipeline cung cấp khả năng kết nối và thu thập dữ liệu thị trường chứng khoán theo thời gian thực thông qua giao thức [WebSocket](https://vnstocks.com/blog/websocket-la-gi-giao-thuc-truyen-tai-du-lieu-chung-khoan). Tính năng này được thiết kế để đáp ứng nhu cầu theo dõi và phân tích dữ liệu thị trường một cách liên tục và tự động.

### Tính năng chính

- **Kết nối thời gian thực**: Nhận dữ liệu thị trường ngay lập tức qua WebSocket
- **Quản lý phiên tự động**: Tự động kết nối/ngắt kết nối theo lịch giao dịch
- **Lưu trữ đa định dạng**: Hỗ trợ lưu trữ dưới định dạng CSV và DuckDB
- **Tùy chỉnh linh hoạt**: Cho phép cấu hình thư mục lưu trữ và bộ lọc dữ liệu
- **Xử lý lỗi thông minh**: Tự động phục hồi kết nối và ghi log chi tiết

## Yêu cầu hệ thống

- Python 3.10, 3.11
- Gói tài trợ Golden của vnstock
- Kết nối internet ổn định

Tính năng kết nối dữ liệu realtime chỉ dành cho người dùng gói tài trợ Golden. Vui lòng tham khảo [hướng dẫn tài trợ](https://vnstocks.com/insiders-program#tiers) để biết thêm chi tiết.

## Sử dụng cơ bản

### Khởi chạy với cấu hình mặc định

**Unix/Linux/Mac:**

Shell

```bash
python3 wss_streaming.py
```

**Windows:**

CMD

```cmd
python wss_streaming.py
```

Với cấu hình mặc định, ứng dụng sẽ:

- Lưu dữ liệu vào thư mục `data/` (tự động tạo nếu chưa tồn tại)
- Thu thập tất cả các loại dữ liệu có sẵn
- Xuất dữ liệu dưới hai định dạng: CSV (theo loại dữ liệu) và DuckDB

### Tùy chỉnh thư mục lưu trữ

Sử dụng tham số `--data-path` để chỉ định thư mục lưu trữ tùy chỉnh:

**Unix/Linux/Mac:**

Shell

```bash
# Sử dụng đường dẫn tương đối
python3 job_examples/wss_streaming.py --data-path custom_data

# Sử dụng đường dẫn tuyệt đối
python3 job_examples/wss_streaming.py --data-path /home/user/market_data

# Sử dụng đường dẫn có khoảng trắng
python3 job_examples/wss_streaming.py --data-path "/home/user/My Market Data"
```

**Windows:**

CMD

```cmd
# Sử dụng đường dẫn tương đối
python job_examples/wss_streaming.py --data-path custom_data

# Sử dụng đường dẫn tuyệt đối
python job_examples/wss_streaming.py --data-path "C:\MarketData\Today"

# Sử dụng đường dẫn có khoảng trắng
python job_examples/wss_streaming.py --data-path "C:\My Market Data\Today"
```

Lưu ý đa nền tảng

- Hệ thống sẽ tự động tạo thư mục nếu chưa tồn tại
- Sử dụng dấu ngoặc kép cho đường dẫn có chứa khoảng trắng
- Có thể sử dụng cả đường dẫn tương đối và tuyệt đối
- **Unix/Linux/Mac**: Sử dụng `python3`, đường dẫn phân cách bởi `/`
- **Windows**: Sử dụng `python`, đường dẫn phân cách bởi `\` và cần dấu ngoặc kép

### Lọc dữ liệu theo loại

Để tối ưu hóa tài nguyên và tập trung vào các loại dữ liệu cần thiết, sử dụng tham số `--data-types`:

**Unix/Linux/Mac:**

Shell

```bash
# Thu thập chỉ dữ liệu giá cổ phiếu và chỉ số
python3 job_examples/wss_streaming.py --data-types stockps index

# Kết hợp với tùy chỉnh thư mục
python3 job_examples/wss_streaming.py --data-path custom_data --data-types stockps index board
```

**Windows:**

CMD

```cmd
# Thu thập chỉ dữ liệu giá cổ phiếu và chỉ số
python job_examples/wss_streaming.py --data-types stockps index

# Kết hợp với tùy chỉnh thư mục
python job_examples/wss_streaming.py --data-path custom_data --data-types stockps index board
```

#### Các loại dữ liệu có sẵn

| Loại dữ liệu | Mô tả |
| --- | --- |
| `stockps` | Dữ liệu giá cổ phiếu theo thời gian thực |
| `index` | Dữ liệu các chỉ số thị trường |
| `board` | Bảng giá tổng quan |
| `boardps` | Bảng giá chi tiết theo từng cổ phiếu |
| `aggregatemarket` | Dữ liệu tổng hợp thị trường |
| `aggregateps` | Dữ liệu tổng hợp chi tiết |
| `soddlot` | Giao dịch lô lẻ |
| `spt` | Giao dịch thỏa thuận |
| `psfsell` | Dữ liệu bán khống |
| `regs` | Thông tin quy định và thông báo |

## Cấu trúc dữ liệu đầu ra

### Định dạng CSV

Dữ liệu được tổ chức thành các tệp CSV riêng biệt theo mẫu:

```
{thư_mục_lưu_trữ}/market_data_{loại_dữ_liệu}_YYYY-MM-DD.csv
```

**Ví dụ cấu trúc thư mục:**

```
data/
├── market_data_stockps_2025-08-29.csv
├── market_data_index_2025-08-29.csv
├── market_data_board_2025-08-29.csv
└── market_data.db
```

### Cơ sở dữ liệu DuckDB

Toàn bộ dữ liệu cũng được lưu trữ trong cơ sở dữ liệu DuckDB:

**Đường dẫn:**`{thư_mục_lưu_trữ}/market_data.db`

**Cấu trúc bảng:** Mỗi loại dữ liệu tương ứng với một bảng:

- `market_data_stockps`
- `market_data_index`
- `market_data_board`
- ...

## Quản lý phiên giao dịch

### Tự động theo lịch giao dịch

Ứng dụng tích hợp `SessionManager` để đồng bộ hoạt động với lịch giao dịch chính thức:

- ✅ Tự động kết nối khi phiên giao dịch mở
- ⏸️ Tạm dừng kết nối trong giờ nghỉ trưa
- 🔄 Tự động kết nối lại sau giờ nghỉ trưa
- ❌ Ngắt kết nối khi thị trường đóng cửa

## Giám sát và xử lý sự cố

### Hệ thống log

Ứng dụng ghi log tại hai vị trí:

- **Console**: Hiển thị trạng thái thời gian thực
- **File log**: `market_data.log` lưu trữ lịch sử chi tiết

### Tắt ứng dụng an toàn

**Tất cả hệ điều hành:** Sử dụng `Ctrl+C` để dừng ứng dụng. Hệ thống sẽ thực hiện:

1. 🔌 Đóng tất cả kết nối WebSocket
2. ⏹️ Dừng SessionManager
3. 💾 Lưu và đóng các tệp CSV
4. 🗃️ Đóng kết nối cơ sở dữ liệu

### Khắc phục sự cố thường gặp

#### Không nhận được dữ liệu

**Nguyên nhân có thể:**

- Kết nối mạng không ổn định
- Thị trường đang đóng cửa
- Lỗi xác thực tài khoản

**Cách khắc phục:**

_Unix/Linux/Mac:_

Shell

```bash
# Kiểm tra kết nối
ping 8.8.8.8

# Xem log chi tiết
tail -f market_data.log
```

_Windows:_

CMD

```cmd
# Kiểm tra kết nối
ping 8.8.8.8

# Xem log chi tiết
type market_data.log
# Hoặc sử dụng PowerShell
Get-Content market_data.log -Wait
```

#### Lỗi thiếu module DuckDB

**Unix/Linux/Mac:**

Shell

```bash
pip3 install duckdb
```

**Windows:**

CMD

```cmd
pip install duckdb
```

#### Lỗi quyền truy cập thư mục

**Unix/Linux/Mac:**

Shell

```bash
# Cấp quyền đầy đủ cho thư mục
chmod 755 /path/to/data/directory

# Hoặc sử dụng đường dẫn có quyền ghi
python3 job_examples/wss_streaming.py --data-path ~/market_data
```

**Windows:**

CMD

```cmd
# Sử dụng đường dẫn có quyền ghi (thư mục Documents)
python job_examples/wss_streaming.py --data-path "%USERPROFILE%\Documents\market_data"

# Hoặc tạo thư mục trong ổ C:
# (Cần chạy Command Prompt với quyền Administrator)
mkdir C:\market_data
python job_examples/wss_streaming.py --data-path "C:\market_data"
```

#### Dữ liệu không đầy đủ

- Kiểm tra bộ lọc `--data-types` có bỏ sót loại dữ liệu cần thiết
- Xem log để xác nhận việc nhận dữ liệu từ server
- Đảm bảo tài khoản có quyền truy cập đầy đủ

Nếu gặp vấn đề liên tục, vui lòng liên hệ với nhóm hỗ trợ và cung cấp nội dung file log để được hỗ trợ tốt nhất.

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập