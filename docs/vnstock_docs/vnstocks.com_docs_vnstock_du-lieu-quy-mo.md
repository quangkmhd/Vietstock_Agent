---
url: "https://vnstocks.com/docs/vnstock/du-lieu-quy-mo"
title: "Dữ liệu quỹ mở | Vnstock"
---

Toggle Sidebar

### Mục lục

Giới thiệu

Vnstock cung cấp thông tin chi tiết quỹ mở công khai từ fmarket.vn giúp các nhà đầu tư có thể dễ dàng truy xuất dữ liệu dành cho mục đích phân tích và tìm kiếm cơ hội đầu tư dựa trên dữ liệu dễ dàng. Bằng cách sử dụng các hàm được mô tả dưới đây, bạn có thể truy xuất dữ liệu qua định dạng pandas DataFrame sau đó phân tích hoặc lưu trữ thành định dạng bạn mong muốn như Excel, csv, Google Sheets, Database, vv.

Vnstock xin gửi lời cám ơn tới bạn andrey\_jef đã đóng góp bộ mã nguồn cho dự án. Các hàm được mô tả dưới đây đã được tuỳ biến lại để tương thích với trải nghiệm chung của Vnstock3.

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/4_funds_vnstock.ipynb)

## Khởi tạo đối tượng

Để tra cứu thông tin quỹ mở, bạn sử dụng module `fund` từ nguồn dữ liệu fmarket như dưới đây. Có thể sử dụng trực tiếp `Fund` class để gọi hàm hoặc gán với biến `fund` cho đơn giản.

Python

```python
from vnstock import Fund
fund = Fund()
```

## Liệt kê quỹ

**Gọi hàm**

Python

```python
fund.listing()
```

**Tham số**

- `fund_type`(str, không bắt buộc): nhóm phân loại quỹ, mặc định là rỗng để liệt kê tất cả quỹ. Các giá trị có thể sử dụng bao gồm:

  - `BALANCED`: Quỹ cân bằng
  - `BOND`: Quỹ trái phiếu
  - `STOCK`: Quỹ cổ phiếu
  - `""`: string rỗng (mặc định) - Tất cả quỹ

**Dữ liệu mẫu:**

Shell

```bash
>>> fund.listing().head()
Total number of funds currently listed on Fmarket:  49
  short_name                                               name     fund_type                                    fund_owner_name  ...  nav_update_at fund_id_fmarket  fund_code   vsd_fee_id
0     SSISCA         QUỸ ĐẦU TƯ LỢI THẾ CẠNH TRANH BỀN VỮNG SSI  Quỹ cổ phiếu                       CÔNG TY TNHH QUẢN LÝ QUỸ SSI  ...     2024-07-09              11     SSISCA   SSISCAN001
1      VESAF  QUỸ ĐẦU TƯ CỔ PHIẾU TIẾP CẬN THỊ TRƯỜNG VINACA...  Quỹ cổ phiếu            CÔNG TY CỔ PHẦN QUẢN LÝ QUỸ VINACAPITAL  ...     2024-07-09              23      VESAF    VESAFN002
2       BVPF            QUỸ ĐẦU TƯ CỔ PHIẾU TRIỂN VỌNG BẢO VIỆT  Quỹ cổ phiếu                  CÔNG TY TNHH QUẢN LÝ QUỸ BẢO VIỆT  ...     2024-07-09              14       BVPF     BVPFN001
3       VEOF         QUỸ ĐẦU TƯ CỔ PHIẾU HƯNG THỊNH VINACAPITAL  Quỹ cổ phiếu            CÔNG TY CỔ PHẦN QUẢN LÝ QUỸ VINACAPITAL  ...     2024-07-09              20       VEOF     VEOFN003
4   VCBF-TBF                QUỸ ĐẦU TƯ CÂN BẰNG CHIẾN LƯỢC VCBF  Quỹ cân bằng  CÔNG TY LIÊN DOANH QUẢN LÝ QUỸ ĐẦU TƯ CHỨNG KH...  ...     2024-07-09              31    VCBFTBF  VCBFTBFN001

[5 rows x 21 columns]
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 49 entries, 0 to 48
Data columns (total 21 columns):
 #   Column                     Non-Null Count  Dtype
---  ------                     --------------  -----
 0   short_name                 49 non-null     object
 1   name                       49 non-null     object
 2   fund_type                  49 non-null     object
 3   fund_owner_name            49 non-null     object
 4   management_fee             49 non-null     float64
 5   inception_date             44 non-null     object
 6   nav                        49 non-null     float64
 7   nav_change_previous        49 non-null     float64
 8   nav_change_last_year       45 non-null     float64
 9   nav_change_inception       49 non-null     float64
 10  nav_change_1m              46 non-null     float64
 11  nav_change_3m              46 non-null     float64
 12  nav_change_6m              43 non-null     float64
 13  nav_change_12m             42 non-null     float64
 14  nav_change_24m             34 non-null     float64
 15  nav_change_36m             28 non-null     float64
 16  nav_change_36m_annualized  28 non-null     float64
 17  nav_update_at              49 non-null     object
 18  fund_id_fmarket            49 non-null     int64
 19  fund_code                  49 non-null     object
 20  vsd_fee_id                 49 non-null     object
dtypes: float64(12), int64(1), object(8)
```

## Tìm kiếm quỹ

**Gọi hàm**

Python

```python
fund.filter('DC')
```

**Tham số**

- `symbol` (str, bắt buộc): Tên viết tắt của quỹ cần tìm kiếm. Nhập 1 phần tên để liệt kê các kết quả trùng khớp.

**Dữ liệu mẫu:**

Shell

```bash
>>> fund.filter('DC')
   id shortName
0  40     VNDCF
1  67      DCIP
2  62    HDBOND
3  27      DCBF
4  25      DCDE
5  28      DCDS
6  29      DCAF
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7 entries, 0 to 6
Data columns (total 2 columns):
 #   Column     Non-Null Count  Dtype
---  ------     --------------  -----
 0   id         7 non-null      int64
 1   shortName  7 non-null      object
dtypes: int64(1), object(1)
memory usage: 240.0+ bytes
```

## Thông tin chi tiết quỹ

### Báo cáo tăng trưởng NAV

**Gọi hàm**

Python

```python
fund.details.nav_report('SSISCA')
```

**Tham số**

- `symbol` (str, bắt buộc): Tên viết tắt của quỹ cần tìm kiếm. Nhập 1 phần tên để liệt kê các kết quả trùng khớp.

**Dữ liệu mẫu:**

Shell

```bash
>>> fund.details.nav_report('SSISCA')
Retrieving data for SSISCA
            date  nav_per_unit short_name
0     2017-01-04      14412.31     SSISCA
1     2017-01-11      14527.86     SSISCA
2     2017-01-18      14240.04     SSISCA
3     2017-01-25      14547.21     SSISCA
4     2017-01-31      14541.96     SSISCA
...          ...           ...        ...
1535  2024-07-03      39212.58     SSISCA
1536  2024-07-04      39510.62     SSISCA
1537  2024-07-05      39690.75     SSISCA
1538  2024-07-08      39871.40     SSISCA
1539  2024-07-09      40055.88     SSISCA

[1540 rows x 3 columns]
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1540 entries, 0 to 1539
Data columns (total 3 columns):
 #   Column        Non-Null Count  Dtype
---  ------        --------------  -----
 0   date          1540 non-null   object
 1   nav_per_unit  1540 non-null   float64
 2   short_name    1540 non-null   object
dtypes: float64(1), object(2)
memory usage: 36.2+ KB
```

### Danh mục đầu tư lớn

**Gọi hàm**

Python

```python
fund.details.top_holding('SSISCA')
```

**Tham số**

- `symbol` (str, bắt buộc): Tên viết tắt của quỹ cần tìm kiếm. Nhập 1 phần tên để liệt kê các kết quả trùng khớp.

**Dữ liệu mẫu:**

Shell

```bash
>>> fund.details.top_holding('SSISCA')

Retrieving data for SSISCA
  stock_code                industry  net_asset_percent type_asset   update_at  fundId short_name
0        FPT  Công nghệ và thông tin              17.10      STOCK  2024-07-05      11     SSISCA
1        MWG                  Bán lẻ               6.65      STOCK  2024-07-05      11     SSISCA
2        ACB               Ngân hàng               5.77      STOCK  2024-07-05      11     SSISCA
3        HPG       Vật liệu xây dựng               3.97      STOCK  2024-07-05      11     SSISCA
4        CTG               Ngân hàng               3.64      STOCK  2024-07-05      11     SSISCA
5        STB               Ngân hàng               3.32      STOCK  2024-07-05      11     SSISCA
6        MBB               Ngân hàng               3.24      STOCK  2024-07-05      11     SSISCA
7        BWE                Tiện ích               2.97      STOCK  2024-07-05      11     SSISCA
8        REE                Xây dựng               2.95      STOCK  2024-07-05      11     SSISCA
9        DHC        Sản xuất Phụ trợ               2.75      STOCK  2024-07-05      11     SSISCA
```

**Kiểu dữ liệu**

Shell

```bash
RangeIndex: 10 entries, 0 to 9
Data columns (total 7 columns):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   stock_code         10 non-null     object
 1   industry           10 non-null     object
 2   net_asset_percent  10 non-null     float64
 3   type_asset         10 non-null     object
 4   update_at          10 non-null     object
 5   fundId             10 non-null     int64
 6   short_name         10 non-null     object
dtypes: float64(1), int64(1), object(5)
memory usage: 688.0+ bytes
```

### Phân bổ theo ngành

**Gọi hàm**

Python

```python
fund.details.industry_holding('SSISCA')
```

**Tham số**

- `symbol` (str, bắt buộc): Tên viết tắt của quỹ cần tìm kiếm. Nhập 1 phần tên để liệt kê các kết quả trùng khớp.

**Dữ liệu mẫu:**

Shell

```bash
>>> fund.details.industry_holding('SSISCA')

Retrieving data for SSISCA
                      industry  net_asset_percent short_name
0                    Ngân hàng              20.46     SSISCA
1       Công nghệ và thông tin              17.10     SSISCA
2                 Bất động sản               8.68     SSISCA
3                       Bán lẻ               6.73     SSISCA
4             Sản xuất Phụ trợ               4.72     SSISCA
5            Vận tải - Kho bãi               4.62     SSISCA
6            Vật liệu xây dựng               3.97     SSISCA
7                     Tiện ích               2.97     SSISCA
8                     Xây dựng               2.95     SSISCA
9       Sản xuất Hàng gia dụng               2.24     SSISCA
10           Chế biến thủy sản               1.85     SSISCA
11  Sản xuất Thiết bị, máy móc               1.82     SSISCA
12    Sản xuất Nhựa - Hóa chất               1.73     SSISCA
13      Dịch vụ tư vấn, hỗ trợ               1.70     SSISCA
14                 Chứng khoán               1.52     SSISCA
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 15 entries, 0 to 14
Data columns (total 3 columns):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   industry           15 non-null     object
 1   net_asset_percent  15 non-null     float64
 2   short_name         15 non-null     object
dtypes: float64(1), object(2)
memory usage: 488.0+ bytes
```

### Phân bổ theo tài sản

**Gọi hàm**

Python

```python
fund.details.asset_holding('SSISCA')
```

**Tham số**

- `symbol` (str, bắt buộc): Tên viết tắt của quỹ cần tìm kiếm. Nhập 1 phần tên để liệt kê các kết quả trùng khớp.

**Dữ liệu mẫu:**

Shell

```bash
>>> fund.details.asset_holding('SSISCA')
Retrieving data for SSISCA
   asset_percent                asset_type short_name
0          83.08                  Cổ phiếu     SSISCA
1          16.92  Tiền và tương đương tiền     SSISCA
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 3 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   asset_percent  2 non-null      float64
 1   asset_type     2 non-null      object
 2   short_name     2 non-null      object
dtypes: float64(1), object(2)
memory usage: 176.0+ bytes
```

#### Tags

[dữ liệu quỹ mở](https://vnstocks.com/blog/tag/du-lieu-quy-mo) [danh mục đầu tư](https://vnstocks.com/blog/tag/danh-muc-dau-tu)

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập