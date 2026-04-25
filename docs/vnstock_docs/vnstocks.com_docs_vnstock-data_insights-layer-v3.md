---
url: "https://vnstocks.com/docs/vnstock-data/insights-layer-v3"
title: "Phân Tích Chuyên Sâu | Vnstock"
---

Toggle Sidebar

### Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock-agent-guide/blob/main/notebooks/01_unified_ui/06_Insights.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Tổng quan

**Insights Layer** cung cấp hệ thống **xếp hạng top cổ phiếu** và **bộ lọc chứng khoán** để nhà đầu tư nhận diện cơ hội và xu hướng thị trường.

## Khởi tạo

Python

```python
from vnstock_data import Insights
ins = Insights()
```

## Cấu trúc Domain

```
Insights()
├── .ranking()       # Xếp hạng top cổ phiếu
└── .screener()      # Bộ lọc chứng khoán
```

Thay đổi kiến trúc

Domain **Valuation** (định giá P/E, P/B toàn thị trường) đã được chuyển sang **Analytics Layer**. Vui lòng dùng `Analytics().valuation(index)` thay cho `Insights().valuation`.

## Hướng dẫn chi tiết

### 1\. Bảng xếp hạng

Xếp hạng top cổ phiếu theo nhiều tiêu chí: tăng/giảm giá, khối lượng, giá trị, nước ngoài mua/bán, giao dịch thỏa thuận.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `gainer()` | `index`, `limit` | Top cổ phiếu tăng giá |
| `loser()` | `index`, `limit` | Top cổ phiếu giảm giá |
| `value()` | `index`, `limit` | Top theo giá trị giao dịch |
| `volume()` | `index`, `limit` | Top theo khối lượng |
| `foreign_buy()` | `date`, `limit` | Top nước ngoài mua ròng |
| `foreign_sell()` | `date`, `limit` | Top nước ngoài bán ròng |
| `deal()` | `index`, `limit` | Top giao dịch thỏa thuận |

**Tham số:**

- `index` (str) — Chỉ số lọc: `'VNINDEX'`, `'HNX'`. Mặc định lấy toàn thị trường.
- `limit` (int) — Số lượng kết quả. Mặc định 10.
- `date` (str) — Ngày giao dịch (YYYY-MM-DD).

Python

```python
from vnstock_data import Insights

ins = Insights()

# Top cổ phiếu tăng giá toàn thị trường
df_gainers = ins.ranking().gainer()

# Top cổ phiếu tăng giá sàn HOSE — lấy 10 mã
df_gainers_vn = ins.ranking() \
                    .gainer(index="VNINDEX", limit=10)

# Top cổ phiếu giảm giá
df_losers = ins.ranking().loser()

# Top theo khối lượng
df_volume = ins.ranking().volume()

# Top nước ngoài mua ròng
df_foreign_buy = ins.ranking().foreign_buy()

# Top nước ngoài bán ròng
df_foreign_sell = ins.ranking().foreign_sell()

# Top giao dịch thỏa thuận
df_deals = ins.ranking().deal()
```

* * *

### 2\. Bộ lọc chứng khoán

Dữ liệu screener toàn thị trường với **hàng trăm chỉ tiêu tài chính**. Người dùng tự áp dụng logic lọc bằng Pandas.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `criteria()` | `lang` | Danh sách giải nghĩa tên cột (`'vi'` / `'en'`) |
| `filter()` | `limit` | Dữ liệu screener toàn thị trường |

Python

```python
from vnstock_data import Insights

ins = Insights()

# Xem danh sách tất cả tiêu chí
criteria_df = ins.screener().criteria(lang="vi")

# Lấy dữ liệu screener toàn thị trường
df_all = ins.screener().filter()
print(f"Tổng số cổ phiếu: {len(df_all)}")
print(f"Tổng số cột chỉ tiêu: {len(df_all.columns)}")

# Lọc cổ phiếu P/E < 10 VÀ ROE > 15%
cheap_good = df_all[\
    (df_all['pe'] < 10) & (df_all['roe'] > 15)\
]
print(cheap_good[['ticker', 'pe', 'roe']].head(10))
```

* * *

### 3\. Tìm cơ hội giá trị

Kết hợp ranking và screener để tìm cổ phiếu giảm giá mạnh nhưng vẫn có chất lượng tốt.

Python

```python
from vnstock_data import Insights

ins = Insights()

# Lấy danh sách cổ phiếu giảm giá mạnh
losers = ins.ranking().loser()

# Lấy dữ liệu screener toàn bộ
screener = ins.screener().filter()

# Merge tìm cơ hội
opportunity = losers.merge(
    screener,
    left_on='code',
    right_on='ticker',
    how='inner'
)
print(opportunity[['ticker', 'pe', 'roe']].head())
```

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập