---
url: "https://vnstocks.com/docs/vnstock/thong-tin-niem-yet"
title: "Thông tin niêm yết | Vnstock"
---

## Mục lục

Gợi ý

Bạn có thể tìm thấy ở đây danh sách tất cả các mã chứng khoán theo nhiều cách phân loại và từ tất cả các lớp tài sản khác nhau. Ngoài việc sử dụng tính năng này để tra cứu thông tin đơn thuần, danh sách mã chứng khoán trả về từ mục này còn được sử dụng cho các vòng lặp truy xuất dữ liệu. Đặc thù của các API do Vnstock được thiết kế để truy xuất thông tin cho từng mã chứng khoán riêng lẻ, việc này giúp tạo ra các "hàm nguyên tử" sử dụng trong việc xây dựng ứng dụng/hệ thống phân tích hoàn chỉnh. Do đó để truy xuất thông tin nhiều mã chứng khoán, bạn cần sử dụng các chương trình đặc thù để thực hiện tải dữ liệu hàng loạt. Tham gia gói tài trợ [Vnstock Insider](https://vnstocks.com/insiders-program) hoặc tham khảo khoá học [Python Vibe Coding - Python Vibe Coding với AI: Phân tích Dữ Liệu & Đầu Tư Chứng Khoán](https://vnstocks.com/khoa-hoc/lp-khoa-hoc-python-chung-khoan) đang mở nếu bạn mới làm quen và chưa rõ các thức thực hiện.

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/1_quickstart_stock_vietnam.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

Hướng dẫn sử dụng

**Notebook minh hoạ**: Dành cho người học data, muốn thực hành trực tiếp với các ví dụ mẫu.

**Agent Guide**: Dành cho người theo trường phái Vibe Coding, muốn viết chương trình hiệu quả với AI.

Để truy xuất danh sách chứng khoán niêm yết, bạn khởi động chương trình và tạo đối tượng `listing`.

Python

```python
from vnstock import Listing

# Khuyến nghị - Thích hợp cho Google Colab/Kaggle
listing = Listing(source='KBS')

# Hoặc sử dụng VCI (dữ liệu đầy đủ hơn nhưng không chạy được trên Colab)
listing = Listing(source='VCI')
```

## So sánh nguồn dữ liệu

| Phương thức | KBS | VCI | Ghi chú |
| --- | --- | --- | --- |
| **all\_symbols()** | ✅ | ✅ | KBS: 1557 mã, VCI: 1736 mã |
| **symbols\_by\_exchange()** | ✅ | ✅ | KBS: 6 cột, VCI: 7 cột |
| **symbols\_by\_industries()** | ✅ | ✅ | KBS: 3 cột, VCI: 10 cột |
| **symbols\_by\_group()** | ✅ | ✅ | Cả hai đều trả về Series |
| **industries\_icb()** | ❌ | ✅ | **Chỉ VCI có** (4 cột) |
| **all\_future\_indices()** | ✅ | ✅ | KBS: 14 mục, VCI: 8 mục |
| **all\_government\_bonds()** | ❌ | ✅ | **Chỉ VCI có** (6 mục) |
| **all\_covered\_warrant()** | ✅ | ✅ | Cả hai đều là Series (323 mục) |
| **all\_bonds()** | ✅ | ✅ | Cả hai đều là Series (82 mục) |

**Khuyến nghị:**

- **KBS**: Thích hợp dùng cho Google Colab/Kaggle
- **VCI**: Dữ liệu đầy đủ hơn, có ICB classification và nhiều chỉ số hơn. Thích hợp cài cục bộ trên máy hoặc dùng dịch vụ Cloud không thuộc Google.

## Cổ phiếu

Nguồn dữ liệu

KBS (khuyến nghị) hoặc VCI (Vietcap) có thể sử dụng cho phép truy xuất dữ liệu danh sách chứng khoán tại Việt Nam.

### Liệt kê tất cả mã chứng khoán

**Gọi hàm**

Python

```python
listing.all_symbols()
```

* * *

**Kết quả trả về**

DataFrame với 2 cột:

- `symbol` (object): Mã chứng khoán
- `organ_name` (object): Tên công ty đầy đủ

**Dữ liệu mẫu**

Shell

```bash
# KBS Source - Shape: (1557, 2)
>>> listing_kbs.all_symbols().head()
  symbol                                             organ_name
0    MTV  CTCP Dịch vụ Môi trường và Công trình Đô thị Vũng Tàu
1    HHN                CTCP Vận tải và Dịch vụ Hàng hóa Hà Nội
2    PDB                       CTCP Tập đoàn Đầu tư Din Capital

# VCI Source - Shape: (1736, 2)
>>> listing_vci.all_symbols().head()
  symbol                                                 organ_name
0    YTC  Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố Hồ Chí Minh
1    YEG                             Công ty Cổ phần Tập đoàn Yeah1
2    YBM             Công ty Cổ phần Khoáng sản Công nghiệp Yên Bái
```

**Kiểu dữ liệu chi tiết**

Shell

```bash
# KBS Source
RangeIndex: 1557 entries, 0 to 1556
Data columns (total 2 cột):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   symbol      1557 non-null   object
 1   organ_name  1557 non-null   object

# VCI Source
RangeIndex: 1736 entries, 0 to 1735
Data columns (total 2 cột):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   symbol      1736 non-null   object
 1   organ_name  1736 non-null   object
```

### Liệt kê mã chứng khoán theo sàn

**Gọi hàm**

Python

```python
listing.symbols_by_exchange(exchange='HOSE')
```

**Tham số**

- `exchange`(str): Sàn giao dịch

  - `'HOSE'`: Sàn giao dịch Chứng khoán TP.HCM
  - `'HNX'`: Sàn giao dịch Chứng khoán Hà Nội
  - `'UPCOM'`: Sàn giao dịch Chứng khoán chưa niêm yết

**Kết quả trả về**

**KBS Source (6 cột):**

- `symbol` (object): Mã chứng khoán
- `organ_name` (object): Tên công ty đầy đủ
- `en_organ_name` (object): Tên công ty tiếng Anh
- `exchange` (object): Sàn giao dịch
- `type` (object): Loại chứng khoán (stock)
- `id` (int64): ID định danh

**VCI Source (7 cột):**

- `symbol` (object): Mã chứng khoán
- `exchange` (object): Sàn giao dịch
- `type` (object): Loại chứng khoán (STOCK)
- `organ_short_name` (object): Tên viết tắt
- `organ_name` (object): Tên công ty đầy đủ
- `product_grp_id` (object): ID nhóm sản phẩm
- `icb_code2` (object): Mã ICB level 2

**Dữ liệu mẫu**

Shell

```bash
# KBS Source - Shape: (1998, 6)
>>> listing_kbs.symbols_by_exchange(exchange='HOSE').head()
  symbol                                             organ_name  \
0    MTV  CTCP Dịch vụ Môi trường và Công trình Đô thị Vũng Tàu
1    HHN                CTCP Vận tải và Dịch vụ Hàng hóa Hà Nội
2    PDB                       CTCP Tập đoàn Đầu tư Din Capital

                                   en_organ_name exchange   type  id
0  Vung Tau Environment Services and Urban Project Joint Stock Company    UPCOM  stock   1
1             Ha Noi Goods Services and Transport Joint Stock Company    UPCOM  stock   1
2                   Din Capital Investment Group Joint Stock Company      HNX  stock   1

# VCI Source - Shape: (3270, 7)
>>> listing_vci.symbols_by_exchange(exchange='HOSE').head()
  symbol exchange   type       organ_short_name  \
0    YTC    UPCOM  STOCK        XNK Y tế TP.HCM
1    YEG      HSX  STOCK         Tập đoàn Yeah1
2    YBM      HSX  STOCK  Khoáng sản CN Yên Bái

                                         organ_name product_grp_id icb_code2
0  Công ty Cổ phần Xuất nhập khẩu Y tế Thành phố Hồ Chí Minh            UPX      4500
1                     Công ty Cổ phần Tập đoàn Yeah1            STO      5500
2     Công ty Cổ phần Khoáng sản Công nghiệp Yên Bái            STO      1700
```

### Liệt kê chứng khoán theo phân nhóm

Liệt kê tất cả mã chứng khoán theo nhóm phân loại:

- **VN30, VN100, HNX30**: Các chỉ số vốn hóa
- **VNMidCap, VNSmallCap, VNAllShare**: Phân loại vốn hóa
- **VNIT, VNIND, VNCONS, VNCOND, VNHEAL, VNENE**: Các chỉ số ngành
- **ETF**: Chứng chỉ quỹ
- **FU\_INDEX**: Hợp đồng tương lai
- **CW**: Chứng quyền có bảo đảm

**Gọi hàm**

Python

```python
listing.symbols_by_group(group_name='VN30')
```

**Tham số**

- `group_name` (str): Tên nhóm chỉ số

**Kết quả trả về**

Series chứa danh sách mã chứng khoán thuộc nhóm.

**Dữ liệu mẫu**

Shell

```bash
# Cả KBS và VCI đều trả về Series với 30 mã VN30
>>> listing.symbols_by_group(group_name='VN30')
0     ACB
1     BCM
2     BID
3     CTG
4     DGC
5     FPT
6     GAS
7     GVR
8     HDB
9     HPG
10    LPB
11    MBB
12    MSN
13    MWG
14    PLX
15    SAB
16    SHB
17    SSB
18    SSI
19    STB
20    TCB
21    TPB
22    VCB
23    VHM
24    VIB
25    VIC
26    VJC
27    VNM
28    VPB
29    VRE
Name: symbol, dtype: object
```

**Kiểu dữ liệu chi tiết**

Shell

```bash
<class 'pandas.core.series.Series'>
RangeIndex: 30 entries, 0 to 29
Series name: symbol
Non-Null Count  Dtype
--------------  -----
30 non-null     object
dtypes: object(1)
memory usage: 368.0+ bytes
```

### Chứng khoán theo ngành

**Gọi hàm**

Python

```python
listing.symbols_by_industries()
```

**Kết quả trả về**

**KBS Source (3 cột):**

- `symbol` (object): Mã chứng khoán
- `industry_code` (int64): Mã ngành
- `industry_name` (object): Tên ngành

**VCI Source (10 cột):**

- `symbol` (object): Mã chứng khoán
- `organ_name` (object): Tên công ty
- `icb_name3`, `icb_name2`, `icb_name4` (object): Tên ngành theo các cấp ICB
- `com_type_code` (object): Mã loại công ty
- `icb_code1`, `icb_code2`, `icb_code3`, `icb_code4` (object): Mã ICB theo các cấp

**Dữ liệu mẫu**

Shell

```bash
# KBS Source - Shape: (697, 3)
>>> listing_kbs.symbols_by_industries().head()
  symbol  industry_code    industry_name
0    AMC             10          Khai khoáng
1    BKC             10          Khai khoáng
2    BMC             10          Khai khoáng
3    CMC             10          Khai khoáng
4    DRC             10          Khai khoáng

# VCI Source - Shape: (1561, 10)
>>> listing_vci.symbols_by_industries().head()
  symbol                                      organ_name             icb_name3  \
0    BQP  Công ty Cổ phần Nhựa chất lượng cao Bình Thuận              Hóa chất
1    VLS         Công ty Cổ phần Sản xuất Thép Việt Long              Kim loại
2    RYG    Công ty Cổ phần Sản xuất và Đầu tư Hoàng Gia  Xây dựng và Vật liệu

         icb_name2                     icb_name4 com_type_code icb_code1 icb_code2 icb_code3 icb_code4
0        Hóa chất            Nhựa, cao su & sợi            CT      1000      1300      1350      1353
1  Tài nguyên Cơ bản         Thép và sản phẩm thép            CT      1000      1700      1750      1757
2  Xây dựng và Vật liệu  Vật liệu xây dựng & Nội thất            CT      2000      2300      2350      2353
```

### Phân loại ngành ICB (Chỉ VCI)

Gợi ý

ICB (Industry Classification Benchmark) là hệ thống phân ngành tiêu chuẩn quốc tế, được phát triển bởi Dow Jones và FTSE. Chỉ có VCI cung cấp dữ liệu ICB đầy đủ. KBS không hỗ trợ phương thức này.

**Gọi hàm**

Python

```python
listing.industries_icb()
```

**Kết quả trả về**

DataFrame với 4 cột:

- `icb_name` (object): Tên ngành tiếng Việt
- `en_icb_name` (object): Tên ngành tiếng Anh
- `icb_code` (object): Mã ICB
- `level` (int64): Cấp phân loại (1-4)

**Dữ liệu mẫu**

Shell

```bash
# VCI Source - Shape: (155, 4)
>>> listing_vci.industries_icb().head()
                                 icb_name                             en_icb_name icb_code  level
0                        Sản xuất Dầu khí                     Oil & Gas Producers     0530      3
1  Thiết bị, Dịch vụ và Phân phối Dầu khí  Oil Equipment, Services & Distribution     0570      3
2                                  Hóa chất                               Chemicals     1350      3
3                        Lâm nghiệp và Giấy                        Forestry & Paper     1730      3
4                                  Kim loại              Industrial Metals & Mining     1750      3

>>> listing_vci.industries_icb().tail()
                    icb_name           en_icb_name icb_code  level
150                 Ngân hàng                  Banks     8300      2
151                  Bảo hiểm              Insurance     8500      2
151              Bất động sản            Real Estate     8600      2
152         Dịch vụ tài chính     Financial Services     8700      2
153       Công nghệ Thông tin             Technology     9500      2
```

**Kiểu dữ liệu chi tiết**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 155 entries, 0 to 154
Data columns (total 4 cột):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   icb_name     155 non-null    object
 1   en_icb_name  155 non-null    object
 2   icb_code     155 non-null    object
 3   level        155 non-null    int64
dtypes: int64(1), object(3)
memory usage: 5.0+ KB
```

## Chỉ số thị trường

Gợi ý

Các chỉ số thị trường cung cấp thông tin về các chỉ số chuẩn hóa từ nhiều nguồn dữ liệu khác nhau, bao gồm HOSE, HNX và các chỉ số ngành. Điều này giúp bạn phân tích xu hướng thị trường và lọc dữ liệu theo ngành.

### Liệt kê tất cả chỉ số

**Gọi hàm**

Python

```python
listing.all_indices()
```

**Dữ liệu mẫu:**

Shell

```bash
>>> listing.all_indices()
         symbol         name                                        description  ...               group index_id  sector_id
0          VN30         VN30  30 cổ phiếu vốn hóa lớn nhất & thanh khoản tốt...  ...        HOSE Indices        5        NaN
1         VNMID        VNMID   Mid-Cap Index - nhóm cổ phiếu vốn hóa trung bình  ...        HOSE Indices        6        NaN
2         VNSML        VNSML        Small-Cap Index - nhóm cổ phiếu vốn hóa nhỏ  ...        HOSE Indices        7        NaN
3         VN100        VN100              100 cổ phiếu có vốn hoá lớn nhất HOSE  ...        HOSE Indices        8        NaN
4         VNALL        VNALL                   Tất cả cổ phiếu trên HOSE và HNX  ...        HOSE Indices        9        NaN
5          VNSI         VNSI                            Vietnam Small-Cap Index  ...        HOSE Indices       21        NaN
6          VNIT         VNIT                                Công nghệ thông tin  ...      Sector Indices       10      159.0
7         VNIND        VNIND                                        Công nghiệp  ...      Sector Indices       11      155.0
8        VNCONS       VNCONS                                     Hàng tiêu dùng  ...      Sector Indices       12      130.0
9        VNCOND       VNCOND                           Hàng tiêu dùng thiết yếu  ...      Sector Indices       13      133.0
10       VNHEAL       VNHEAL                                  Chăm sóc sức khoẻ  ...      Sector Indices       14      135.0
11        VNENE        VNENE                                         Năng lượng  ...      Sector Indices       15      154.0
12        VNUTI        VNUTI                                   Dịch vụ tiện ích  ...      Sector Indices       16      150.0
13       VNREAL       VNREAL                                       Bất động sản  ...      Sector Indices       17      166.0
14        VNFIN        VNFIN                                          Tài chính  ...      Sector Indices       18      138.0
15        VNMAT        VNMAT                                    Nguyên vật liệu  ...      Sector Indices       19      143.0
16    VNDIAMOND    VNDIAMOND  Chỉ số các cổ phiếu có triển vọng lớn của doan...  ...  Investment Indices        2        NaN
17    VNFINLEAD    VNFINLEAD  Chỉ số của các cổ phiếu thuộc nhóm ngành tài c...  ...  Investment Indices        3        NaN
18  VNFINSELECT  VNFINSELECT  Chỉ số của các cổ phiếu đại diện cho ngành tài...  ...  Investment Indices        4        NaN
19        VNX50        VNX50  50 cổ phiếu vốn hóa lớn nhất trên toàn bộ thị ...  ...         VNX Indices        4        NaN
20       VNXALL       VNXALL  Tất cả cổ phiếu trên toàn bộ thị trường HOSE v...  ...         VNX Indices        1        NaN

[21 rows x 7 cột]
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 21 entries, 0 to 20
Data columns (total 7 cột):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   symbol       21 non-null     object
 1   name         21 non-null     object
 2   description  21 non-null     object
 3   full_name    21 non-null     object
 4   group        21 non-null     object
 5   index_id     21 non-null     int64
 6   sector_id    10 non-null     float64
```

### Liệt kê chỉ số theo nhóm

Các nhóm chỉ số có sẵn bao gồm:

- **HOSE Indices**: Các chỉ số chính của sàn HOSE (VN30, VN100, v.v.)
- **Sector Indices**: Các chỉ số ngành (VNIT, VNIND, VNCONS, v.v.)
- **Investment Indices**: Các chỉ số đầu tư (VNDIAMOND, VNFINLEAD, v.v.)
- **VNX Indices**: Các chỉ số của sàn HNX (VNX50, VNXALL)

**Gọi hàm**

Python

```python
listing.indices_by_group('HOSE Indices')
```

**Dữ liệu mẫu:**

Shell

```bash
>>> listing.indices_by_group('HOSE Indices')
  symbol   name                                        description         full_name         group  index_id
0   VN30   VN30  30 cổ phiếu vốn hóa lớn nhất & thanh khoản tốt...        VN30 Index  HOSE Indices         5
1  VNMID  VNMID   Mid-Cap Index - nhóm cổ phiếu vốn hóa trung bình    VNMidCap Index  HOSE Indices         6
2  VNSML  VNSML        Small-Cap Index - nhóm cổ phiếu vốn hóa nhỏ  VNSmallCap Index  HOSE Indices         7
3  VN100  VN100              100 cổ phiếu có vốn hoá lớn nhất HOSE       VN100 Index  HOSE Indices         8
4  VNALL  VNALL                   Tất cả cổ phiếu trên HOSE và HNX       VNAll Index  HOSE Indices         9
5   VNSI   VNSI                            Vietnam Small-Cap Index        VNSI Index  HOSE Indices        21
```

**Kiểu dữ liệu**

Shell

```bash
RangeIndex: 6 entries, 0 to 5
Data columns (total 6 cột):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   symbol       6 non-null      object
 1   name         6 non-null      object
 2   description  6 non-null      object
 3   full_name    6 non-null      object
 4   group        6 non-null      object
 5   index_id     6 non-null      int64
```

## FX, Crypto, Chỉ số thế giới

### Tìm mã chứng khoán quốc tế

Gợi ý

Để tìm kiếm mã chứng khoán `symbol_id` cho thị trường quốc tế và sử dụng cho việc tra cứu giá trong trường hợp mã chứng khoán. bạn tìm kiếm chưa được thêm vào danh sách hỗ trợ chính thức qua lớp hàm Vnstock, bạn có thể sử dụng cách gọi hàm từ các hàm cốt lõi của hệ thống. Thông tin `symbol_id` được sử dụng để tra cứu thông tin các mã chứng khoán trong trường hợp bạn muốn "vọc" sâu vào lớp hàm cốt lõi của Vnstock tại `vnstock3.explorer.msn.quote`

**Gọi hàm**

Python

```python
from vnstock.explorer.msn.listing import Listing
Listing().search_symbol_id('USD')
```

**Dữ liệu mẫu:**

Shell

```bash
>>> from vnstock.explorer.msn.listing import Listing
>>> Listing().search_symbol_id('USD')

                symbol symbol_id exchange_name  exchange_code_mic  ...                                           eng_name description                                         local_name locale
0                  USD    a2521h     NYSE ARCA               ARCX  ...                     ProShares Ultra Semiconductors                                 ProShares Ultra Semiconductors  en-us
1                  USD    aaa5bh     Australia               XASX  ...                           BetaShares US Dollar ETF                                       BetaShares US Dollar ETF  en-au
2             SPRPUS8P    buam8m                  INDX_DEFAULT-SP  ...  S&P Risk Parity Index (USD-Only Constituents) ...              S&P Risk Parity Index (USD-Only Constituents) ...  en-us
3  SPCRR2B10BCPKUSD.TR    bp2ic7                    INDX_24HRS-SP  ...                  S&P Pak USD2 Bil and USD10 Bil GR                              S&P Pak USD2 Bil and USD10 Bil GR  en-us
4              RGAHU_T    bxyrec                INDX_DEFAULT-FTSE  ...  FTSE EPRA Nareit Developed ex Australia hedged...              FTSE EPRA Nareit Developed ex Australia hedged...  en-gb
5     SPCRR2B10BCCOUSD    bkn7u2                    INDX_24HRS-SP  ...                     S&P Col USD2 Bil and USD10 Bil                                 S&P Col USD2 Bil and USD10 Bil  en-us
6             FGCICUHN    bxwl5r                INDX_DEFAULT-FTSE  ...  FTSE Global Core Infrastructure 50/50 100% Hed...              FTSE Global Core Infrastructure 50/50 100% Hed...  en-gb
7             GPPS008U    blhayc                  INDX_24HRS-FTSE  ...  FTSE Japan 100% Hedged to USD Net Tax (US RIC)...              FTSE Japan 100% Hedged to USD Net Tax (US RIC)...  en-gb
8        SPCRU2BRLAUSD    c4yww7                  INDX_DEFAULT-SP  ...         S&P Latin America Under USD2 Billion (USD)                     S&P Latin America Under USD2 Billion (USD)  en-us
9              RLHAU_T    bxyvh7                INDX_DEFAULT-FTSE  ...  FTSE EPRA Nareit Australia hedged in USD Net R...              FTSE EPRA Nareit Australia hedged in USD Net R...  en-gb

[10 rows x 10 cột]
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 10 cột):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   symbol             10 non-null     object
 1   symbol_id          10 non-null     object
 2   exchange_name      10 non-null     object
 3   exchange_code_mic  10 non-null     object
 4   short_name         10 non-null     object
 5   friendly_name      10 non-null     object
 6   eng_name           10 non-null     object
 7   description        10 non-null     object
 8   local_name         10 non-null     object
 9   locale             10 non-null     object
dtypes: object(10)
memory usage: 928.0+ bytes
```

#### Tags

[thông tin niêm yết](https://vnstocks.com/blog/tag/thong-tin-niem-yet) [danh sách niêm yết](https://vnstocks.com/blog/tag/danh-sach-niem-yet) [thông tin công ty](https://vnstocks.com/blog/tag/thong-tin-cong-ty)

### Thảo luận

Đang tải bình luận...