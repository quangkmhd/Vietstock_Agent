---
url: "https://vnstocks.com/docs/vnstock-pipeline/tuy-chinh-pipeline"
title: "Tùy chỉnh Pipeline của bạn | Vnstock"
---

Toggle Sidebar

### Mục lục

## Tùy chỉnh pipeline

vnstock\_pipeline cung cấp ba phương pháp chính để tùy chỉnh pipeline:

1. **Sử dụng template có sẵn với tham số tùy chỉnh**
2. **Mở rộng các lớp template**
3. **Tạo pipeline hoàn toàn mới**

### Sử dụng template có sẵn với tham số tùy chỉnh

Đây là cách đơn giản nhất để tùy chỉnh pipeline. Bạn chỉ cần gọi các hàm task có sẵn với các tham số phù hợp với nhu cầu của mình.

Python

```python
from vnstock_pipeline.tasks.financial import run_financial_task

# Tùy chỉnh các tham số
run_financial_task(
    tickers=["ACB", "VCB", "HPG"],
    balance_sheet_period="quarter",  # Thay đổi từ "year" sang "quarter"
    lang="en",                       # Thay đổi ngôn ngữ sang tiếng Anh
    dropna=False                     # Giữ lại các giá trị NaN
)
```

### Mở rộng các lớp template

Khi bạn cần tùy chỉnh logic xử lý dữ liệu, bạn có thể mở rộng các lớp template có sẵn.

Python

```python
from vnstock_pipeline.template.vnstock import VNFetcher, VNValidator, VNTransformer
from vnstock_pipeline.core.scheduler import Scheduler
from vnstock_pipeline.core.exporter import CSVExport, TimeSeriesExporter
import pandas as pd

# Ví dụ 1: Tùy chỉnh Fetcher với caching
class CustomIntradayFetcher(VNFetcher):
    def _vn_call(self, ticker: str, **kwargs) -> pd.DataFrame:
        # Tùy chỉnh cách lấy dữ liệu
        # Ví dụ: thêm caching, thay đổi tham số, v.v.
        page_size = kwargs.get("page_size", 100000)  # Tăng page_size
        stock = Vnstock().stock(symbol=ticker, source="VCI")
        return stock.quote.intraday(page_size=page_size)

# Ví dụ 2: Tùy chỉnh Transformer thêm tính toán
class CustomIntradayTransformer(VNTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        # Gọi phương thức transform của lớp cha
        df = super().transform(data)

        # Thêm xử lý tùy chỉnh
        if "price" in df.columns:
            df["price_change"] = df["price"].diff()
            df["price_pct_change"] = df["price"].pct_change() * 100

        return df

# Sử dụng các lớp tùy chỉnh
fetcher = CustomIntradayFetcher()
validator = VNValidator()  # Sử dụng validator mặc định
transformer = CustomIntradayTransformer()

# Có thể dùng CSVExport, TimeSeriesExporter, hay custom exporter
exporter = TimeSeriesExporter(base_path="./data/custom_intraday")

# Tạo scheduler và chạy
scheduler = Scheduler(fetcher, validator, transformer, exporter)
scheduler.run(["ACB", "VCB", "HPG"])
```

### Tạo custom exporter

Bạn có thể tạo exporter riêng bằng cách kế thừa từ `Exporter` base class:

Python

```python
from vnstock_pipeline.core.exporter import Exporter
import pandas as pd
from pathlib import Path
import json

class JSONExporter(Exporter):
    """Custom exporter để lưu dữ liệu dưới dạng JSON"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def export(self, data: pd.DataFrame, ticker: str, **kwargs):
        """Export DataFrame to JSON"""
        if data is None or data.empty:
            return None

        file_path = self.base_path / f"{ticker}.json"

        # Convert to JSON format
        data_dict = data.to_dict(orient='records')

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=2, default=str)

        return file_path

    def preview(self, ticker: str, n: int = 5, **kwargs):
        """Preview JSON data"""
        file_path = self.base_path / f"{ticker}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)

        # Return as DataFrame (preview)
        return pd.DataFrame(data_dict[-n:]) if isinstance(data_dict, list) else None

# Sử dụng custom exporter
json_exporter = JSONExporter("./data/json_export")

# Integrate vào pipeline
scheduler = Scheduler(fetcher, validator, transformer, json_exporter)
scheduler.run(["ACB", "VCB"])
```

### Tạo pipeline hoàn toàn mới

Khi bạn cần một pipeline hoàn toàn tùy chỉnh, bạn có thể triển khai trực tiếp các lớp trừu tượng trong module `core`.

Python

```python
import pandas as pd
import time
from pathlib import Path

# Tạo thư mục lưu trữ dữ liệu
DATA_DIR = Path("./data/custom_intraday")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Danh sách mã chứng khoán
TICKERS = ['ACB', 'VCB', 'HPG', 'VNM', 'VIC']

# Hàm tùy chỉnh để lấy dữ liệu
def fetch_data(ticker):
    # Triển khai logic lấy dữ liệu của bạn ở đây
    from vnstock import Vnstock
    stock = Vnstock().stock(symbol=ticker, source="VCI")
    return stock.quote.intraday()

# Hàm tùy chỉnh để xác thực dữ liệu
def validate_data(data):
    if not isinstance(data, pd.DataFrame) or data.empty:
        return False
    required_columns = ["time", "price", "volume"]
    return all(col in data.columns for col in required_columns)

# Hàm tùy chỉnh để chuyển đổi dữ liệu
def transform_data(data):
    df = data.copy()
    # Chuyển đổi thời gian
    df["time"] = pd.to_datetime(df["time"])
    # Sắp xếp theo thời gian
    df = df.sort_values("time")
    # Thêm cột giá trị giao dịch
    if "price" in df.columns and "volume" in df.columns:
        df["value"] = df["price"] * df["volume"]
    return df

# Hàm tùy chỉnh để xuất dữ liệu
def export_data(data, ticker):
    file_path = DATA_DIR / f"{ticker}.csv"
    data.to_csv(file_path, index=False)
    print(f"Đã lưu dữ liệu cho {ticker} vào {file_path}")

# Hàm chính để chạy pipeline
def run_custom_pipeline():
    for ticker in TICKERS:
        try:
            # Lấy dữ liệu
            print(f"Đang lấy dữ liệu cho {ticker}...")
            data = fetch_data(ticker)

            # Xác thực dữ liệu
            if not validate_data(data):
                print(f"Dữ liệu không hợp lệ cho {ticker}")
                continue

            # Chuyển đổi dữ liệu
            transformed_data = transform_data(data)

            # Xuất dữ liệu
            export_data(transformed_data, ticker)

        except Exception as e:
            print(f"Lỗi khi xử lý {ticker}: {e}")

if __name__ == "__main__":
    run_custom_pipeline()
```

### Thảo luận

Đang tải bình luận...

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập