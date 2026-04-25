---
url: "https://vnstocks.com/docs/vnstock/thong-tin-cong-ty"
title: "Thông tin công ty | Vnstock"
---

## Mục lục

Gợi ý

Các hàm trong mục thông tin công ty chỉ áp dụng với mã chứng khoán của các doanh nghiệp trong nước. Khuyến nghị sử dụng KBS làm nguồn dữ liệu mặc định (dùng được cho Google Colab/Kaggle). Các hàm truy xuất thông tin công ty không cần nhập tham số sau khi đã tạo đối tượng `company`.

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/1_quickstart_stock_vietnam.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

Hướng dẫn sử dụng

**Notebook minh hoạ**: Dành cho người học data, muốn thực hành trực tiếp với các ví dụ mẫu.

**Agent Guide**: Dành cho người theo trường phái Vibe Coding, muốn viết chương trình hiệu quả với AI.

## Khởi tạo đối tượng

Bạn có thể sử dụng hai nguồn dữ liệu: **KBS** (khuyến nghị), **VCI** (không thể truy cập từ các dịch vụ của Google Cloud do bị chặn dải IP). Thông tin nguồn dữ liệu được cài đặt khi khởi tạo đối tượng python trước khi gọi các hàm truy xuất từng loại thông tin cụ thể.

Python

```python
from vnstock import Company

# Khuyến nghị - Ổn định hơn cho Google Colab/Kaggle
company = Company(symbol='VCB', source='KBS')

# Hoặc sử dụng VCI (dữ liệu đầy đủ hơn)
company = Company(symbol='VCB', source='VCI')
```

## So Sánh Nguồn Dữ Liệu

| Phương Thức | KBS | VCI | Ghi Chú |
| --- | --- | --- | --- |
| **overview()** | ✅ | ✅ | KBS: 30 columns, VCI: 10 columns |
| **shareholders()** | ✅ | ✅ | KBS: 4 cols, VCI: 5 cols |
| **officers()** | ✅ | ✅ | KBS: 5 cols, VCI: 7 cols |
| **subsidiaries()** | ✅ | ❌ | Chỉ KBS có (6 cols) |
| **affiliate()** | ✅ | ✅ | Cả hai đều rỗng |
| **news()** | ✅ | ✅ | KBS: 5 cols, VCI: 18 cols |
| **events()** | ✅ | ✅ | KBS: rỗng, VCI: 13 cols |
| **ownership()** | ✅ | ❌ | Chỉ KBS có (4 cols) |
| **capital\_history()** | ✅ | ❌ | Chỉ KBS có (3 cols) |
| **insider\_trading()** | ✅ | ❌ | Chỉ KBS có (có thể rỗng) |
| **reports()** | ❌ | ✅ | Chỉ VCI có (có thể rỗng) |
| **trading\_stats()** | ❌ | ✅ | Chỉ VCI có (24 cols) |
| **ratio\_summary()** | ❌ | ✅ | Chỉ VCI có (46 cols) |

## Thông tin công ty

**Gọi hàm**

Python

```python
company = Company(symbol='VCI', source='KBS')
company.overview()
```

**Tham số**

Không có

### KBS Source - 30 columns

**Dữ liệu trả về**

- `business_model` (object): Mô hình kinh doanh
- `symbol` (object): Mã chứng khoán
- `founded_date` (object): Ngày thành lập
- `charter_capital` (int64): Vốn điều lệ
- `number_of_employees` (int64): Số lượng nhân viên
- `listing_date` (object): Ngày niêm yết
- `par_value` (int64): Mệnh giá
- `exchange` (object): Sàn giao dịch
- `listing_price` (int64): Giá niêm yết
- `listed_volume` (int64): Khối lượng niêm yết
- `ceo_name` (object): Tên CEO
- `ceo_position` (object): Vị trí CEO
- `inspector_name` (object): Tên kiểm soát viên
- `inspector_position` (object): Vị trí kiểm soát viên
- `establishment_license` (object): Giấy phép thành lập
- `business_code` (object): Mã ngành kinh doanh
- `tax_id` (object): Mã số thuế
- `auditor` (object): Kiểm toán viên
- `company_type` (object): Loại hình công ty
- `address` (object): Địa chỉ
- `phone` (object): Điện thoại
- `fax` (object): Fax
- `email` (object): Email
- `website` (object): Website
- `branches` (object): Chi nhánh
- `history` (object): Lịch sử
- `free_float_percentage` (int64): Tỷ lệ free float
- `free_float` (int64): Số lượng free float
- `outstanding_shares` (int64): Số cổ phiếu đang lưu hành
- `as_of_date` (object): Ngày cập nhật dữ liệu

**Dữ liệu mẫu**

Shell

```bash
>>> company.overview()
Shape: (1, 30)
>>> company.overview()[['symbol', 'charter_capital', 'exchange', 'founded_date']].head()
  symbol  charter_capital exchange founded_date
0    VCI      8501000000000      HOSE   06/08/2007
```

### VCI Source - 10 columns

**Dữ liệu trả về**

- `symbol` (object): Mã chứng khoán
- `id` (object): ID công ty
- `issue_share` (int64): Số cổ phiếu phát hành
- `history` (object): Lịch sử công ty
- `company_profile` (object): Hồ sơ công ty
- `icb_name3` (object): Phân loại ngành ICB cấp 3
- `icb_name2` (object): Phân loại ngành ICB cấp 2
- `icb_name4` (object): Phân loại ngành ICB cấp 4
- `financial_ratio_issue_share` (int64): Tỷ lệ tài chính trên số cổ phiếu
- `charter_capital` (int64): Vốn điều lệ

**Dữ liệu mẫu**

Shell

```bash
>>> company.overview()
Shape: (1, 10)
>>> company.overview()[['symbol', 'charter_capital', 'icb_name4']].head()
  symbol     id  issue_share  ...             icb_name4 charter_capital
0    VCI  75885    850100000  ...  Môi giới chứng khoán   8501000000000
```

## Cổ đông lớn

**Gọi hàm**

Python

```python
company.shareholders()
```

**Tham số**

Không có

### KBS Source - 4 columns

**Dữ liệu trả về**

- `name` (object): Tên cổ đông
- `update_date` (object): Ngày cập nhật
- `shares_owned` (int64): Số cổ phiếu sở hữu
- `ownership_percentage` (float64): Tỷ lệ sở hữu (%)

**Dữ liệu mẫu**

Shell

```bash
>>> company.shareholders()
Shape: (1, 4)
>>> company.shareholders()
      name          update_date  shares_owned  ownership_percentage
0  Tô Hải  2025-06-30T00:00:00     128889403                 17.95
```

### VCI Source - 5 columns

**Dữ liệu trả về**

- `id` (object): ID cổ đông
- `share_holder` (object): Tên cổ đông
- `quantity` (int64): Số lượng cổ phiếu
- `share_own_percent` (float64): Tỷ lệ sở hữu (%)
- `update_date` (object): Ngày cập nhật

**Dữ liệu mẫu**

Shell

```bash
>>> company.shareholders()
Shape: (33, 5)
>>> company.shareholders().head(3)
         id           share_holder   quantity  share_own_percent update_date
0  97763912                 Tô Hải  129139403            0.17870  2025-10-31
1  97762509         PYN Elite Fund    8132100            0.04910  2025-01-24
2  97753862  Nguyễn Phan Minh Khôi    7483872            0.04591  2025-01-24
```

## Ban lãnh đạo

**Gọi hàm**

Python

```python
company.officers()
```

**Tham số**

Không có

### KBS Source - 5 columns

**Dữ liệu trả về**

- `from_date` (int64): Năm bắt đầu
- `position` (object): Vị trí công việc (tiếng Việt)
- `name` (object): Tên nhân viên
- `position_en` (object): Vị trí công việc (tiếng Anh)
- `owner_code` (object): Mã sở hữu

**Dữ liệu mẫu**

Shell

```bash
>>> company.officers()
Shape: (14, 5)
>>> company.officers()[['name', 'position', 'from_date']].head(3)
                   name        position  from_date
0  Bà Nguyễn Thanh Phượng          CTHĐQT       2007
1       Ông Đinh Quang Hoàn  Phó TGĐ/Phó CTHĐQT       2007
2                Ông Tô Hải      TGĐ/TVHĐQT       2007
```

### VCI Source - 7 columns

**Dữ liệu trả về**

- `id` (int64): ID nhân viên
- `officer_name` (object): Tên nhân viên
- `officer_position` (object): Vị trí công việc
- `officer_own_percent` (float64): Tỷ lệ sở hữu (%)
- `quantity` (int64): Số lượng cổ phiếu
- `update_date` (object): Ngày cập nhật
- `position` (object): Vị trí (có thể rỗng)

**Dữ liệu mẫu**

Shell

```bash
>>> company.officers()
Shape: (14, 7)
>>> company.officers()[['officer_name', 'officer_position', 'officer_own_percent']].head(3)
   id         officer_name                            officer_position  \
0  11               Tô Hải  Tổng Giám đốc/Thành viên Hội đồng Quản trị
1  14  Nguyễn Thanh Phượng                  Chủ tịch Hội đồng Quản trị
2   4     Nguyễn Quang Bảo                           Phó Tổng Giám đốc

   officer_own_percent   quantity update_date position
0               0.1787  129139403  2025-10-31      NaN
1               0.0318   22815000  2025-10-31      NaN
2               0.0032    2324156  2025-10-31      NaN
```

## Công ty con (Chỉ KBS)

**Gọi hàm**

Python

```python
company.subsidiaries()
```

**Tham số**

Không có

**Dữ liệu trả về**

- `update_date` (object): Ngày cập nhật
- `name` (object): Tên công ty con
- `charter_capital` (int64): Vốn điều lệ
- `ownership_percent` (int64): Tỷ lệ sở hữu (%)
- `currency` (object): Loại tiền tệ
- `type` (object): Loại quan hệ

**Dữ liệu mẫu**

Shell

```bash
>>> company.subsidiaries()
Shape: (1, 6)
>>> company.subsidiaries()
           update_date                                          name  charter_capital  ownership_percent currency         type
0  2019-01-28T00:00:00  CTCP Quản lý Quỹ Đầu tư Chứng khoán Bản Việt     130000000000                 51      VND  công ty con
```

**Lưu ý**: VCI source trả về lỗi `RetryError` cho phương thức này.

## Công ty liên kết

**Gọi hàm**

Python

```python
company.affiliate()
```

**Tham số**

Không có

### KBS Source - 6 columns

**Dữ liệu trả về**

- `update_date` (object): Ngày cập nhật
- `name` (object): Tên công ty liên kết
- `charter_capital` (int64): Vốn điều lệ
- `ownership_percent` (float64): Tỷ lệ sở hữu (%)
- `currency` (object): Loại tiền tệ
- `type` (object): Loại quan hệ

**Dữ liệu mẫu**

Shell

```bash
>>> company.affiliate()
Shape: (18, 6)
>>> company.affiliate().head(3)
           update_date                                                          name  charter_capital  ownership_percent currency              type
0  2024-12-31T00:00:00                            CTCP Phát triển Giáo dục Miền Đông     366000000000              50.00      VND  công ty liên kết
1  2024-12-31T00:00:00                              CTCP Phát triển Hạ tầng Kỹ thuật    3777000000000              49.76      VND  công ty liên kết
2  2024-12-31T00:00:00  Công ty Liên doanh TNHH Khu công nghiệp Việt Nam - Singapore    2678000000000              49.00      VND  công ty liên kết
```

### VCI Source - 4 columns

**Dữ liệu trả về**

- `id` (object): ID công ty liên kết
- `sub_organ_code` (object): Mã công ty con
- `organ_name` (object): Tên công ty
- `ownership_percent` (object): Tỷ lệ sở hữu (có thể rỗng)

**Dữ liệu mẫu**

Shell

```bash
>>> company.affiliate()
Shape: (2, 4)
>>> company.affiliate()
         id sub_organ_code                                       organ_name ownership_percent
0  27673690           ACBD  CÔNG TY CỔ PHẦN DỊCH VỤ BẢO VỆ NGÂN HÀNG Á CHÂU             None
1  27673689           SGGS        Công ty Cổ phần Sài Gòn Kim hoàn ACB- SJC             None
```

## Tin tức

**Gọi hàm**

Python

```python
company.news()
```

**Tham số**

Không có

### KBS Source - 5 columns

**Dữ liệu trả về**

- `head` (object): Tiêu đề tin tức
- `article_id` (int64): ID bài viết
- `title` (object): Tiêu đề phụ
- `publish_time` (object): Thời gian xuất bản
- `url` (object): Link bài viết

**Dữ liệu mẫu**

Shell

```bash
>>> company.news()
Shape: (1, 5)
>>> company.news()[['head', 'publish_time']].head()
                                                head  article_id                                           title
0  Chứng khoán Vietcap (HOSE: VCI) công bố BCTC q...     1392728  Vietcap vượt 15% kế hoạch lợi nhuận 2025, tăng...
                 publish_time                                                url
0  2026-01-20T15:57:16.46  /2026/01/vietcap-vuot-15-ke-hoach-loi-nhuan-20...
```

### VCI Source - 18 columns

**Dữ liệu trả về**

- `id` (int64): ID tin tức
- `news_title` (object): Tiêu đề tin tức
- `public_date` (object): Ngày công bố
- `meta_title` (object): Meta title
- `meta_description` (object): Meta description
- `meta_keywords` (object): Meta keywords
- `tags` (object): Tags
- `content` (object): Nội dung
- `author` (object): Tác giả
- `source` (object): Nguồn
- `status` (int64): Trạng thái
- `created_at` (object): Thời gian tạo
- `updated_at` (object): Thời gian cập nhật
- `published_at` (object): Thời gian xuất bản
- `url` (object): Link
- `image_url` (object): Link ảnh
- `price_change_pct` (float64): Tỷ lệ thay đổi giá
- `symbol` (object): Mã chứng khoán

**Dữ liệu mẫu**

Shell

```bash
>>> company.news()
Shape: (10, 18)
>>> company.news()[['news_title', 'public_date', 'price_change_pct']].head(3)
        id                                         news_title  ...  price_change_pct
0  9121667  VCI: Thông báo về việc giao dịch chứng khoán t...  ...        -0.013235
1  9108930  VCI: Giấy phép điều chỉnh giấy phép thành lập ...  ...         0.019118
2  9095781  VCI: Quyết định về việc thay đổi đăng ký niêm yết  ...        -0.002825
```

## Sự kiện

**Gọi hàm**

Python

```python
company.events()
```

**Tham số**

Không có

### KBS Source

**Dữ liệu trả về**

DataFrame có thể rỗng

⚠️ **Lưu ý**: KBS thường trả về dữ liệu sự kiện rỗng.

### VCI Source - 13 columns

**Dữ liệu trả về**

- `id` (object): ID sự kiện
- `event_title` (object): Tiêu đề sự kiện (tiếng Việt)
- `en__event_title` (object): Tiêu đề sự kiện (tiếng Anh)
- `public_date` (object): Ngày công bố
- `issue_date` (object): Ngày phát hành
- `source_url` (object): Link tài liệu
- `event_list_code` (object): Mã loại sự kiện
- `event_list_name` (object): Tên loại sự kiện (tiếng Việt)
- `en__event_list_name` (object): Tên loại sự kiện (tiếng Anh)
- `ratio` (float64): Tỷ lệ
- `value` (float64): Giá trị
- `record_date` (object): Ngày ghi danh
- `exright_date` (object): Ngày hết quyền

**Dữ liệu mẫu**

Shell

```bash
>>> company.events()
Shape: (32, 13)
>>> company.events()[['event_title', 'event_list_name', 'public_date']].head(5)
         id                                        event_title  ...           event_list_name en__event_list_name
0   1868825  VCI - Trả cổ tức Đợt 1, 2021 bằng tiền 1200 VN...  ...  Trả cổ tức bằng tiền mặt       Cash Dividend
1  16582552  VCI - Trả cổ tức Đợt 1 năm 2022 bằng tiền 700 ...  ...  Trả cổ tức bằng tiền mặt       Cash Dividend
2  22322707  VCI - Trả cổ tức Đợt 2 năm 2022 bằng tiền 500 ...  ...  Trả cổ tức bằng tiền mặt       Cash Dividend
```

## Cơ cấu cổ đông (Chỉ KBS)

**Gọi hàm**

Python

```python
company.ownership()
```

**Tham số**

Không có

**Dữ liệu trả về**

- `owner_type` (object): Loại cổ đông
- `ownership_percentage` (float64): Tỷ lệ sở hữu (%)
- `shares_owned` (int64): Số cổ phiếu sở hữu
- `update_date` (object): Ngày cập nhật

**Dữ liệu mẫu**

Shell

```bash
>>> company.ownership()
Shape: (3, 4)
>>> company.ownership()
                owner_type  ownership_percentage  shares_owned          update_date
0     CĐ nắm trên 5% số CP                 17.95     128889403  2024-12-31T00:00:00
1  CĐ nắm từ 1% - 5% số CP                 39.65     284754680  2024-12-31T00:00:00
2     CĐ nắm dưới 1% số CP                 42.40     304455397  2024-12-31T00:00:00
```

## Lịch sử vốn điều lệ (Chỉ KBS)

**Gọi hàm**

Python

```python
company.capital_history()
```

**Tham số**

Không có

**Dữ liệu trả về**

- `date` (object): Ngày thay đổi
- `charter_capital` (int64): Vốn điều lệ
- `currency` (object): Loại tiền tệ

**Dữ liệu mẫu**

Shell

```bash
>>> company.capital_history()
Shape: (19, 3)
>>> company.capital_history().head()
        date  charter_capital currency
0  2025-12-17    8501000000000      VND
1  2025-03-07    7226000000000      VND
2  2024-06-12    7180994800000      VND
3  2024-10-10    5744694800000      VND
4  2024-05-08    4419000000000      VND
```

## Giao dịch nội bộ (Chỉ KBS)

**Gọi hàm**

Python

```python
company.insider_trading(page=1, page_size=10)
```

**Tham số**

- `page` (int, tùy chọn): Số trang (mặc định: 1)
- `page_size` (int, tùy chọn): Kích thước trang (mặc định: 10)

**Dữ liệu trả về**

DataFrame rỗng

⚠️ **Lưu ý**: Có thể trả về DataFrame rỗng nếu không có giao dịch nội bộ.

## Báo cáo phân tích (Chỉ VCI)

**Gọi hàm**

Python

```python
company.reports()
```

**Tham số**

Không có

**Dữ liệu trả về**

DataFrame rỗng

⚠️ **Lưu ý**: Có thể trả về DataFrame rỗng nếu không có báo cáo phân tích.

## Thống kê giao dịch (Chỉ VCI)

**Gọi hàm**

Python

```python
company.trading_stats()
```

**Tham số**

Không có

**Dữ liệu trả về**

DataFrame với 24 columns thống kê giao dịch bao gồm:

- `symbol` (object): Mã chứng khoán
- `exchange` (object): Sàn giao dịch
- `ev` (int64): Enterprise value
- `ceiling` (int64): Giá trần
- `floor` (int64): Giá sàn
- `reference` (int64): Giá tham chiếu
- `avg_match_price_*` (float64): Giá trung bình khớp lệnh (1d, 3d, 1w, 1m, 3m, 6m, 1y)
- `avg_match_volume_2w` (float64): Khối lượng trung bình 2 tuần
- `foreign_holding_room` (int64): Room ngoại
- `current_holding_ratio` (float64): Tỷ lệ nắm giữ hiện tại
- `max_holding_ratio` (float64): Tỷ lệ nắm giữ tối đa
- `buy_foreign_volume` (int64): Khối lượng mua ngoại
- `sell_foreign_volume` (int64): Khối lượng bán ngoại
- `buy_foreign_value` (int64): Giá trị mua ngoại
- `sell_foreign_value` (int64): Giá trị bán ngoại
- `total_buy_volume` (int64): Tổng khối lượng mua
- `total_sell_volume` (int64): Tổng khối lượng bán
- `total_deal_volume` (int64): Tổng khối lượng thỏa thuận

**Dữ liệu mẫu**

Shell

```bash
>>> company.trading_stats()
Shape: (1, 24)
>>> company.trading_stats()[['symbol', 'exchange', 'ev', 'foreign_holding_room']].head()
  symbol exchange              ev  ceiling  floor  reference  avg_match_price_1d
0    VCI     HOSE  29498470000000    37250  33950      35600           35600.00
```

## Tóm tắt tỷ lệ tài chính (Chỉ VCI)

**Gọi hàm**

Python

```python
company.ratio_summary()
```

**Tham số**

Không có

**Dữ liệu trả về**

DataFrame với 46 columns các chỉ số tài chính bao gồm:

**Chỉ số cơ bản:**

- `symbol` (object): Mã chứng khoán
- `year_report` (int64): Năm báo cáo

**Chỉ số doanh thu và lợi nhuận:**

- `revenue` (int64): Doanh thu
- `ebit` (int64): Lợi nhuận trước thuế và lãi vay
- `ebitda` (int64): EBITDA
- `net_profit_before_tax` (int64): Lợi nhuận trước thuế
- `net_profit_after_tax` (int64): Lợi nhuận sau thuế

**Chỉ số cân kế:**

- `total_assets` (int64): Tổng tài sản
- `total_equity` (int64): Vốn chủ sở hữu
- `total_liabilities` (int64): Tổng nợ
- `current_assets` (int64): Tài sản ngắn hạn
- `current_liabilities` (int64): Nợ ngắn hạn
- `inventory` (int64): Hàng tồn kho
- `receivables` (int64): Các khoản phải thu
- `cash_and_equivalents` (int64): Tiền và tương đương tiền
- `short_term_debt` (int64): Nợ ngắn hạn
- `long_term_debt` (int64): Nợ dài hạn

**Chỉ số trên mỗi cổ phiếu:**

- `book_value_per_share` (float64): Giá trị sổ sách trên mỗi cổ phiếu
- `eps` (float64): Lợi nhuận trên mỗi cổ phiếu

**Chỉ số sinh lời:**

- `roe` (float64): ROE
- `roa` (float64): ROA
- `roic` (float64): ROIC
- `gross_margin` (float64): Biên lợi nhuận gộp
- `ebitda_margin` (float64): Biên lợi nhuận EBITDA
- `ebit_margin` (float64): Biên lợi nhuận EBIT
- `net_margin` (float64): Biên lợi nhuận ròng

**Chỉ số hiệu quả hoạt động:**

- `asset_turnover` (float64): Vòng quay tài sản
- `equity_turnover` (float64): Vòng quay vốn chủ sở hữu

**Chỉ số thanh khoản:**

- `current_ratio` (float64): Tỷ lệ thanh khoản hiện hành
- `quick_ratio` (float64): Tỷ lệ thanh khoản nhanh

**Chỉ số đòn bẩy:**

- `debt_to_equity` (float64): D/E
- `debt_to_assets` (float64): Nợ trên tài sản
- `long_term_debt_to_equity` (float64): Nợ dài hạn trên vốn chủ sở hữu
- `interest_coverage` (float64): Tỷ lệ bao lãi

**Chỉ số định giá:**

- `pe` (float64): P/E
- `pb` (float64): P/B
- `ps` (float64): P/S
- `ev_to_ebitda` (float64): EV/EBITDA
- `ev_to_sales` (float64): EV/Sales
- `price_to_book` (float64): Giá trên giá trị sổ sách

**Chỉ số cổ tức:**

- `dividend_yield` (float64): Tỷ suất cổ tức
- `payout_ratio` (float64): Tỷ lệ trả cổ tức

**Chỉ số dòng tiền:**

- `fcf_yield` (float64): Tỷ suất dòng tiền tự do
- `fcf_margin` (float64): Biên lợi nhuận dòng tiền tự do
- `operating_cash_flow` (int64): Dòng tiền từ hoạt động kinh doanh
- `free_cash_flow` (int64): Dòng tiền tự do

**Dữ liệu mẫu**

Shell

```bash
>>> company.ratio_summary()
Shape: (1, 46)
>>> company.ratio_summary()[['symbol', 'year_report', 'revenue', 'ebit']].head()
  symbol  year_report        revenue          ebit
0    VCI         2025  1443289075867  716139241499
```

## Lưu ý quan trọng

1. **KBS là nguồn khuyến nghị**: Ổn định hơn VCI cho Google Colab/Kaggle
2. **Dữ liệu không đầy đủ**: Không phải công ty nào cũng có đầy đủ thông tin cho tất cả phương thức
3. **Giá trị rỗng**: Nếu không có dữ liệu, sẽ trả về DataFrame rỗng
4. **Phụ thuộc vào nguồn**: Thông tin khác nhau giữa KBS và VCI
5. **Methods riêng biệt**: KBS có ownership/capital\_history/insider\_trading, VCI có reports/trading\_stats/ratio\_summary

#### Tags

[thông tin công ty](https://vnstocks.com/blog/tag/thong-tin-cong-ty) [dữ liệu niêm yết](https://vnstocks.com/blog/tag/du-lieu-niem-yet) [danh sách niêm yết](https://vnstocks.com/blog/tag/danh-sach-niem-yet)

### Thảo luận

Đang tải bình luận...