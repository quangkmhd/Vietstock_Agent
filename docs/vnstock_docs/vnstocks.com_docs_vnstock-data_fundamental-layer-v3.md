---
url: "https://vnstocks.com/docs/vnstock-data/fundamental-layer-v3"
title: "Dữ Liệu Cơ Bản | Vnstock"
---

Toggle Sidebar

### Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock-agent-guide/blob/main/notebooks/01_unified_ui/03_Fundamental.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Tổng quan

`Fundamental` cung cấp dữ liệu báo cáo tài chính và chỉ số tài chính được tổng hợp, chuẩn hoá từ các nguồn công khai — phục vụ cho phân tích cơ bản doanh nghiệp. Thư viện `vnstock_data` đóng vai trò kết nối API, chuẩn hoá dữ liệu và cung cấp trải nghiệm người dùng thân thiện, dễ dàng tích hợp với AI nhờ tài liệu chuẩn mực.

## Khởi tạo

Python

```python
from vnstock_data import Fundamental
fun = Fundamental()
```

## Cấu trúc Domain

```
Fundamental()
└── .equity()
    ├── .income_statement()    # Báo cáo kết quả kinh doanh
    ├── .balance_sheet()       # Bảng cân đối kế toán
    ├── .cash_flow()           # Báo cáo lưu chuyển tiền tệ
    ├── .ratio()               # Chỉ số tài chính
    └── .note()                # Thuyết minh BCTC
```

### Tra cứu nhanh

Python

```python
from vnstock_data import show_api, Fundamental
show_api(Fundamental())
```

**Hiển thị kết quả API Tree**

Text

```plaintext
API STRUCTURE TREE
└── Fundamental
    └── equity() # Access financial data for a specific corporate equity (Fundamental Layer).
        ├── balance_sheet() [KBS] -> DataFrame # Extracts Balance Sheet.
        ├── cash_flow() [KBS] -> DataFrame # Extracts Cash Flow statement.
        ├── income_statement() [KBS] -> DataFrame # Extracts Income Statement.
        ├── note() [VCI] -> DataFrame # Extracts notes (Thuyết minh Báo cáo tài chính).
        ├── ratio() [KBS] -> DataFrame # Extracts key financial ratios (P/E, ROE, Debt/Equity, etc.).

Tip: Sử dụng show_doc(node) để đọc docstring.
[Navigation] = Intermediate methods returning domain objects
```

## Hướng dẫn chi tiết

### 1\. Báo cáo kết quả kinh doanh

Doanh thu, chi phí, lợi nhuận gộp, lợi nhuận ròng, EPS — theo **quý (Q)** hoặc **năm (Y)**.

Python

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Báo cáo thu nhập quý
df_income_q = fun.equity.income_statement("TCB", period="Q")

# Báo cáo thu nhập năm
df_income_y = fun.equity.income_statement("HPG", period="Y")
```

* * *

### 2\. Bảng cân đối kế toán

Tài sản, nợ phải trả, vốn chủ sở hữu — theo **quý (Q)** hoặc **năm (Y)**.

Python

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Cân đối kế toán quý
df_bs_q = fun.equity.balance_sheet("TCB", period="Q")

# Cân đối kế toán năm
df_bs_y = fun.equity.balance_sheet("VIC", period="Y")

# Phân tích xu hướng tài sản
assets_trend = fun.equity.balance_sheet("HPG", period="Y")
```

**Các cột dữ liệu trả về**`date`, `total_assets`, `current_assets`, `fixed_assets`, `total_liabilities`, `current_liabilities`, `long_term_liabilities`, `equity`

* * *

### 3\. Báo cáo lưu chuyển tiền tệ

Dòng tiền từ hoạt động kinh doanh, đầu tư, và tài chính — theo **quý (Q)** hoặc **năm (Y)**.

Python

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Lưu chuyển tiền tệ quý
df_cf_q = fun.equity.cash_flow("TCB", period="Q")

# Lưu chuyển tiền tệ năm
df_cf_y = fun.equity.cash_flow("VNM", period="Y")

# Kiểm tra sức khỏe dòng tiền
cf_health = fun.equity.cash_flow("VIC", period="Y")
```

**Các cột dữ liệu trả về**`date`, `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, `free_cash_flow`

* * *

### 4\. Chỉ số tài chính

Các chỉ số tài chính quan trọng: P/E, P/B, ROE, ROA, Debt/Equity, Current Ratio, v.v.

Python

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Tỷ số tài chính
df_ratio = fun.equity.ratio("TCB")
```

**Các cột dữ liệu trả về**`date`, `pe_ratio`, `pb_ratio`, `eps`, `roa`, `roe`, `debt_to_equity`, `current_ratio`, `quick_ratio`, `profit_margin`, `return_on_assets`, `return_on_equity`

* * *

### 5\. Thuyết minh BCTC

Dữ liệu thuyết minh chi tiết đi kèm báo cáo tài chính.

Python

```python
from vnstock_data import Fundamental

fun = Fundamental()

# Thuyết minh BCTC
df_note = fun.equity.note("TCB")
```

* * *

### 6\. Phân tích tài chính kết hợp

Kết hợp nhiều nguồn dữ liệu để đánh giá toàn diện một cổ phiếu.

Python

```python
from vnstock_data import Fundamental, Market

fun = Fundamental()
mkt = Market()
symbol = "TCB"

# Lấy dữ liệu tài chính
income = fun.equity.income_statement(symbol, period="Y")
balance = fun.equity.balance_sheet(symbol, period="Y")
ratio = fun.equity.ratio(symbol)

# Lấy giá hiện tại
quote = mkt.equity(symbol).quote()

# Tính toán các chỉ số
recent_ratio = ratio.iloc[-1]
recent_income = income.iloc[-1]

print(f"Stock: {symbol}")
print(f"Current Price: {quote['close'].values[0]:.0f}")
print(f"PE Ratio: {recent_ratio['pe_ratio']:.1f}")
print(f"PB Ratio: {recent_ratio['pb_ratio']:.2f}")
print(f"ROE: {recent_ratio['roe']:.1f}%")
print(f"Annual Revenue: {recent_income['revenue']:,.0f}")
print(f"Net Profit: {recent_income['net_profit']:,.0f}")
```

Mẹo phân tích

Kết hợp `Market` để lấy giá hiện tại và `Fundamental` để lấy EPS, từ đó tự tính hoặc kiểm chứng lại P/E realtime.

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập