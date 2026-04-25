---
url: "https://vnstocks.com/docs/vnstock-pipeline/hieu-nang-toi-uu"
title: "Hiệu năng và tối ưu hóa | Vnstock"
---

Toggle Sidebar

### Mục lục

## Hiệu năng và tối ưu hóa

### Xử lý song song

vnstock\_pipeline tự động sử dụng xử lý song song khi số lượng mã chứng khoán vượt quá ngưỡng (mặc định là 10). Điều này giúp tăng đáng kể tốc độ xử lý dữ liệu.

Python

```python
# Scheduler sẽ tự động sử dụng xử lý song song cho danh sách mã lớn
scheduler.run(tickers_list)  # Nếu len(tickers_list) > 10
```

Bạn có thể tùy chỉnh ngưỡng này khi khởi tạo Scheduler:

Python

```python
scheduler = Scheduler(
    fetcher, validator, transformer, exporter,
    parallel_threshold=5  # Sử dụng xử lý song song khi có từ 5 mã trở lên
)
```

### Cơ chế retry

Scheduler có cơ chế retry tích hợp để xử lý các lỗi tạm thời khi lấy dữ liệu.

Python

```python
# Tùy chỉnh số lần retry và thời gian chờ
scheduler = Scheduler(
    fetcher, validator, transformer, exporter,
    retry_attempts=5,           # Số lần thử lại tối đa
    backoff_factor=1.5          # Hệ số tăng thời gian chờ giữa các lần retry
)
```

### Kiểm soát giờ giao dịch

Module `utils.market_hours` giúp kiểm soát việc lấy dữ liệu theo giờ giao dịch của thị trường.

Python

```python
from vnstock_pipeline.utils.market_hours import trading_hours

# Kiểm tra trạng thái thị trường
market_status = trading_hours(market="HOSE", enable_log=True, language="vi")

if market_status["is_trading_hour"]:
    print(f"Thị trường đang mở, phiên: {market_status['trading_session']}")
    # Thực hiện lấy dữ liệu
else:
    print("Thị trường đóng cửa, dừng lấy dữ liệu")
```

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập