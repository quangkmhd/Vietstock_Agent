---
url: "https://vnstocks.com/docs/vnstock/bang-gia-giao-dich"
title: "Bảng giá giao dịch | Vnstock"
---

Toggle Sidebar

### Mục lục

Gợi ý

Các hàm tra cứu thông tin trong mục này cho phép bạn truy xuất dữ liệu bảng giá chứng khoán theo thời gian thực. Hỗ trợ cả hai nguồn dữ liệu KBS và VCI với cấu trúc và độ chi tiết khác nhau.

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/1_quickstart_stock_vietnam.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

Hướng dẫn sử dụng

**Notebook minh hoạ**: Dành cho người học data, muốn thực hành trực tiếp với các ví dụ mẫu.

**Agent Guide**: Dành cho người theo trường phái Vibe Coding, muốn viết chương trình hiệu quả với AI.

## So sánh nguồn dữ liệu

| Phương thức | KBS | VCI | Ghi chú |
| --- | --- | --- | --- |
| **price\_board()** | ✅ | ✅ | KBS: 29 cột, VCI: 77 cột |

**Khuyến nghị:**

- **KBS**: Dữ liệu gọn gàng, ổn định, 29 cột, phù hợp sử dụng thường xuyên
- **VCI**: Dữ liệu cực kỳ chi tiết, 77 cột với MultiIndex, phù hợp phân tích chuyên sâu

## Khởi tạo Trading

### KBS Trading (Khuyến nghị)

Python

```python
from vnstock import Trading

# Khởi tạo với KBS
trading_kbs = Trading(source="KBS", symbol="VCI")
```

### VCI Trading

Python

```python
# Khởi tạo với VCI
trading_vci = Trading(source="VCI", symbol="VCI")
```

**Các tham số chung:**

- `source` (str): Nguồn dữ liệu - 'KBS' hoặc 'VCI'
- `symbol` (str): Mã chứng khoán mặc định

## Bảng giá thị trường

### KBS Source

**Gọi hàm**

Python

```python
from vnstock import Trading

trading = Trading(source="KBS", symbol="VCI")
board = trading.price_board(symbols_list=['VCI', 'VCB', 'ACB'])
print(f"Shape: {board.shape}")  # (3, 29)
```

**Dữ liệu mẫu KBS:**

Shell

```bash
>>> trading.price_board(symbols_list=['VCI', 'VCB'])

  symbol exchange  reference_price  price_change  percent_change  ...  ask_price_3  ask_vol_3  foreign_buy_volume  foreign_sell_volume
0    VCI     HOSE            36150           500        1.383126  ...        36200       100              12345                 67890
1    VCB     HOSE            69800           700        1.002865  ...        69900       200              23456                 34567

[2 rows x 29 columns]
```

**Các cột chính KBS:**

- `symbol`, `exchange`: Mã CK và sàn
- `reference_price`: Giá tham chiếu
- `price_change`, `percent_change`: Thay đổi giá và %
- `open_price`, `high_price`, `low_price`, `close_price`: OHLC
- `total_trades`, `total_value`: Tổng số giao dịch và giá trị
- `bid_price_1/2/3`, `bid_vol_1/2/3`: 3 mức giá mua
- `ask_price_1/2/3`, `ask_vol_1/2/3`: 3 mức giá bán
- `foreign_buy_volume`, `foreign_sell_volume`: Khối lượng NĐT

### VCI Source

**Gọi hàm**

Python

```python
from vnstock import Trading

trading = Trading(source="VCI", symbol="VCI")
board = trading.price_board(symbols_list=['VCI', 'VCB'])
print(f"Shape: {board.shape}")  # (2, 77)
```

**Dữ liệu mẫu VCI:**

Shell

```bash
>>> trading.price_board(symbols_list=['VCI'])

  listing symbol listing ref_price match match_price match match_vol  ...  bid_ask ask_3_price bid_ask ask_3_volume
0      VCI            36150                      36200        123456  ...              36300               1000
1      VCB            69800                      69900        234567  ...              70000               2000

[2 rows x 77 columns]
```

**Cấu trúc MultiIndex VCI (77 columns):**

**LISTING (24 cột):**

- `symbol`: Mã chứng khoán
- `ceiling`, `floor`: Giá trần, giá sàn
- `ref_price`: Giá tham chiếu
- `stock_type`: Loại cổ phiếu
- `exchange`: Sàn giao dịch
- `trading_status`, `trading_status_code`, `trading_status_group`: Trạng thái giao dịch
- `security_status`: Trạng thái chứng khoán
- `last_trading_date`: Ngày giao dịch cuối
- `issue_date`: Ngày phát hành
- `listed_share`: Số lượng niêm yết
- `coupon_rate`, `yield`: Lãi suất coupon, lợi suất
- `organ_name`: Tên tổ chức phát hành
- `mapping_symbol`: Mã mapping
- `product_grp_id`, `partition`: ID sản phẩm, phân loại
- `index_type`: Loại chỉ số

**MATCH (38 cột):**

- `match_price`, `match_vol`: Giá và khối lượng khớp lệnh
- `accumulated_value`, `accumulated_volume`: Giá trị và khối lượng tích lũy
- `accumulated_value_g1`, `accumulated_volume_g1`: Tích lũy phiên G1
- `open_price`, `highest`, `lowest`: Giá mở cửa, cao nhất, thấp nhất
- `avg_match_price`: Giá khớp lệnh trung bình
- `foreign_buy_volume`, `foreign_sell_volume`: Khối lượng NĐT mua/bán
- `foreign_buy_value`, `foreign_sell_value`: Giá trị NĐT mua/bán
- `total_room`: Dư room
- `current_room`: Room hiện tại
- `total_buy_orders`, `total_sell_orders`: Tổng lệnh mua/bán
- `match_price_ato`, `match_volume_ato`: Giá/khối lượng ATO
- `match_price_atc`, `match_volume_atc`: Giá/khối lượng ATC
- `trading_session_id`: ID phiên giao dịch
- `first_time_match_price`: Giá khớp lần đầu
- `match_type`: Loại khớp lệnh
- `underlying`, `open_interest`: Cơ sở, vị thế mở

**BID\_ASK (15 cột):**

- `transaction_time`: Thời gian giao dịch
- `bid_count`, `ask_count`: Số lệnh mua/bán
- `bid_1_price`, `bid_1_volume`: Mức 1 - Giá/khối lượng mua
- `bid_2_price`, `bid_2_volume`: Mức 2 - Giá/khối lượng mua
- `bid_3_price`, `bid_3_volume`: Mức 3 - Giá/khối lượng mua
- `ask_1_price`, `ask_1_volume`: Mức 1 - Giá/khối lượng bán
- `ask_2_price`, `ask_2_volume`: Mức 2 - Giá/khối lượng bán
- `ask_3_price`, `ask_3_volume`: Mức 3 - Giá/khối lượng bán

**Truy cập MultiIndex VCI:**

Python

```python
import pandas as pd
from vnstock import Trading

# Lấy dữ liệu VCI (vẫn có MultiIndex)
trading = Trading(source="VCI", symbol="VCI")
board = trading.price_board(symbols_list=['VCI', 'VCB'])

# Option 1: Truy cập trực tiếp MultiIndex
listing_info = board[[('listing', 'symbol'), ('listing', 'ref_price'), ('listing', 'exchange')]]
trading_info = board[[('match', 'match_price'), ('match', 'match_vol'), ('match', 'accumulated_value')]]

# Option 2: Flatten columns để dễ sử dụng hơn
board_flat = board.copy()
board_flat.columns = ['_'.join(col).strip() for col in board.columns.values]

# Bây giờ có thể truy cập như bình thường
print(board_flat[['listing_symbol', 'listing_ref_price', 'match_match_price']].head())
```

## Khi nào dùng nguồn nào?

**Dùng KBS khi:**

- Cần dữ liệu nhanh và ổn định
- Chỉ cần thông tin cơ bản (giá, KL, thay đổi)
- Xử lý data đơn giản với flat columns
- Muốn data gọn gàng, dễ sử dụng

**Dùng VCI khi:**

- Cần phân tích sâu thị trường
- Cần market detail đầy đủ (77 columns)
- Cần thông tin chi tiết về niêm yết và giao dịch
- Muốn data chi tiết với MultiIndex structure

#### Tags

[bảng giá chứng khoán](https://vnstocks.com/blog/tag/bang-gia-chung-khoan) [dữ liệu bảng giá](https://vnstocks.com/blog/tag/du-lieu-bang-gia) [giá cổ phiếu thời gian thực](https://vnstocks.com/blog/tag/gia-co-phieu-thoi-gian-thuc)

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập