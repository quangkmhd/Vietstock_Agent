---
url: "https://vnstocks.com/docs/vnstock-data/reference-layer-v3"
title: "Dữ Liệu Tham Chiếu | Vnstock"
---

Toggle Sidebar

### Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock-agent-guide/blob/main/notebooks/01_unified_ui/01_Reference.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Tổng quan

**Reference Layer** cung cấp thông tin nền tảng, tĩnh về các sản phẩm tài chính — công ty, chỉ số, ngành, danh sách symbol, ETF, trái phiếu, sự kiện, v.v. Đây là dữ liệu **không thay đổi thường xuyên** và được sử dụng để **tra cứu (lookup)** hay làm **dữ liệu gốc (master data)**.

## Khởi tạo

Python

```python
from vnstock_data import Reference
ref = Reference()
```

## Cấu trúc Domain

```
Reference()
├── .company(symbol)       # Thông tin công ty
├── .equity                # Danh sách cổ phiếu
├── .index                 # Danh sách chỉ số
├── .industry              # Ngành kinh tế
├── .fund                  # Quỹ đầu tư mở
├── .etf                   # Quỹ ETF
├── .bond                  # Trái phiếu
├── .events                # Sự kiện thị trường
├── .search                # Tìm kiếm toàn cục
├── .futures(symbol)       # Hợp đồng tương lai
└── .warrant(symbol)       # Chứng quyền
```

### Tra cứu nhanh

Python

```python
from vnstock_data import show_api, Reference
show_api(Reference())
```

**Hiển thị kết quả API Tree**

Text

```plaintext
API STRUCTURE TREE - VNSTOCK_DATA (Unified UI Endpoints)
vnstock_data
├── Reference
│   ├── bond # Access bond reference data.
│   │   ├── list() # List bonds available in the market.
│   ├── equity # Access equity reference data.
│   │   ├── list() [VCI] # List all equity symbols.
│   │   ├── list_by_exchange() # List all equities organized by exchange.
│   │   ├── list_by_industry() # List equities by industry (ICB classification).
│   ├── etf # Access ETF reference data.
│   │   ├── list() [KBS] # List all Exchange-Traded Funds (ETFs) available in the market.
│   ├── events # Access events reference data (calendar, etc.).
│   │   ├── calendar() [VCI] # Retrieve events calendar (dividends, AGM, new listings, ...) from the default data source.
│   ├── fund # Master data for Mutual Funds (Chứng Chỉ Quỹ).
│   │   ├── list() [FMARKET] # Extracts the list of all available mutual funds.
│   ├── index # Access index reference data.
│   │   ├── groups() [KBS] # List all supported index groups and categories.
│   ├── industry # Access industry reference data.
│   │   ├── list() [VCI] # List ICB industry classifications for all symbols in the market.
│   │   ├── sectors() [VCI] # List all symbols by their industry sectors.
│   └── search # Access global symbol search.
│       ├── symbol() [MSN] # Retrieves a list of symbols from the market matching the query.
├── Market
├── Fundamental
├── Analytics
├── Macro
└── Insights

Tip: Sử dụng show_doc(node) để đọc docstring.
[Navigation] = Intermediate methods returning domain objects
```

## Hướng dẫn chi tiết

### 1\. Thông tin công ty

Truy xuất thông tin tổng quan, cổ đông, ban lãnh đạo, công ty con, tin tức, sự kiện và tỷ lệ ký quỹ của một mã cổ phiếu cụ thể.

| Phương thức | Mô tả |
| --- | --- |
| `info()` | Thông tin tổng quan công ty |
| `shareholders()` | Danh sách cổ đông chính |
| `officers()` | Danh sách ban lãnh đạo |
| `subsidiaries()` | Danh sách công ty con |
| `news()` | Tin tức công ty |
| `events()` | Sự kiện công ty |
| `margin_ratio()` | Tỷ lệ ký quỹ qua các công ty chứng khoán |

Python

```python
from vnstock_data import Reference

ref = Reference()

# Thông tin tổng quan công ty
df_profile = ref.company("TCB").info()

# Danh sách cổ đông lớn
df_shareholders = ref.company("VIC").shareholders()

# Quản lý cấp cao
df_officers = ref.company("HPG").officers()

# Công ty con
df_subs = ref.company("VIC").subsidiaries()

# Tin tức & sự kiện
df_news = ref.company("TCB").news()
df_events = ref.company("TCB").events()

# Tỷ lệ ký quỹ
df_margin = ref.company("TCB").margin_ratio()
```

* * *

### 2\. Danh sách cổ phiếu

Tra cứu toàn bộ danh sách cổ phiếu niêm yết, lọc theo nhóm chỉ số, theo sàn giao dịch hoặc theo ngành ICB.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `list()` | — | Toàn bộ danh sách cổ phiếu (1700+ mã) |
| `list_by_group()` | `group` | Cổ phiếu theo nhóm (VN30, HOSE...) |
| `list_by_exchange()` | `exchange` | Cổ phiếu theo sàn (HSX, HNX...) |
| `list_by_industry()` | — | Cổ phiếu theo ngành ICB |

Python

```python
from vnstock_data import Reference

ref = Reference()

# Tất cả symbol
all_symbols = ref.equity.list()

# Cổ phiếu nhóm VN30
vn30 = ref.equity.list_by_group("VN30")

# Cổ phiếu sàn HSX
hsx_stocks = ref.equity.list_by_exchange("HSX")

# Cổ phiếu theo ngành ICB
industry_stocks = ref.equity.list_by_industry()
```

* * *

### 3\. Danh sách chỉ số

Liệt kê toàn bộ chỉ số thị trường, các nhóm chỉ số, và thành phần cổ phiếu trong từng chỉ số.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `list()` | — | Toàn bộ chỉ số kèm metadata |
| `groups()` | — | Liệt kê các nhóm chỉ số |
| `members()` | `group` | Thành phần cổ phiếu của chỉ số |
| `list_by_group()` | `group` | Chỉ số theo nhóm |

Python

```python
from vnstock_data import Reference

ref = Reference()

# Tất cả chỉ số
all_indices = ref.index.list()

# Nhóm chỉ số
groups = ref.index.groups()

# Thành phần VN30
vn30_members = ref.index.members("VN30")

# Thông tin chi tiết 1 chỉ số
vn30_info = ref.index("VN30").info()
vn30_desc = ref.index("VN30").description()
```

* * *

### 4\. Ngành kinh tế

Tra cứu hệ thống phân ngành ICB và danh sách cổ phiếu thuộc từng ngành.

| Phương thức | Mô tả |
| --- | --- |
| `list()` | Toàn bộ danh sách ngành ICB |
| `sectors()` | Phân loại cổ phiếu theo ngành |

Python

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách ngành ICB
industries = ref.industry.list()

# Cổ phiếu theo ngành
sectors = ref.industry.sectors()
```

* * *

### 5\. Quỹ đầu tư mở

Tra cứu danh sách tất cả quỹ đầu tư mở (chứng chỉ quỹ) trên thị trường.

Python

```python
from vnstock_data import Reference

ref = Reference()
funds = ref.fund.list()
```

* * *

### 6\. Quỹ ETF

Tra cứu danh sách tất cả quỹ ETF đang niêm yết.

Python

```python
from vnstock_data import Reference

ref = Reference()
etf_list = ref.etf.list()
```

* * *

### 7\. Trái phiếu

Tra cứu danh sách trái phiếu theo loại: tất cả, doanh nghiệp, hoặc chính phủ.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `list()` | `bond_type` | `'all'`, `'corporate'`, `'government'` |

Python

```python
from vnstock_data import Reference

ref = Reference()

# Tất cả trái phiếu
all_bonds = ref.bond.list(bond_type="all")

# Chỉ trái phiếu doanh nghiệp
corp_bonds = ref.bond.list(bond_type="corporate")
```

* * *

### 8\. Sự kiện thị trường

Tra cứu lịch sự kiện thị trường: cổ tức, ĐHCĐ, IPO, giao dịch nội bộ và các sự kiện đặc biệt.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `calendar()` | `start`, `end`, `event_type` | Lịch sự kiện (cổ tức, ĐHCĐ, IPO...) |
| `market()` | `start`, `end`, `event_type` | Sự kiện thị trường (nghỉ lễ, sự cố...) |

**Giá trị `event_type` hỗ trợ cho `calendar()`:**

- `'dividend'` — Cổ tức, phát hành cổ phiếu
- `'insider'` — Giao dịch nội bộ
- `'agm'` — Đại hội cổ đông
- `'others'` — Biến động khác

Python

```python
from vnstock_data import Reference

ref = Reference()

# Lịch sự kiện tháng 3/2026
events = ref.events.calendar(
    start="2026-03-01",
    end="2026-03-31"
)

# Chỉ sự kiện cổ tức
dividends = ref.events.calendar(
    start="2026-03-01",
    end="2026-03-31",
    event_type="dividend"
)

# Sự kiện thị trường (nghỉ lễ, sự cố)
market_events = ref.events.market()
```

* * *

### 9\. Tìm kiếm chứng khoán quốc tế

Tìm kiếm symbol để tra cứu dữ liệu chứng khoán quốc tế từ MSN — cổ phiếu, crypto, forex, chỉ số.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `symbol()` | `query`, `locale`, `limit` | Tìm kiếm symbol toàn cục |

Python

```python
from vnstock_data import Reference

ref = Reference()

# Tìm kiếm "VNM"
results = ref.search.symbol("VNM")

# Tìm Bitcoin
btc = ref.search.symbol("Bitcoin", limit=5)

# Tìm vàng (khu vực tiếng Anh)
gold = ref.search.symbol("Gold", locale="en-us")
```

Mẹo hay

`symbol_id` từ kết quả tìm kiếm có thể dùng cho các domain Market thử nghiệm (crypto, forex, commodity).

* * *

### 10\. Hợp đồng tương lai

Tra cứu danh sách và thông tin chi tiết hợp đồng tương lai.

Python

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách hợp đồng tương lai
futures_list = ref.futures().list()

# Thông tin chi tiết hợp đồng
futures_info = ref.futures("VN30F2503").info()
```

* * *

### 11\. Chứng quyền

Tra cứu danh sách và thông tin chi tiết chứng quyền có bảo đảm.

Python

```python
from vnstock_data import Reference

ref = Reference()

# Danh sách chứng quyền
warrant_list = ref.warrant().list()

# Thông tin chi tiết
warrant_info = ref.warrant("CACB2511").info()
```

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập