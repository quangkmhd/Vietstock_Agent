---
url: "https://vnstocks.com/docs/vnstock-data/macro-layer-v3"
title: "Dữ Liệu Vĩ Mô & Hàng Hóa | Vnstock"
---

Toggle Sidebar

### Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock-agent-guide/blob/main/notebooks/01_unified_ui/05_Macro.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Tổng quan

**Macro Layer** cung cấp dữ liệu kinh tế vĩ mô, tiền tệ và giá cả hàng hóa — phục vụ cho phân tích tác động của yếu tố kinh tế đến thị trường, trading danh mục hàng hóa, quản lý rủi ro tiền tệ và dự báo xu hướng kinh tế.

## Khởi tạo

Python

```python
from vnstock_data import Macro
mac = Macro()
```

## Cấu trúc Domain

```
Macro()
├── .economy()       # Dữ liệu kinh tế Việt Nam
├── .currency()      # Tỷ giá, lãi suất
└── .commodity()     # Giá hàng hóa
```

## Hướng dẫn chi tiết

### 1\. Kinh tế Việt Nam

Dữ liệu kinh tế Việt Nam theo quý/năm: GDP, CPI, FDI, xuất nhập khẩu, sản xuất công nghiệp, bán lẻ, cung tiền, dân số & lao động.

| Phương thức | Mô tả |
| --- | --- |
| `gdp()` | Tăng trưởng GDP |
| `cpi()` | Chỉ số giá tiêu dùng |
| `industry_prod()` | Sản xuất công nghiệp |
| `import_export()` | Xuất nhập khẩu |
| `retail()` | Bán lẻ |
| `fdi()` | Đầu tư trực tiếp nước ngoài |
| `money_supply()` | Cung tiền |
| `population_labor()` | Dân số & lao động |

**Tham số chung:**

- `start` — Mốc bắt đầu (VD: `"2020-01"`)
- `end` — Mốc kết thúc (VD: `"2026-03"`)
- `period` — `"quarter"` (mặc định), `"month"` hoặc `"year"`
- `length` — Số kỳ gần nhất (VD: `length=12` lấy 12 tháng gần nhất)

Python

```python
from vnstock_data import Macro

mac = Macro()

# GDP theo quý
df_gdp_q = mac.economy() \
               .gdp(start="2020-01", end="2026-03", period="quarter")

# GDP năm
df_gdp_y = mac.economy().gdp(period="year")

# CPI theo tháng — 24 tháng gần nhất
df_cpi = mac.economy().cpi(period="month", length=24)

# Sản xuất công nghiệp
df_ind = mac.economy().industry_prod(period="month", length=12)

# Xuất nhập khẩu
df_trade = mac.economy().import_export(period="month")

# Bán lẻ
df_retail = mac.economy().retail(period="month")

# FDI
df_fdi = mac.economy().fdi(period="month")

# Cung tiền
df_money = mac.economy().money_supply(period="month")

# Dân số & lao động
df_labor = mac.economy().population_labor(period="year")
```

* * *

### 2\. Tiền tệ & lãi suất

Tỷ giá hối đoái liên ngân hàng và lãi suất huy động/cho vay.

| Phương thức | Tham số riêng | Mô tả |
| --- | --- | --- |
| `exchange_rate()` | `period`, `length` | Tỷ giá hối đoái |
| `interest_rate()` | `period`, `format`, `length` | Lãi suất |

**Lưu ý:**

- `period` — `"day"` (mặc định), `"month"`, `"quarter"`
- `format` — `"pivot"` (mặc định) hoặc `"long"`

Python

```python
from vnstock_data import Macro

mac = Macro()

# Tỷ giá hàng ngày — 90 ngày gần nhất
df_exr = mac.currency() \
             .exchange_rate(period="day", length=90)

# Tỷ giá trung bình tháng — 12 tháng
df_exr_m = mac.currency() \
               .exchange_rate(period="month", length=12)

# Lãi suất hàng ngày — 1 năm gần nhất
df_ir = mac.currency() \
            .interest_rate(period="day", length=365)

# Lãi suất định dạng long (dễ vẽ biểu đồ)
df_ir_long = mac.currency() \
                 .interest_rate(period="month", format="long")
```

Tương thích ngược

Phương thức gọi trực tiếp như `Macro().interest_rate()` đã lỗi thời và sẽ in cảnh báo. Hãy chuyển sang `Macro().currency().interest_rate()`.

* * *

### 3\. Giá cả hàng hóa

Giá hàng hóa trong nước và quốc tế: vàng, dầu, thép, nông sản, thực phẩm.

| Phương thức | Tham số `market` | Mô tả |
| --- | --- | --- |
| `gold()` | `"VN"` / `"GLOBAL"` | Giá vàng |
| `gas()` | `"VN"` / `"GLOBAL"` | Giá xăng dầu / khí |
| `oil_crude()` | — | Giá dầu thô WTI & Brent |
| `coke()` | — | Giá than cốc |
| `steel()` | `"VN"` / `"GLOBAL"` | Giá thép |
| `iron_ore()` | — | Giá quặng sắt |
| `fertilizer_ure()` | — | Giá phân URE |
| `soybean()` | — | Giá đậu tương |
| `corn()` | — | Giá ngô |
| `sugar()` | — | Giá đường |
| `pork()` | `"VN"` / `"CHINA"` | Giá thịt lợn hơi |

Python

```python
from vnstock_data import Macro

mac = Macro()

# Giá vàng SJC trong nước
df_gold_vn = mac.commodity().gold(market="VN")

# Giá vàng quốc tế
df_gold_global = mac.commodity().gold(market="GLOBAL")

# Giá dầu thô WTI & Brent
df_oil = mac.commodity().oil_crude()

# Giá thép HRC quốc tế
df_steel = mac.commodity().steel(market="GLOBAL")

# Giá xăng lẻ trong nước
df_gas_vn = mac.commodity().gas(market="VN")

# Nông sản quốc tế
df_soy = mac.commodity().soybean()
df_corn = mac.commodity().corn()
df_sugar = mac.commodity().sugar()

# Giá thịt lợn hơi Việt Nam
df_pork = mac.commodity().pork(market="VN")
```

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập