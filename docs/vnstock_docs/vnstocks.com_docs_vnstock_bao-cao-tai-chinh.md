---
url: "https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh"
title: "Báo cáo tài chính | Vnstock"
---

Toggle Sidebar

### Mục lục

Gợi ý

Các hàm tra cứu thông tin báo cáo tài chính chỉ áp dụng với mã chứng khoán của các doanh nghiệp trong nước. Định dạng báo cáo tài chính được cung cấp đã qua xử lý, chuẩn hoá và rút gọn bởi các đơn vị cung cấp dữ liệu cho công ty chứng khoán. Để tra cứu thông tin báo cáo tài chính bản đầy đủ được công bố bởi công ty niêm yết, bạn có thể truy cập trang công bố thông tin của Uỷ ban chứng khoán tại địa chỉ `congbothongtin.ssc.gov.vn` hoặc các trang thông tin chứng khoán phổ biến trên thị trường. Nguồn dữ liệu được khuyến nghị là **KBS** cho mẫu báo cáo tài chính chuẩn và chi tiết.

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/1_quickstart_stock_vietnam.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

Hướng dẫn sử dụng

**Notebook minh hoạ**: Dành cho người học data, muốn thực hành trực tiếp với các ví dụ mẫu.

**Agent Guide**: Dành cho người theo trường phái Vibe Coding, muốn viết chương trình hiệu quả với AI.

## So sánh nguồn dữ liệu

| Phương thức | KBS | VCI | Ghi chú |
| --- | --- | --- | --- |
| **income\_statement()** | ✅ | ✅ | KBS: 90 dòng, VCI: 25+ cột |
| **balance\_sheet()** | ✅ | ✅ | KBS: 162 dòng, VCI: 36 cột |
| **cash\_flow()** | ✅ | ✅ | KBS: 159 dòng, VCI: 39 cột |
| **ratio()** | ✅ | ✅ | KBS: 27 chỉ số, VCI: 37+ chỉ số |

**Khuyến nghị:**

- **KBS**: Dữ liệu chi tiết theo dòng, phù hợp phân tích chuyên sâu, có cấu trúc phân cấp
- **VCI**: Dữ liệu theo cột, dễ sử dụng và tích hợp, định dạng đơn giản

## Khởi tạo Finance

### KBS Finance (Khuyến nghị)

Python

```python
from vnstock import Finance

# Khởi tạo với KBS
finance_kbs = Finance(
    source="KBS",           # Nguồn dữ liệu
    symbol="VCI",            # Mã chứng khoán
    standardize_columns=True,  # Chuẩn hóa tên cột
)
```

### VCI Finance

Python

```python
# Khởi tạo với VCI
finance_vci = Finance(
    source="VCI",            # Nguồn dữ liệu
    symbol="VCI",            # Mã chứng khoán
    period="quarter",        # Chu kỳ mặc định
    get_all=True,            # Lấy tất cả các trường
)
```

**Các tham số chung:**

- `symbol` (str): Mã chứng khoán (VD: 'VCI', 'ACB')
- `standardize_columns` (bool): Chuẩn hóa tên cột theo schema. Mặc định: True
- `proxy_mode` (str): Chế độ proxy. Mặc định: None
- `proxy_list` (list): Danh sách URL proxy. Mặc định: None

## Field Display Mode

Từ phiên bản v3.4.0+, tất cả các phương thức báo cáo tài chính hỗ trợ `display_mode` parameter để kiểm soát cách hiển thị các trường dữ liệu:

### Cách sử dụng

Python

```python
from vnstock import Finance
from vnstock.explorer.kbs.financial import FieldDisplayMode

finance = Finance(symbol="VCI", source="KBS")

# Mode 1: Standardized (mặc định) - Chỉ item tiếng Việt + item_id
df_std = finance.income_statement(
    period="quarter",
    display_mode=FieldDisplayMode.STD
)

# Mode 2: All Fields - Hiển thị cả item (VN), item_en, item_id
df_all = finance.income_statement(
    period="quarter",
    display_mode=FieldDisplayMode.ALL
)

# Mode 3: Auto Convert - Tự động chuyển đổi
df_auto = finance.income_statement(
    period="quarter",
    display_mode=FieldDisplayMode.AUTO
)

# Mode 4: chỉ Tiếng Việt (backward compatible)
df_vi = finance.income_statement(
    period="quarter",
    display_mode='vi'
)

# Mode 5: chỉ Tiếng Anh (backward compatible)
df_en = finance.income_statement(
    period="quarter",
    display_mode='en'
)
```

### Bảng so sánh các mode

| Mode | Tên | Mô tả | Cột |
| --- | --- | --- | --- |
| `FieldDisplayMode.STD` | Standardized | Chỉ hiển thị 'item' và 'item\_id' (chuẩn hóa) | item, item\_id, periods |
| `FieldDisplayMode.ALL` | All Fields | Hiển thị tất cả: item (VN), item\_en, item\_id | item, item\_en, item\_id, periods |
| `FieldDisplayMode.AUTO` | Auto Convert | Tự động chuyển đổi dựa trên loại dữ liệu | item, item\_en, item\_id, periods |
| `'vi'` | Vietnamese Only | Chỉ tiếng Việt (backward compatible) | item, item\_id, periods |
| `'en'` | English Only | Chỉ tiếng Anh (backward compatible) | item\_en, item\_id, periods |

## Báo cáo kết quả kinh doanh

### KBS Source - Báo cáo kết quả kinh doanh

**Gọi hàm**

Python

```python
from vnstock import Finance
from vnstock.explorer.kbs.financial import FieldDisplayMode

finance = Finance(symbol="VCI", source="KBS")

# Mode mặc định - Standardized
df = finance.income_statement(period="quarter")
print(f"Shape: {df.shape}")  # (90, 6)
```

**Tham số**

- `period` (str): Kỳ báo cáo - 'quarter' hoặc 'year'
- `display_mode` (str/FieldDisplayMode): Mode hiển thị trường dữ liệu

**Dữ liệu mẫu KBS:**

Shell

```bash
>>> finance.income_statement(period="quarter")

                                                item                             item_id      2025-Q4      2025-Q3      2025-Q2      2025-Q1
0                             I. DOANH THU HOẠT ĐỘNG                             operating_income          NaN          NaN          NaN          NaN
1  1.1. Lãi từ các tài sản tài chính ghi nhận thô...  gains_from_financial_assets_at_fair_value_thro...   750209276.0   590437543.0   615976718.0   524812855.0
2                    a. Lãi bán các tài sản tài chính  a_realised_gains_on_disposals_of_fvtpl_financi...   748943883.0   589172069.0   614712244.0   523548381.0

[90 rows x 6 columns]
```

**Dữ liệu mẫu KBS - All Fields Mode:**

Shell

```bash
>>> finance.income_statement(period="quarter", display_mode=FieldDisplayMode.ALL)

                                                item                                           item_en                             item_id  unit  levels  row_number      2025-Q4      2025-Q3      2025-Q2      2025-Q1
0                             I. DOANH THU HOẠT ĐỘNG                                     OPERATING INCOME                             operating_income  NaN      1.0           0          NaN          NaN          NaN          NaN
1  1.1. Lãi từ các tài sản tài chính ghi nhận thô...  1.1. Gains from financial assets at fair value...  gains_from_financial_assets_at_fair_value_thro...  VND      2.0           1   750209276.0   590437543.0   615976718.0   524812855.0

[90 rows x 10 columns]
```

### VCI Source - Báo cáo kết quả kinh doanh

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="VCI")
df = finance.income_statement(period="quarter")
print(f"Shape: {df.shape}")  # (52, 25)
```

**Dữ liệu mẫu VCI:**

Shell

```bash
>>> finance.income_statement(period="quarter")

  ticker  yearReport  lengthReport  Revenue (Bn. VND)  Revenue YoY (%)  Attribute to parent company (Bn. VND)  ...  Net Profit For the Year  Minority Interest  Attributable to parent company  Sales  Other income
0    VCI        2025             4      1526308619569         0.527843                            1452727693070  ...             1452727693070                 0                    1452727693070    NaN           NaN
1    VCI        2025             3      1443289075867         0.481268                            1370219906556  ...             1370219906556                 0                    1370219906556    NaN           NaN
2    VCI        2025             2      1159674866340         0.266226                            1100476657055  ...             1100476657055                 0                    1100476657055    NaN           NaN

[52 rows x 25 columns]
```

## Bảng cân đối kế toán

### KBS Source - Bảng cân đối kế toán

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="KBS")
df = finance.balance_sheet(period="quarter")
print(f"Shape: {df.shape}")  # (162, 6)
```

**Dữ liệu mẫu KBS:**

Shell

```bash
>>> finance.balance_sheet(period="quarter")

                                                item                             item_id      2025-Q4      2025-Q3      2025-Q2      2025-Q1
0                                 A. TÀI SẢN                                    assets          NaN          NaN          NaN          NaN
1                              I. Tài sản ngắn hạn                             current_assets          NaN          NaN          NaN          NaN
2                                   Tiền và các khoản tương đương tiền                         cash_and_cash_equivalents  63589689844.0  58696689844.0  52346689844.0  48996689844.0
3                                              Đầu tư tài chính ngắn hạn                     short_term_financial_investments  1234567890.0   1234567890.0   1234567890.0   1234567890.0
4                                                 Các khoản phải thu ngắn hạn                           short_term_receivables  9876543210.0   8765432109.0   7654321098.0   6543210987.0

[162 rows x 6 columns]
```

### VCI Source - Bảng cân đối kế toán

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="VCI")
df = finance.balance_sheet(period="quarter")
print(f"Shape: {df.shape}")  # (52, 36)
```

**Dữ liệu mẫu VCI:**

Shell

```bash
>>> finance.balance_sheet(period="quarter")

  ticker  yearReport  lengthReport  CURRENT ASSETS (Bn. VND)  Cash and cash equivalents (Bn. VND)  ...  Fixed Asset-To-Equity  Owners' Equity/Charter Capital  Asset Turnover  Revenue YoY (%)
0    VCI        2025             4                3516.842588                    635.89689844  ...                   0.12                         1.05        0.08         0.527843
1    VCI        2025             3                3456.789012                    586.96689844  ...                   0.11                         1.04        0.07         0.481268
2    VCI        2025             2                3234.567890                    523.46689844  ...                   0.10                         1.03        0.06         0.266226

[52 rows x 36 columns]
```

## Báo cáo lưu chuyển tiền tệ

### KBS Source - Báo cáo lưu chuyển tiền tệ

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="KBS")
df = finance.cash_flow(period="quarter")
print(f"Shape: {df.shape}")  # (159, 6)
```

**Dữ liệu mẫu KBS:**

Shell

```bash
>>> finance.cash_flow(period="quarter")

                                                item                             item_id      2025-Q4      2025-Q3      2025-Q2      2025-Q1
0                      I. Lưu chuyển tiền tệ từ hoạt động kinh doanh                             cash_from_operations          NaN          NaN          NaN          NaN
1                                            Lợi nhuận trước thuế                             profit_before_tax  1452727693070.0 1370219906556.0 1100476657055.0   987654321098.0
2                               Các khoản điều chỉnh lại lợi nhuận trước thuế                    adjustments_to_profit_before_tax  -1234567890.0  -1234567890.0  -1234567890.0  -1234567890.0

[159 rows x 6 columns]
```

### VCI Source - Báo cáo lưu chuyển tiền tệ

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="VCI")
df = finance.cash_flow(period="quarter")
print(f"Shape: {df.shape}")  # (52, 39)
```

**Dữ liệu mẫu VCI:**

Shell

```bash
>>> finance.cash_flow(period="quarter")

  ticker  yearReport  lengthReport  Net Cash Flow from Operating Activities (Bn. VND)  ...  Net increase/decrease in cash and cash equivalents (Bn. VND)  Cash and cash equivalents at beginning of period (Bn. VND)  Cash and cash equivalents at end of period (Bn. VND)
0    VCI        2025             4                                         1234.567890  ...                                               48.930000                                      586.96689844                                     635.89689844
1    VCI        2025             3                                         1234.567890  ...                                               63.500000                                      523.46689844                                     586.96689844
2    VCI        2025             2                                         1234.567890  ...                                               33.500000                                      489.96689844                                     523.46689844

[52 rows x 39 columns]
```

## Chỉ số tài chính

### KBS Source - Chỉ số tài chính

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="KBS")
df = finance.ratio(period="quarter")
print(f"Shape: {df.shape}")  # (27, 6)
```

**Dữ liệu mẫu KBS:**

Shell

```bash
>>> finance.ratio(period="quarter")

              item     item_id      2025-Q4      2025-Q3      2025-Q2      2025-Q1
0              PE         pe          12.5        13.2        14.1        15.3
1              PB         pb           1.8         1.9         2.0         2.1
2             ROE        roe          15.2        14.8        14.5        14.2
3             ROA        roa           8.7         8.5         8.3         8.1
4            Beta       beta           1.2         1.3         1.4         1.5

[27 rows x 6 columns]
```

### VCI Source - Chỉ số tài chính

**Gọi hàm**

Python

```python
finance = Finance(symbol="VCI", source="VCI")
df = finance.ratio(period="quarter")
print(f"Shape: {df.shape}")  # (52, 37)
```

**Dữ liệu mẫu VCI:**

Shell

```bash
>>> finance.ratio(period="quarter")

  ticker  yearReport  lengthReport  (ST+LT borrowings)/Equity  Debt/Equity  Fixed Asset-To-Equity  ...  Revenue YoY (%)  Net Profit YoY (%)  ROE (%)  ROA (%)
0    VCI        2025             4                     0.12         0.08                  0.12  ...         0.527843           0.123456    15.2     8.7
1    VCI        2025             3                     0.11         0.07                  0.11  ...         0.481268           0.234567    14.8     8.5
2    VCI        2025             2                     0.10         0.06                  0.10  ...         0.266226           0.345678    14.5     8.3

[52 rows x 37 columns]
```

## Mẹo sử dụng

### 1\. Lọc các chỉ tiêu chính (KBS)

Python

```python
from vnstock import Finance

finance = Finance(symbol="VCI", source="KBS")
df = finance.income_statement(period="quarter")

# Lọc theo levels (level 1 = chỉ tiêu chính)
key_items = df[df['levels'] == 1]
print(key_items[['item', 'item_id', '2025-Q4']])

# Lọc theo item_id cụ thể
important_ids = ['revenue', 'net_profit', 'operating_profit']
important_data = df[df['item_id'].isin(important_ids)]
```

### 2\. Kết hợp dữ liệu từ nhiều báo cáo

Python

```python
from vnstock import Finance
import pandas as pd

finance = Finance(symbol="VCI", source="KBS")

# Lấy dữ liệu từ các báo cáo khác nhau
income = finance.income_statement(period="year")
balance = finance.balance_sheet(period="year")
ratios = finance.ratio(period="year")

# Lọc các chỉ tiêu cần thiết
revenue = income[income['item_id'] == 'revenue'].iloc[0]
total_assets = balance[balance['item_id'] == 'total_assets'].iloc[0]
roe = ratios[ratios['item_id'] == 'roe'].iloc[0]

# Tạo bảng tổng hợp
summary = pd.DataFrame({
    'Revenue': revenue[['2025', '2024', '2023']],
    'Total Assets': total_assets[['2025', '2024', '2023']],
    'ROE': roe[['2025', '2024', '2023']]
})
print(summary)
```

### 3\. Proxy Support cho Cloud Environments

Python

```python
# Tránh IP blocking trên Google Colab/Kaggle
finance = Finance(
    symbol="VCI",
    source="KBS",
    proxy_mode="rotate",  # Xoay vòng proxy
    proxy_list=[\
        "http://proxy1.com:8080",\
        "http://proxy2.com:8080"\
    ]
)

df = finance.income_statement(period="quarter")
```

## Lưu ý quan trọng

- **KBS** là nguồn dữ liệu khuyến nghị cho vnstock 3.4.2+, cung cấp dữ liệu chi tiết và có cấu trúc phân cấp
- **VCI** vẫn được hỗ trợ nhưng có cấu trúc dữ liệu đơn giản hơn
- Luôn kiểm tra shape và columns của DataFrame trước khi xử lý
- Sử dụng `display_mode` để kiểm soát cách hiển thị dữ liệu
- Các period columns có format: `'2025-Q4', '2025-Q3', '2025-Q2', '2025-Q1'` cho quarterly và `'2025', '2024', '2023'` cho yearly

#### Tags

[báo cáo tài chính](https://vnstocks.com/blog/tag/bao-cao-tai-chinh) [chỉ số tài chính](https://vnstocks.com/blog/tag/chi-so-tai-chinh)

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập