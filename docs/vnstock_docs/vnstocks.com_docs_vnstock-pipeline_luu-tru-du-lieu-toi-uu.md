---
url: "https://vnstocks.com/docs/vnstock-pipeline/luu-tru-du-lieu-toi-uu"
title: "Lưu trữ dữ liệu tối ưu với Parquet | Vnstock"
---

Toggle Sidebar

### Mục lục

## Giới thiệu

Tính năng mới này cung cấp khả năng lưu trữ dữ liệu chứng khoán hiệu quả hơn bằng định dạng Parquet, kèm theo cấu trúc thư mục rõ ràng để dễ quản lý.

## Cấu trúc thư mục

Dữ liệu được tổ chức theo cấu trúc sau:

Shell

```bash
data/
├── intraday/           # Loại dữ liệu (vd: intraday, daily, financials)
│   ├── YYYY-MM-DD/     # Ngày dữ liệu
│   │   ├── VNM.parquet
│   │   └── FPT.parquet
│   └── YYYY-MM-DD/
│       └── VNM.parquet
└── daily/              # Một loại dữ liệu khác
    └── YYYY-MM-DD/
        └── VNM.parquet
```

## Cách sử dụng

### 1\. Sử dụng ParquetExport đơn giản

Python

```python
"""
Ví dụ đơn giản sử dụng DataManager để lưu trữ dữ liệu intraday.
"""
from vnstock_pipeline.core.data_manager import DataManager
from vnstock_pipeline.tasks.intraday import IntradayFetcher, IntradayTransformer, IntradayValidator
from pathlib import Path

# Khởi tạo data manager
data_manager = DataManager(Path("./data"))

# Khởi tạo các thành phần pipeline
fetcher = IntradayFetcher()
validator = IntradayValidator()
transformer = IntradayTransformer()

# Lấy và xử lý dữ liệu
ticker = "VNM"
print(f"Đang lấy dữ liệu intraday cho {ticker}...")

try:
    # 1. Lấy dữ liệu từ API
    raw_data = fetcher.fetch(ticker)

    # 2. Kiểm tra dữ liệu
    if validator.validate(raw_data):
        # 3. Chuyển đổi dữ liệu
        processed_data = transformer.transform(raw_data)

        if len(processed_data) > 0:
            # 4. Lưu dữ liệu
            file_path = data_manager.save_data(
                data=processed_data,
                ticker=ticker,
                data_type="intraday",
                date="2025-08-30"
            )

            print(f"✅ Đã lưu {len(processed_data)} bản ghi vào {file_path}")

            # 5. Xem trước dữ liệu
            preview = data_manager.load_data(ticker, "intraday", "2025-08-30")
            print(f"\nDữ liệu mới nhất:")
            print(preview.tail(3))
        else:
            print("Không có dữ liệu để lưu")
    else:
        print("❌ Dữ liệu không hợp lệ")

except Exception as e:
    print(f"❌ Lỗi: {str(e)}")
```

### 2\. Sử dụng DataManager để quản lý dữ liệu

Python

```python
from vnstock_pipeline.core.data_manager import DataManager
import pandas as pd

# Khởi tạo DataManager
dm = DataManager("path/to/data")

# Lưu dữ liệu
# Dữ liệu sẽ được lưu vào: path/to/data/intraday/2025-08-30/VNM.parquet
dm.save_data(
    data=data_frame,  # DataFrame chứa dữ liệu
    ticker="VNM",
    data_type="intraday",
    date="2025-08-30"  # Nếu bỏ qua, mặc định là ngày hiện tại
)

# Đọc dữ liệu
# Đọc dữ liệu 2 ngày gần nhất
data = dm.load_data(
    ticker="VNM",
    data_type="intraday",
    start_date="2025-08-29",
    end_date="2025-08-30"
)

# Liệt kê dữ liệu có sẵn
available = dm.list_available_data("intraday")
print(available)

# Xóa dữ liệu
# Xóa dữ liệu của một mã cổ phiếu trong một ngày
dm.delete_data("intraday", ticker="VNM", date="2025-08-30")

# Xóa toàn bộ dữ liệu của một loại
dm.delete_data("intraday")
```

## Lợi ích của việc sử dụng Parquet

1. **Tiết kiệm dung lượng**: Dữ liệu được nén hiệu quả, tiết kiệm tới 75% dung lượng so với CSV
2. **Tốc độ đọc/ghi nhanh**: Đọc ghi nhanh hơn nhiều so với CSV, đặc biệt với khối lượng dữ liệu lớn
3. **Hỗ trợ schema**: Tự động bảo toàn kiểu dữ liệu
4. **Hỗ trợ cắt cột**: Chỉ đọc những cột cần thiết
5. **Tương thích**: Làm việc tốt với các công cụ phân tích dữ liệu hiện đại

## Chương trình mẫu

Lưu đoạn code sau thành file `orderbook_parquet_daily.py` sau đó chạy script với Python.

Python

```python
"""
Pipeline tải dữ liệu intraday cuối ngày và lưu trữ bằng định dạng Parquet.
Chạy 1 lần vào cuối phiên giao dịch để tạo cơ sở dữ liệu.
"""
import time
from datetime import datetime, time as dtime, timedelta
from pathlib import Path

from vnstock.core.utils.market import trading_hours
from vnstock_pipeline.core.data_manager import DataManager
from vnstock_pipeline.tasks.intraday import (
    IntradayFetcher,
    IntradayTransformer,
    IntradayValidator,
)

# Cấu hình
BASE_DATA_DIR = Path("./data")
TICKERS = [\
    'ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR', 'HDB', 'HPG',\
    'LPB', 'MBB', 'MSN', 'MWG', 'PLX', 'SAB', 'SHB', 'SSB', 'SSI', 'STB',\
    'TCB', 'TPB', 'VCB', 'VHM', 'VIB', 'VIC', 'VJC', 'VNM', 'VPB', 'VRE'\
]

# Thời gian chờ giữa các lần gọi API (giây)

API_DELAY = 1

def get_current_session_date():
    """Lấy ngày hiện tại dưới dạng YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")

def process_intraday_data():
    """Xử lý và lưu trữ dữ liệu intraday."""
    # Khởi tạo các thành phần pipeline
    fetcher = IntradayFetcher()
    validator = IntradayValidator()
    transformer = IntradayTransformer()
    data_manager = DataManager(BASE_DATA_DIR)

    # Lấy ngày hiện tại
    current_date = get_current_session_date()

    print(f"\n=== Bắt đầu cập nhật dữ liệu ngày {current_date} ===")

    success_count = 0
    error_count = 0

    for i, ticker in enumerate(TICKERS, 1):
        try:
            print(f"\n[{i}/{len(TICKERS)}] Đang xử lý {ticker}...")

            # 1. Lấy dữ liệu
            df = fetcher.fetch(ticker)

            # 2. Kiểm tra dữ liệu
            if not validator.validate(df):
                print("  ⚠️  Lỗi kiểm tra dữ liệu, bỏ qua...")
                error_count += 1
                continue

            # 3. Chuyển đổi dữ liệu
            df = transformer.transform(df)

            if len(df) == 0:
                print("  ℹ️  Không có dữ liệu mới")
                continue

            # 4. Lưu dữ liệu dưới dạng Parquet
            file_path = data_manager.save_data(
                data=df,
                ticker=ticker,
                data_type="intraday",
                date=current_date
            )

            # 5. In thông báo
            last_row = df.iloc[-1]
            try:
                close_price = float(last_row.get('close', 0))
                close_str = f"{close_price:,.2f}"
            except (ValueError, TypeError):
                close_str = str(last_row.get('close', 'N/A'))

            msg = (
                f"  ✅ Đã lưu {len(df)} bản ghi vào {file_path}"
                f"\n  ⏰ Thời gian cuối: {last_row.get('time', 'N/A')}"
                f"\n  💰 Giá đóng cửa: {close_str}"
            )
            print(msg)

            success_count += 1

            # Nghỉ giữa các lần gọi API
            if i < len(TICKERS):
                time.sleep(API_DELAY)

        except Exception as e:
            error_count += 1
            print(f"  ❌ Lỗi: {str(e)}")

    # Tổng kết
    print("\n=== TỔNG KẾT ===")
    print(f"Thành công: {success_count}/{len(TICKERS)}")
    print(f"Lỗi: {error_count}/{len(TICKERS)}")
    print(f"Hoàn thành lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def wait_until_market_close():
    """
    Kiểm tra thời gian giao dịch và quyết định có cần chờ không.
    Sử dụng hàm trading_hours từ thư viện vnstock để xác định trạng thái thị trường.
    Trả về True nếu cần chạy cập nhật dữ liệu, False nếu không cần.
    """
    # Lấy thông tin giờ giao dịch từ thư viện vnstock
    market_status = trading_hours(market="HOSE", enable_log=False, language="vi")

    # Nếu là cuối tuần
    if market_status["trading_session"] == "weekend":
        print("Hôm nay là cuối tuần, không cần cập nhật dữ liệu.")
        return False

    # Nếu đang trong giờ giao dịch, chờ đến khi kết thúc
    if market_status["is_trading_hour"]:
        now = datetime.now()
        close_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        wait_seconds = (close_time - now).total_seconds()

        if wait_seconds > 0:
            wait_minutes = int(wait_seconds / 60)
            print(f"Đang trong giờ giao dịch, chờ đến 15:00 (còn {wait_minutes} phút)...")
            time.sleep(wait_seconds)

    # Ngoài giờ giao dịch, chạy ngay
    print("Ngoài giờ giao dịch, tiến hành cập nhật dữ liệu ngay...")
    return True

if __name__ == "__main__":
    print("=== CHƯƠNG TRÌNH CẬP NHẬT DỮ LIỆU INTRADAY ===")
    print(f"Theo dõi {len(TICKERS)} mã cổ phiếu")
    print("Chương trình sẽ chạy vào cuối phiên giao dịch (15:00)")
    print("Nhấn Ctrl+C để dừng chương trình\n")

    try:
        # Kiểm tra xem có cần chạy cập nhật không
        should_run = wait_until_market_close()

        if should_run:
            # Chạy cập nhật dữ liệu
            process_intraday_data()
        else:
            print("Không cần cập nhật dữ liệu vào thời điểm này.")

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
    except Exception as e:
        print(f"\nLỗi không mong muốn: {str(e)}")
```

## Mẹo sử dụng

1. **Chọn cột khi đọc**: Luôn chỉ định các cột cần thiết để tăng tốc độ đọc

Python

```python
# Chỉ đọc các cột được chọn
dm.load_data("VNM", "intraday", columns=["time", "price", "volume"])
```

2. **Lọc dữ liệu khi đọc**: Sử dụng bộ lọc để giảm lượng dữ liệu cần đọc

Python

```python
# Chỉ đọc dữ liệu có giá đóng cửa > 100
filters = [("price", "<=", 60.3), ("volume", ">", 10000)]
data = dm.load_data("VNM", "intraday", filters=filters)
```

3. **Xử lý dữ liệu lớn**: Với dữ liệu lớn, sử dụng iterator để xử lý từng phần

Python

```python
dataset = ds.dataset("path/to/data/intraday")
for batch in dataset.to_batches():
   df = batch.to_pandas()
   # Xử lý từng batch
```

## Xử lý lỗi thường gặp

1. **Lỗi thiếu thư viện**: Đảm bảo đã cài đặt đầy đủ các thư viện phụ thuộc là `pyarrow`
2. **Lỗi kiểu dữ liệu**: Kiểm tra kiểu dữ liệu trước khi lưu
3. **Quyền truy cập**: Đảm bảo có quyền ghi vào thư mục đích

## Lời kết

Tính năng mới này cung cấp một giải pháp lưu trữ dữ liệu hiệu quả và dễ sử dụng, giúp tối ưu hiệu năng và dễ dàng mở rộng cho các ứng dụng phân tích dữ liệu chứng khoán.

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập