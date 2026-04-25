---
url: "https://vnstocks.com/docs/vnstock-ta/cac-buoc-su-dung"
title: "Hướng dẫn các bước sử dụng | Vnstock"
---

Toggle Sidebar

### Mục lục

Thành công

Các bước sử dụng Vnstock TA tương đối đơn giản thông qua các đoạn mã mẫu giúp bạn nhanh chóng thiết lập và sử dụng. Bạn có thể sử dụng file Notebook minh hoạ để thực hiện lệnh hoặc copy các đoạn lệnh vào chương trình Python để sử dụng. Để sử dụng thư viện, bạn cần tham gia tối thiểu là [**gói tài trợ Silver**](https://vnstocks.com/insiders-program), và nhận được quyền truy cập repository bí mật qua Github để cài đặt thư viện.

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock_insider_guide/blob/main/demo/2-vnstock_ta-demo.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Cài đặt

Vui lòng tham khảo hướng dẫn cài đặt tại mục tài liệu hướng dẫn Cài đặt phần mềm trong gói thư viện tài trợ Vnstock. Sử dụng Notebook minh hoạ dưới đây để cài đặt nhanh và thử nghiệm ngay với Google Colab.

[Hướng dẫn cài đặt](https://vnstocks.com/vnstock-insider-api/cai-dat-go-loi)

## Nạp dữ liệu

Python

```python
import pandas as pd
from vnstock_ta import DataSource

data = DataSource(symbol='ACB',
                  start='2023-01-02', end='2025-03-22',
                  interval='1D', source='VCI').get_data()
```

Sau thao tác này, dữ liệu cần thiết cho phân tích kỹ thuật với định dạng tiêu chuẩn OHLCV sẽ được nạp vào môi trường làm việc để bạn sử dụng.

## Thiết lập

Python

```python
# Nạp biến data nhận dữ liệu giá đầu vào ở trên
from vnstock_ta import Indicator, Plotter
 # Optional: Import các biến được định nghĩa sẵn mã màu tương phản tốt với chart
from vnstock_ta.utils.const import _CRIMSON_RED, _EMERALD_GREEN, _ORANGE, _LIME_PUNCH, _ISLAND_GREEN, _SLATE_BLUE, _TURKISH_SEA

# Gán Indicator Class với tên viết tắt
ta = Indicator(data)

# Đổi theme='light' để sử dụng giao diện sáng, áp dụng tất cả hàm đi kèm
chart = Plotter(data, theme='dark', watermark=True, display=True)
```

## Tính toán chỉ báo

Việc tính toán chỉ báo kỹ thuật rất đơn giản và sử dụng giá trị mặc định theo thiết lập tiêu chuẩn từ TradingView, bạn có thể thay đổi thông số để phù hợp với chiến lược của mình.

Ví dụ, sau các bước thiết lập, bạn có thể tính dải dữ liệu MACD chỉ với 1 câu lệnh.

Python

```python
ta.macd(fast=12, slow=26, signal=9)
```

Kết quả trả về:

Shell

```bash
time
2023-01-03          NaN
2023-01-04          NaN
2023-01-05          NaN
2023-01-06          NaN
2023-01-09          NaN
                ...
2024-06-04    52.565116
2024-06-05    50.727906
2024-06-06    48.386306
2024-06-07    48.669824
2024-06-10    50.144457
Name: RSI_14, Length: 355, dtype: float64
```

Bạn cũng có thể biểu diễn đồ thị tương tác cho chỉ báo bất kỳ với cú pháp đơn giản:

Python

```python
ta.macd(fast=12, slow=26, signal=9)
```

![Đồ thị kỹ thuật với chỉ báo MACD](https://vnstocks.com/images/macd_vnstock_ta_chart.png)Đồ thị kỹ thuật với chỉ báo MACD

Chi tiết các hàm và bước tính toán, bạn có thể xem trong Notebook minh hoạ và thao tác nhanh để thấy kết quả.

Chúc bạn thành công!

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập