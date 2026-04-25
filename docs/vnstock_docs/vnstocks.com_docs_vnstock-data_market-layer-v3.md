---
url: "https://vnstocks.com/docs/vnstock-data/market-layer-v3"
title: "Dữ Liệu Giao Dịch | Vnstock"
---

## Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock-agent-guide/blob/main/notebooks/01_unified_ui/02_Market.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Tổng quan

**Market Layer** cung cấp dữ liệu **realtime & lịch sử** về giá, khối lượng, vốn hóa, thanh khoản ngay từ các sàn giao dịch và nhà cung cấp dữ liệu. Đây là dữ liệu **thay đổi liên tục** và phục vụ cho trading, phân tích kỹ thuật, và theo dõi danh mục.

## Khởi tạo

Python

```python
from vnstock_data import Market
mkt = Market()
```

## Cấu trúc Domain

```
Market()
├── .equity(symbol)        # Thị trường cổ phiếu
├── .index(symbol)         # Thị trường chỉ số
├── .futures(symbol)       # Hợp đồng tương lai
├── .warrant(symbol)       # Chứng quyền
├── .etf(symbol)           # Quỹ ETF
├── .fund(symbol)          # Quỹ đầu tư mở
├── .crypto(symbol)        # Tiền mã hoá (thử nghiệm)
├── .forex(symbol)         # Ngoại hối (thử nghiệm)
├── .commodity(symbol)     # Hàng hoá quốc tế (thử nghiệm)
└── .quote(symbols_list)   # Bảng giá nhiều mã
```

## Hướng dẫn chi tiết

### 1\. Thị trường cổ phiếu

Domain cốt lõi của Market Layer, cung cấp đầy đủ dữ liệu giao dịch cho mọi mã cổ phiếu niêm yết.

| Phương thức | Mô tả |
| --- | --- |
| `ohlcv()` | Giá OHLCV lịch sử |
| `trades()` | Lệnh giao dịch chi tiết (Time & Sales) |
| `order_book()` | Cấp độ mua/bán |
| `quote()` | Giá hiện tại / Bảng giá |
| `session_stats()` | Thống kê phiên giao dịch |
| `foreign_flow()` | Dòng tiền nước ngoài |
| `proprietary_flow()` | Dòng tiền tự doanh |
| `block_trades()` | Giao dịch thỏa thuận |
| `odd_lot()` | Giao dịch lô lẻ |
| `volume_profile()` | Phân bố khối lượng theo giá |
| `summary()` | Tổng hợp thông tin cổ phiếu |

Python

```python
from vnstock_data import Market

mkt = Market()

# Giá OHLCV lịch sử
df_ohlc = mkt.equity("VIC") \
              .ohlcv(start="2026-02-01", end="2026-03-01")

# Lệnh giao dịch chi tiết trong ngày
df_trades = mkt.equity("TCB").trades()

# Cấp độ mua/bán
df_orderbook = mkt.equity("VNM").order_book()

# Bảng giá
quote = mkt.equity("HPG").quote()

# Dòng tiền nước ngoài
foreign = mkt.equity("VIC").foreign_flow()

# Dòng tiền tự doanh
proprietary = mkt.equity("VIC").proprietary_flow()

# Giao dịch thỏa thuận
blocks = mkt.equity("VIC").block_trades()

# Giao dịch lô lẻ
odd = mkt.equity("HPG").odd_lot()

# Phân bố khối lượng theo giá
vol_profile = mkt.equity("VJC").volume_profile()

# Tổng hợp thông tin
summary = mkt.equity("TCB").summary()
```

* * *

### 2\. Thị trường chỉ số

Theo dõi diễn biến của các chỉ số thị trường: VNINDEX, HNX, VN30, v.v.

| Phương thức | Mô tả |
| --- | --- |
| `ohlcv()` | Điểm chỉ số lịch sử |
| `quote()` | Điểm chỉ số hiện tại |
| `summary()` | Tổng hợp chỉ số |

Python

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử điểm VNIndex
df_vnindex = mkt.index("VNINDEX") \
                .ohlcv(start="2026-01-01", end="2026-03-01")

# Điểm hiện tại
quote_index = mkt.index("VNINDEX").quote()
```

* * *

### 3\. Hợp đồng tương lai

Dữ liệu giao dịch cho thị trường phái sinh — hỗ trợ OHLCV, bảng giá, lệnh khớp và sổ lệnh.

| Phương thức | Mô tả |
| --- | --- |
| `ohlcv()` | Giá hợp đồng lịch sử |
| `quote()` | Giá hiện tại |
| `trades()` | Giao dịch chi tiết |
| `order_book()` | Cấp độ mua/bán |
| `summary()` | Thông tin hợp đồng |

Python

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử giá VN30F
df_vn30f = mkt.futures("VN30F2503") \
               .ohlcv(start="2026-02-01", end="2026-03-01")

# Giá hiện tại
quote_vn30f = mkt.futures("VN30F2503").quote()

# Lệnh giao dịch chi tiết
trades = mkt.futures("VN30F2503").trades()
```

* * *

### 4\. Chứng quyền

Dữ liệu giao dịch cho thị trường chứng quyền có bảo đảm.

| Phương thức | Mô tả |
| --- | --- |
| `ohlcv()` | Giá chứng quyền lịch sử |
| `quote()` | Giá hiện tại |
| `trades()` | Giao dịch chi tiết |
| `order_book()` | Cấp độ mua/bán |
| `summary()` | Thông tin chứng quyền |

Python

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử giá chứng quyền
df_warrant = mkt.warrant("CACB2511") \
                 .ohlcv(start="2026-02-01", end="2026-03-01")

# Giá hiện tại
quote = mkt.warrant("CACB2511").quote()
```

* * *

### 5\. Quỹ ETF

Dữ liệu giao dịch cho các quỹ ETF — hỗ trợ giống Equity Market (đầy đủ OHLCV, dòng tiền, bảng giá, v.v.).

Python

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử giá ETF
df_etf = mkt.etf("E1VFVN30") \
             .ohlcv(start="2026-02-01", end="2026-03-01")

# Giá hiện tại
quote_etf = mkt.etf("E1VFVN30").quote()

# Dòng tiền nước ngoài trên ETF
foreign = mkt.etf("E1VFVN30").foreign_flow()
```

* * *

### 6\. Quỹ đầu tư mở

Theo dõi lịch sử NAV và danh mục nắm giữ của các quỹ mở.

| Phương thức | Mô tả |
| --- | --- |
| `history()` | Lịch sử NAV quỹ |
| `top_holding()` | Top cổ phiếu nắm giữ |
| `industry_holding()` | Nắm giữ theo ngành |
| `asset_holding()` | Nắm giữ theo loại tài sản |

Python

```python
from vnstock_data import Market

mkt = Market()

# Lịch sử NAV quỹ
df_nav = mkt.fund("VFIBS").history()

# Top cổ phiếu trong quỹ
top_holding = mkt.fund("VFIBS").top_holding()

# Nắm giữ theo ngành
industry = mkt.fund("VFIBS").industry_holding()

# Nắm giữ theo loại tài sản
asset = mkt.fund("VFIBS").asset_holding()
```

* * *

### 7\. Bảng giá nhiều mã

Lấy bảng giá cho nhiều mã cổ phiếu cùng lúc — hiệu quả hơn rất nhiều so với gọi từng mã.

Python

```python
from vnstock_data import Market

mkt = Market()

# Bảng giá nhiều mã cùng lúc
df_quotes = mkt.quote(["VIC", "TCB", "HPG", "VNM"])
```

Mẹo về hiệu suất

Luôn sử dụng `mkt.quote(list)` khi cần lấy giá nhiều mã thay vì lặp `mkt.equity(symbol).quote()` từng mã một. Giảm đáng kể số request gửi đi.

* * *

### 8\. Thị trường quốc tế (thử nghiệm)

Các domain sau đang trong giai đoạn thử nghiệm — chỉ hỗ trợ `ohlcv()` cho dữ liệu lịch sử thông qua nguồn MSN.

Python

```python
from vnstock_data import Market

mkt = Market()

# Crypto — Bitcoin
df_btc = mkt.crypto("BTC") \
             .ohlcv(start="2026-01-01", end="2026-03-01")

# Forex — cặp tiền tệ
df_fx = mkt.forex("USDVND") \
            .ohlcv(start="2026-01-01", end="2026-03-01")

# Commodity — vàng
df_gold = mkt.commodity("GC=F") \
              .ohlcv(start="2026-01-01", end="2026-03-01")
```

Lưu ý quan trọng

Dùng `Reference().search.symbol("tên_tài_sản")` để tìm đúng mã symbol cho các thị trường quốc tế. Các domain này chưa ổn định và có thể thay đổi.

### Thảo luận

Đang tải bình luận...