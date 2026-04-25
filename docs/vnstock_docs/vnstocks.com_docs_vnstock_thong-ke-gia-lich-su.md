---
url: "https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su"
title: "Thống kê giá lịch sử | Vnstock"
---

## Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/1_quickstart_stock_vietnam.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

Hướng dẫn sử dụng

**Notebook minh hoạ**: Dành cho người học data, muốn thực hành trực tiếp với các ví dụ mẫu.

**Agent Guide**: Dành cho người theo trường phái Vibe Coding, muốn viết chương trình hiệu quả với AI.

## So sánh nguồn dữ liệu

| Phương thức | KBS | VCI | Ghi chú |
| --- | --- | --- | --- |
| **history()** | ✅ | ✅ | Cả hai đều hỗ trợ OHLCV |
| **intraday()** | ✅ | ✅ | Cả hai đều hoạt động (5 cột) |
| **price\_depth()** | ❌ | ❌ | Đã bị loại bỏ trong v3.4.2 |

**Khuyến nghị:**

- **KBS**: Thích hợp cho Google Colab/Kaggle.
- **VCI**: Dữ liệu đầy đủ hơn, linh hoạt hơn. Thích hợp cài cục bộ trên máy hoặc dùng dịch vụ Cloud không thuộc Google.

## Chứng khoán Việt Nam

Gợi ý

Các hàm tra cứu thông tin giá lịch sử tại Vnstock sử dụng dữ liệu trực tiếp từ dữ liệu công khai của công ty chứng khoán cho thị trường Việt Nam. Dữ liệu trả về là dữ liệu thời gian thực trong giờ giao dịch.

Hiện tại bạn có thể lựa chọn nguồn dữ liệu `VCI` hoặc `KBS` để truy xuất thông tin giá lịch sử và dữ liệu khớp lệnh mã chứng khoán (cổ phiếu, hợp đồng tương lai, chứng quyền, trái phiếu) bất kỳ.

Python

```python
from vnstock import Quote

# Khuyến nghị - Thích hợp cho Google Colab/Kaggle
quote = Quote(symbol='VCI', source='KBS')

# Hoặc VCI - Dữ liệu đầy đủ hơn nhưng không chạy được trên Colab
quote = Quote(symbol='VCI', source='VCI')
```

Danh sách các loại chứng khoán được hỗ trợ:

- **Cổ phiếu:** xem tại mục [Liệt kê tất cả mã cổ phiếu](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#liet-ke-tat-ca-ma-cp)
- **Chỉ số:**`VNINDEX`, `HNXINDEX`, `UPCOMINDEX`, `VN30`, `HNX30`
- **Hợp đồng tương lai**: Chấp nhận cả hai kiểu nhập tên là`VN30F1M` và `VN30F2411`
- **Chứng quyền**: `CFPT2314`
- **Trái phiếu niêm yết**: `CII424002` (hiện tại chỉ nguồn VCI hỗ trợ)
- **Chứng chỉ quỹ - ETF**: Tra cứu như với mã cổ phiếu, ví dụ `E1VFVN30`

Chi tiết các mã chứng khoán thuộc từng loại kể trên có thể được tra cứu tại mục Danh sách niêm yết - [Liệt kê CP theo phân nhóm](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#liet-ke-cp-theo-phan-nhom)

### Giá lịch sử (OHLCV)

Gợi ý

Dữ liệu giá lịch sử thể hiện lịch sử giá giao dịch (đã điều chỉnh) của mã chứng khoán bất kỳ. Đây là dữ liệu được sử dụng để biểu diễn đồ thị kỹ thuật với định dạng tiêu chuẩn OHLCV (Open, High, Low, Close, Volume).

**Gọi hàm**

Python

```python
# Lấy 1 tháng gần nhất
quote.history(length="1M", interval="1D")

# Hoặc lấy theo khoảng thời gian cụ thể
quote.history(start='2024-01-01', end='2024-05-25', interval="1D")
```

**Tham số**

**Cả KBS và VCI:**

- `start` (str): Ngày bắt đầu (YYYY-MM-DD). Bắt buộc nếu không có length
- `end` (str): Ngày kết thúc (YYYY-MM-DD). Mặc định None (hiện tại)
- `interval` (str): Khung thời gian. Mặc định "1D"
- `length` (str/int): Khoảng thời gian lùi lại từ hiện tại hoặc số nến

**KBS thêm:**

- `get_all` (bool): Lấy tất cả các cột. Mặc định False

**Khung thời gian hỗ trợ:**

- `"1m"`: 1 phút
- `"5m"`: 5 phút
- `"15m"`: 15 phút
- `"30m"`: 30 phút
- `"1H"`: 1 giờ
- `"1D"`: 1 ngày
- `"1W"`: 1 tuần
- `"1M"`: 1 tháng

**Định dạng length linh hoạt:**

- Chu kỳ: `"1M"`, `"3M"`, `"1Y"` (tháng, quý, năm)
- Số ngày: `150`, `"150"`
- Số nến: `"100b"`, `"50b"`

**Dữ liệu mẫu**

**KBS Source:**

Shell

```bash
>>> quote_kbs.history(length="1M", interval="1D")

                 time     open     high      low    close    volume
0  2026-01-05 07:00:00  34791.0  34889.0  33115.0  33460.0  10463000
1  2026-01-06 07:00:00  33608.0  34101.0  33066.0  33509.0   7681400
2  2026-01-07 07:00:00  33953.0  34594.0  33608.0  34150.0   5883700

[20 rows x 6 columns]
```

**VCI Source:**

Shell

```bash
>>> quote_vci.history(length="1M", interval="1D")

        time   open   high    low  close   volume
0  2025-12-29  35.09  35.73  34.79  34.79  6892857
1  2025-12-30  35.28  35.58  34.79  34.89  6366199
2  2025-12-31  34.99  35.38  34.50  34.79  8097918

[23 rows x 6 columns]
```

**Thuộc tính dữ liệu**
Bạn có thể truy xuất thông tin thuộc tính của dữ liệu trả về với 2 thông tin sau:

- `name`: Tên mã chứng khoán
- `category`: Tên loại tài sản mã chứng khoán đó thuộc về.

Python

```python
>>> df.name
'VCI'
>>> df.category
'stock'
```

**Kiểu dữ liệu**

**KBS Source:**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 20 entries, 0 to 19
Data columns (total 6 cột):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   time    20 non-null    datetime64[ns]
 1   open    20 non-null    float64
 2   high    20 non-null    float64
 3   low     20 non-null    float64
 4   close   20 non-null    float64
 5   volume  20 non-null    int64
dtypes: datetime64[ns](1), float64(4), int64(1)
memory usage: 1.1 KB
```

**VCI Source:**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 23 entries, 0 to 22
Data columns (total 6 cột):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   time    23 non-null    datetime64[ns]
 1   open    23 non-null    float64
 2   high    23 non-null    float64
 3   low     23 non-null    float64
 4   close   23 non-null    float64
 5   volume  23 non-null    int64
dtypes: datetime64[ns](1), float64(4), int64(1)
memory usage: 1.2 KB
```

Có thể bạn chưa biết

Dữ liệu giá lịch sử cho đồ thị nến (ohlcv) là dữ liệu sinh ra từ phép lấy mẫu theo tần suất thời gian được chỉ định (ví dụ 1 phút hay 1 ngày) trên cơ sở dữ liệu khớp lệnh (intraday). Phép tổng hợp được sử dụng như sau:

- `open`: mốc thời gian quan sát sớm nhất. Sử dụng phép tổng hợp `first()`.
- `close`: mốc thời gian quan sát sau cùng. Sử dụng phép tổng hợp `last()`.
- `high`: giá cao nhất. Sử dụng phép tổng hợp `max()`
- `low`: giá thấp nhất. Sử dụng phép tổng hợp `min()`

Dữ liệu được trả về từ hàm `history()` là dữ liệu đã tổng hợp sẵn, có điều chỉnh khi có sự kiện quyền (chia tách, trả cổ tức cổ phiếu), được cung cấp bởi công ty chứng khoán/dịch vụ cung cấp dữ liệu.

Hiểu bản chất của dữ liệu, giúp bạn tuỳ biến và phân tích một cách linh hoạt. Nếu những nội dung này mới lạ với bạn, [khoá học](https://vnstocks.com/lp-khoa-hoc-python-chung-khoan/) mà dự án Vnstock x LEarn Anything cung cấp sẽ hữu ích để bạn hiểu hơn về dữ liệu trên thị trường chứng khoán và cách sử dụng chúng hiệu quả.

### Dữ liệu khớp lệnh (Intraday)

Gợi ý

Dữ liệu intraday thể hiện giao dịch khớp lệnh trong phiên có độ chính xác đến hàng giây theo thời gian thực khi truy cứu trong khung giờ giao dịch 9:00 - 15:00 hàng ngày. Độ lớn của số điểm dữ liệu giao dịch mỗi ngày cho các mã chứng khoán lớn có thể lên đến ~15,000 dòng cho 1 ngày.

**Gọi hàm**

Python

```python
quote.intraday(page_size=100)
```

**Tham số**

**KBS:**

- `page_size` (int): Số bản ghi muốn lấy về. Mặc định 100, có thể tăng lên 150\_000 nếu mã có thanh khoản lớn hoặc hợp đồng tương lai VN30.
- `get_all` (bool): Lấy tất cả các cột. Mặc định False

**VCI:**

- `page_size` (int): Số bản ghi muốn lấy về. Mặc định 100. có thể tăng lên 150\_000 nếu mã có thanh khoản lớn hoặc hợp đồng tương lai VN30.
- `last_time` (str/int/float): Thời gian cắt dữ liệu
- `last_time_format` (str): Định dạng của last\_time

**Dữ liệu mẫu**

**KBS Source:**

Shell

```bash
>>> quote_kbs.intraday(page_size=5)

                 time  price  volume match_type                              id
4 2026-01-30 14:29:59  103.9    1800       sell  2026-01-30_142959_1039000_1800
3 2026-01-30 14:30:00  103.9    1900       sell  2026-01-30_143000_1039000_1900

[5 rows x 5 columns]
```

**VCI Source:**

Shell

```bash
>>> quote_vci.intraday(page_size=5)

                       time  price  volume match_type         id
0 2026-01-30 14:29:59+07:00  103.9     100       Sell  429968774
1 2026-01-30 14:29:59+07:00  103.9     500       Sell  429968773

[5 rows x 5 columns]
```

**Ý nghĩa các cột dữ liệu**

- `time` (datetime64\[ns\]): Thời gian diễn ra giao dịch khớp lệnh
- `price` (float64): Giá thực hiện của giao dịch khớp lệnh
- `volume` (int64): Khối lượng của giao dịch khớp lệnh
- `match_type` (object): Loại giao dịch khớp lệnh (Buy/Sell)
- `id` (object): Mã định danh duy nhất của giao dịch khớp lệnh

Giải thích thuật ngữ

- `time`: thời gian khớp lệnh. Bắt đầu từ 9:15 đến 14:45 trong ngày giao dịch.
- `price`: Mức giá của giao dịch mua/bán được khớp lệnh.
- `volume`: Khối lượng giao dịch của lệnh mua/bán được khớp.
- `match_type`: Loại giao dịch được mua/bán.
- `id`: mã giao dịch. Thông tin này sử dụng làm mốc để ghép nối dữ liệu nếu thực hiện truy xuất dữ liệu từng phần.

Có thể bạn chưa biết

Từ giá trị giao dịch được tính toán thông qua giá và khối lượng giao dịch, có thể ước lượng và phân loại nhà đầu tư. Đây cũng là cách một số website chứng khoán sử dụng để phân cấp \`Cá mập\`, \`Sói già\`, \`Cừu non\`.

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
Index: 100 entries, 99 to 0
Data columns (total 5 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   time        100 non-null    datetime64[ns]
 1   price       100 non-null    float64
 2   volume      100 non-null    int64
 3   match_type  100 non-null    object
 4   id          100 non-null    object
dtypes: datetime64[ns](1), float64(1), int64(1), object(2)
memory usage: 4.7+ KB
```

## Chứng khoán quốc tế

Trước khi gọi hàm và truy xuất dữ liệu theo các cú pháp thuộc từng mục bên dưới, bạn chắc chắn rằng đã gọi Vnstock class từ thư viện vnstock. Dữ liệu chỉ có khung thời gian cuối ngày, tức mặc định là `interval='1D'`.

Python

```python
from vnstock import Vnstock
```

Hai cách truy xuất dữ liệu

Có 2 hình thức truy xuất dữ liệu từ hàm của Vnstock cho nhóm dữ liệu này:

1. Gọi theo các hàm từ Vnstock class như dưới đây tại các mục [Forex](https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su#forex-fx), [Crypto](https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su#crypto), [Chỉ số quốc tế](https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su#chi-so-quoc-te). Cách này hạn chế số mã có thể được tra cứu vì danh sách phân loại sẵn để chuyển đổi giữa tên symbol và mã tra cứu từ nguồn dữ liệu không đầy đủ. Tuy nhiên đây là cách dùng tiện lợi và tự nhiên nhất bạn nên dùng. Đối với các mã chứng khoán bạn cần tìm không được hỗ trợ sẵn, hãy làm theo cách thứ 2.
2. Gọi theo hàm `quote` từ lõi phần mềm, sử dụng nguồn `msn`.





















Python









```python
from vnstock.explorer.msn.quote import *
quote = Quote(symbol_id='avyufr')
quote.history(start='2020-01-01', end='2024-12-31')
```



Trong đó, `symbol_id` là mã định danh tương ứng từng `symbol` được chỉ định bởi MSN, bạn có thể tra cứu mã này với cú pháp:





















Python









```python
from vnstock.explorer.msn.listing import Listing
Listing().search_symbol_id('USD')
```


### Forex (FX)

**Gọi hàm**

Python

```python
fx = Vnstock().fx(symbol='JPYVND', source='MSN')
fx.quote.history(start='2024-02-28', end='2024-05-25')
```

**Tham số**

- `symbol`: Mã cặp tiền tệ cần tra cứu. Hiện tại hàm hỗ trợ truy xuất dữ liệu trực tiếp cho các cặp tiền tệ sau:`USDVND`, `JPYVND`, `AUDVND`, `CNYVND`, `KRWVND`, `USDJPY`, `USDEUR`, `USDCAD`, `USDCHF`, `USDCNY`, `USDKRW`, `USDSGD`, `USDHKD`, `USDTRY`, `USDINR`, `USDDKK`, `USDSEK`, `USDILS`, `USDRUB`, `USDMXN`, `USDZAR`, `EURUSD`, `EURVND`, `EURJPY`, `EURGBP`, `EURCHF`, `EURCAD`, `EURAUD`, `EURNZD`, `GBPJPY`, `GBPVND`, `GBPUSD`, `GBPAUD`, `GBPCHF`, `GBPNZD`, `GBPCAD`, `AUDUSD`, `NZDUSD`.
- `start`: Ngày kết thúc của truy vấn dữ liệu lịch sử. Định dạng `YYYY-mm-dd`
- `end`: Ngày kết thúc của truy vấn dữ liệu lịch sử. Định dạng `YYYY-mm-dd`
- `interval` (tuỳ chọn): Khung thời gian lấy mẫu dữ liệu. Chỉ hỗ trợ giá trị "1D" để lấy dữ liệu cuối ngày.

**Dữ liệu mẫu:**

Shell

```bash
>>> fx.quote.history(start='2024-02-28', end='2024-05-25')

         time    open    high     low   close
0  2024-02-28  163.60  163.88  163.20  163.37
1  2024-02-29  163.37  165.13  163.36  164.28
2  2024-03-01  164.28  164.30  163.45  164.12
3  2024-03-04  164.15  164.43  163.76  163.92
4  2024-03-05  163.92  164.92  163.76  164.55
..        ...     ...     ...     ...     ...
58 2024-05-20  163.54  163.68  162.80  162.87
59 2024-05-21  162.87  163.37  162.47  163.02
60 2024-05-22  163.00  163.09  162.34  162.40
61 2024-05-23  162.40  162.70  162.01  162.28
62 2024-05-24  162.27  162.37  162.03  162.18

[63 rows x 5 columns]
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 63 entries, 0 to 62
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   time    63 non-null     datetime64[ns]
 1   open    63 non-null     float64
 2   high    63 non-null     float64
 3   low     63 non-null     float64
 4   close   63 non-null     float64
dtypes: datetime64[ns](1), float64(4)
memory usage: 2.6 KB
```

### Crypto

**Gọi hàm**

Python

```python
crypto = Vnstock().crypto(symbol='BTC', source='MSN')
crypto.quote.history(start='2023-01-01', end='2024-12-31')
```

**Tham số**

- `symbol`: Mã crypto bạn cần tra cứu. Hiện tại hỗ trợ các mã sau: `BTC`, `ETH`, `USDT`, `USDC`, `BNB`, `BUSD`, `XRP`, `ADA`, `SOL`, `DOGE`
- `start`: Ngày kết thúc của truy vấn dữ liệu lịch sử. Định dạng `YYYY-mm-dd`
- `end`: Ngày kết thúc của truy vấn dữ liệu lịch sử. Định dạng `YYYY-mm-dd`
- `interval` (tuỳ chọn): Khung thời gian lấy mẫu dữ liệu. Chỉ hỗ trợ giá trị "1D" để lấy dữ liệu cuối ngày.

**Dữ liệu mẫu:**

Shell

```bash
>>> crypto.quote.history(start='2023-01-01', end='2024-12-31')

          time          open          high           low         close            volume
151 2023-01-07  4.284546e+08  4.324123e+08  4.253995e+08  4.313937e+08   366798893802898
152 2023-02-06  5.937590e+08  5.960796e+08  5.812771e+08  5.841758e+08   497871354777384
153 2023-03-08  5.707559e+08  5.732777e+08  5.601426e+08  5.654487e+08   579335227686628
154 2023-04-07  7.170032e+08  7.170835e+08  7.058959e+08  7.136673e+08   352144573109365
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
Index: 17 entries, 151 to 167
Data columns (total 6 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   time    17 non-null     datetime64[ns]
 1   open    17 non-null     float64
 2   high    17 non-null     float64
 3   low     17 non-null     float64
 4   close   17 non-null     float64
 5   volume  17 non-null     int64
dtypes: datetime64[ns](1), float64(4), int64(1)
memory usage: 952.0 bytes
```

### Chỉ số quốc tế

**Gọi hàm**

Python

```python
index = Vnstock().world_index(symbol='DJI', source='MSN')
index.quote.history(start='2023-01-01', end='2024-12-31')
```

- `symbol`: mã chỉ số bạn cần tra cứu. Sử dụng một trong các mã sau:
  - `INX`: S&P 500 Index
  - `DJI`: Dow Jones Industrial Average
  - `COMP`: Nasdaq Composite Index
  - `RUT`: Russell 2000 Index
  - `NYA`: NYSE Composite Index
  - `RUI`: Russell 1000 Index
  - `RUA`: Russell 3000 Index
  - `UKX`: FTSE 100 Index
  - `DAX`: DAX Index
  - `PX1`: CAC 40 Index
  - `N225`: Nikkei 225 Index
  - `000001`: Shanghai SE Composite Index
  - `HSI`: Hang Seng Index
  - `SENSEX`: S&P BSE Sensex Index
  - `ME00000000`: S&P/BMV IPC
- `start`: Ngày kết thúc của truy vấn dữ liệu lịch sử. Định dạng `YYYY-mm-dd`

- `end`: Ngày kết thúc của truy vấn dữ liệu lịch sử. Định dạng `YYYY-mm-dd`

- `interval` (tuỳ chọn): Khung thời gian lấy mẫu dữ liệu. Chỉ hỗ trợ giá trị "1D" để lấy dữ liệu cuối ngày.


**Dữ liệu mẫu:**

Shell

```bash
>>> index.quote.history(start='2023-01-01', end='2024-12-31')

          time      open      high       low     close     volume
0   2023-01-03  33148.90  33387.52  32850.57  33136.37  358608345
1   2023-01-04  33165.14  33409.10  33033.48  33269.77  383346276
2   2023-01-05  33191.72  33191.72  32812.33  32930.08  342665273
3   2023-01-06  33055.30  33710.66  32997.39  33630.61  365497603
4   2023-01-09  33664.39  33935.11  33487.66  33517.65  327846929
..         ...       ...       ...       ...       ...        ...
346 2024-05-20  39989.76  40077.40  39787.09  39806.77  275306588
347 2024-05-21  39804.40  39905.80  39778.73  39872.99  318222838
348 2024-05-22  39863.33  39890.91  39559.09  39671.04  260936322
349 2024-05-23  39694.95  39694.95  39025.51  39065.26  338754861
350 2024-05-24  39089.23  39220.31  39020.29  39069.59  254833323

[351 rows x 6 columns]
```

**Kiểu dữ liệu**

Shell

```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 351 entries, 0 to 350
Data columns (total 6 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   time    351 non-null    datetime64[ns]
 1   open    351 non-null    float64
 2   high    351 non-null    float64
 3   low     351 non-null    float64
 4   close   351 non-null    float64
 5   volume  351 non-null    int64
dtypes: datetime64[ns](1), float64(4), int64(1)
memory usage: 16.6 KB
```

#### Tags

[dữ liệu giá](https://vnstocks.com/blog/tag/du-lieu-gia) [intraday](https://vnstocks.com/blog/tag/intraday) [ohlcv](https://vnstocks.com/blog/tag/ohlcv)

### Thảo luận

Đang tải bình luận...