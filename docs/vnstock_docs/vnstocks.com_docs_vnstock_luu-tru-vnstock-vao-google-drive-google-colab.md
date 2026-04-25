---
url: "https://vnstocks.com/docs/vnstock/luu-tru-vnstock-vao-google-drive-google-colab"
title: "Lưu Trữ Vnstock Vào Google Drive Để Sử Dụng Trong Google Colab | Vnstock"
---

## Mục lục

## Tổng Quan

Khi làm việc với Google Colab, bạn có thể đã gặp tình huống phiền toái: mỗi lần mở phiên làm việc mới, toàn bộ môi trường sẽ được đặt lại từ đầu, buộc bạn phải cài đặt lại tất cả thư viện như Vnstock. Điều này không chỉ tốn thời gian mà còn làm mất đi dữ liệu phân tích quý báu.

Giải Pháp Vnstock

**🚀 Khởi động tức thì:** Sau khi thiết lập, mỗi phiên mới chỉ mất vài giây để sẵn sàng thay vì 5-10 phút cài đặt lại.

**💾 Bảo toàn dữ liệu:** Tất cả cài đặt và kết quả phân tích được lưu trữ an toàn trên Google Drive.

**⚡ Tăng năng suất:** Tập trung vào phân tích thay vì cài đặt môi trường lặp lại.

## Các Bước Thực Hiện

### 1\. Chuẩn Bị

- Mở Google Colab và đăng nhập tài khoản Google
- Tạo notebook mới hoặc mở notebook hiện có

### 2\. Kết Nối Google Drive

Python

```python
from google.colab import drive
drive.mount('/content/drive')
```

### 3\. Cài Đặt Vnstock Lần Đầu (Một Lần Duy Nhất)

Python

```python
# Cài đặt vào thư mục persistent trên Drive
!pip install --target=/content/drive/MyDrive/.venv vnstock

# Thêm đường dẫn để có thể import
import sys
sys.path.insert(0, '/content/drive/MyDrive/.venv')

# Kiểm tra cài đặt
import vnstock
print("Vnstock đã sẵn sàng!")
```

### 4\. Khởi Tạo Môi Trường Vnstock

Python

```python
# Sau khi cài đặt xong, sử dụng hàm khởi tạo
from vnstock.core.config.ggcolab import initialize_colab_environment
initialize_colab_environment()
```

### 5\. Sử Dụng Các Phiên Sau

**Bước 5.1: Kết nối Google Drive**

Python

```python
# Mount Drive để truy cập thư viện đã cài đặt
from google.colab import drive
drive.mount('/content/drive')
```

**Bước 5.2: Thêm đường dẫn và sử dụng Vnstock**

Python

```python
# Sau khi Drive đã mount thành công, thêm đường dẫn thư viện
import sys
sys.path.insert(0, '/content/drive/MyDrive/.venv')

# Sử dụng Vnstock bình thường
import vnstock
from vnstock import Listing

listing = Listing()
symbols = listing.all_symbols()
print(symbols.head())
```

#### Tags

[google colab](https://vnstocks.com/blog/tag/google-colab) [persistent storage](https://vnstocks.com/blog/tag/persistent-storage) [môi trường ảo](https://vnstocks.com/blog/tag/moi-truong-ao)

### Thảo luận

Đang tải bình luận...