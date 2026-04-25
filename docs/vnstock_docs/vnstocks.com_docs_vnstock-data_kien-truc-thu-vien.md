---
url: "https://vnstocks.com/docs/vnstock-data/kien-truc-thu-vien"
title: "Kiến trúc thư viện | Vnstock"
---

## Mục lục

Gợi ý

Thư viện `vnstock_data` được thiết kế với cấu trúc hướng mô-đun, dễ mở rộng, dễ tích hợp, và dễ chuyển đổi nguồn dữ liệu chỉ qua một tham số cấu hình.

Đây là bộ công cụ dữ liệu chứng khoán - kinh tế - tài sản toàn diện, sẵn sàng hỗ trợ bạn xây dựng mọi sản phẩm từ phân tích, hỗ trợ giao dịch, đến dự báo thị trường.

## Triết Lý Thiết Kế 3 Lớp

Mọi dòng code trong `vnstock_data` đều hướng tới một mục tiêu duy nhất: **Giúp bạn tập trung vào phân tích tài chính thay vì xử lý mã nguồn.**

| Lớp Kiến Trúc | Bản Chất Kỹ Thuật | Ý nghĩa |
| --- | --- | --- |
| **Giao diện hợp nhất (Unified UI)** | Lớp trên cùng, tổ chức lại toàn bộ dữ liệu thành cấu trúc nghiệp vụ (Market, Reference, Fundamental...). | **Lập trình như một chuyên gia tài chính.** Trải nghiệm xuyên suốt, dễ tìm kiếm chức năng qua `show_api()`, gọi hàm liền mạch qua dấu chấm `.` để phân nhánh hàm mà không cần quan tâm tới cài đặt nguồn dữ liệu. |
| **Giao tiếp chung (Core Adapter)** | Lớp trung gian tạo ra một chuẩn giao tiếp duy nhất giữa code của bạn và mọi nguồn cấp dữ liệu. | **Sự tự do vô hạn (Vendor-Lock Free).** Thay đổi nhà cung cấp (từ VCI sang VND, MAS) chỉ đơn giản là thay đổi giá trị `source=` khi khởi tạo class. Code hiện tại không bao giờ bị gãy, tối đa hóa tính linh hoạt cho mọi dự án. |
| **Module Nguồn cấp (Implementation)** | Lớp dưới cùng giao tiếp trực tiếp với hệ thống API gốc đặc thù của từng nguồn cấp. | **Quyền kiểm soát tuyệt đối trên Production.** Đóng gói chặt chẽ, đảm bảo tính ổn định cao nhất 24/7. Cho phép bạn khai thác tận cùng những trường dữ liệu "hiếm" chỉ riêng của một hệ thống có được. |

## Hướng Dẫn Sử Dụng

Thông báo tương thích

`vnstock_data` hỗ trợ **3 cách tiếp cận** khi gọi dữ liệu, được tổ chức theo cấu trúc 3 lớp. Người dùng cũ từ gói Free của Vnstock có thể nâng cấp mượt mà chỉ bằng cách thay đổi câu lệnh import. Để tận dụng toàn bộ sức mạnh và tiện ích mới nhất, chúng tôi đặc biệt khuyến nghị nền tảng **Unified UI**.

Python

```python
# Câu lệnh cũ
from vnstock import Quote, Trading, Finance, Listing, Company, Macro

# Câu lệnh dùng cho bản sponsor (Đổi tên thư viện là được)
from vnstock_data import Market, Reference, Fundamental
```

### 1\. Giao diện hợp nhất (Unified UI - Khuyên dùng)

> Kiến trúc tiêu chuẩn mới nhất, vận hành mượt mà, cảm hứng thiết kế từ Bloomberg Terminal, FIX.

Đây là cách tương tác với dữ liệu theo các miền nghiệp vụ rõ ràng, giúp lập trình viên thao tác một cách tự nhiên mà không cần bận tâm về cấu trúc kỹ thuật bên dưới.

Python

```python
from vnstock_data import Market, Reference, Fundamental

# Ví dụ tra cứu giá lịch sử thông qua Market Layer
df = Market.quote(symbol="VCI") \
           .history(start="2024-02-01", end="2025-04-18", interval="1D")
```

✅ **Ưu điểm**:

- Trải nghiệm lập trình trơn tru, liền mạch với khả năng gọi chuỗi (method chaining).
- Các nhóm dữ liệu được tổ chức logic theo sát kiến thức tài chính thực tiễn.
- Hỗ trợ hàm `show_api()` để dễ dàng tự khám phá chức năng như có một bản đồ hướng dẫn bên cạnh.

### 2\. Sử dụng Giao tiếp chung (Core Adapter)

> **Tối ưu cho sự linh hoạt, hoán đổi nguồn nhà cung cấp, phù hợp người dùng nâng cấp từ bản cũ.**

Phương thức này dành riêng cho người dùng quen thuộc với phong cách của phiên bản Vnstock trước đây. Chỉ cần điều chỉnh phần import thư viện, gần như toàn bộ tính năng và code hiện tại của bạn sẽ tiếp tục hoạt động nguyên vẹn.

Python

```python
from vnstock_data import Quote, Trading, Finance, Listing, Company, Macro

quote = Quote(source="vci", symbol="VCI")
df = quote.history(start="2024-02-01", end="2025-04-18", interval="1D")
```

✅ **Ưu điểm**:

- Chuyển đổi siêu tốc từ phiên bản open-source.
- Linh hoạt đối chiếu và thay đổi nhà cung cấp (từ VCI sang VND, MAS...).

### 3\. Tương tác trực tiếp Module Nguồn cấp

> **Kiểm soát chặt chẽ nhất, tối ưu cho sự ổn định ở môi trường Production.**

Thay vì dùng giao tiếp chung, bạn gọi thẳng dữ liệu từ module bên trong của từng nhà cung cấp.

Python

```python
from vnstock_data.explorer.vci import Quote

quote = Quote(symbol="VCI")
df = quote.history(start="2024-02-01", end="2025-04-18", interval="1D")
```

✅ **Ưu điểm**:

- Giảm thiểu hoàn toàn rủi ro chức năng không hỗ trợ chéo.
- Truy cập vào những trường dữ liệu đặc thù hay tính năng ẩn chỉ có riêng ở một nhà cung cấp cụ thể.

## Tra cứu API

Thay vì phải tra cứu tài liệu rời rạc, **Unified UI** gom toàn bộ thư viện lại thành một cây tính năng. Gõ `show_api()` và bạn sẽ có toàn cảnh bức tranh dữ liệu.

Python

```python
from vnstock_data import show_api, show_doc
>>> show_api()
```

**Hiển thị kết quả API Tree**

Text

```plaintext
API STRUCTURE TREE - VNSTOCK_DATA (Unified UI Endpoints)
vnstock_data
├── Reference
│   ├── bond # Access bond reference data.
│   │   ├── list() # List bonds available in the market.
│   ├── company() # Access company-specific reference data.
│   │   ├── events() [VCI] -> DataFrame # Get company events.
│   │   ├── info() [VCI] -> DataFrame # Get company info/overview.
│   │   ├── margin_ratio() [KBS] -> DataFrame # Get margin lending ratio for the company across brokers.
│   │   ├── news() [VCI] -> DataFrame # Get company news.
│   │   ├── officers() [VCI] -> DataFrame # Get company officers.
│   │   ├── shareholders() [VCI] -> DataFrame # Get company shareholders.
│   │   ├── subsidiaries() [VCI] -> DataFrame # Get company subsidiaries.
│   ├── equity # Access equity reference data.
│   │   ├── list() [VCI] -> DataFrame # List all equity symbols.
│   │   ├── list_by_exchange() -> DataFrame # List all equities organized by exchange.
│   │   ├── list_by_group() -> DataFrame # List equities by group (e.g., VN30, HOSE).
│   │   ├── list_by_industry() -> DataFrame # List equities by industry (ICB classification).
│   ├── etf # Access ETF reference data.
│   │   ├── list() [KBS] -> DataFrame # List all Exchange-Traded Funds (ETFs) available in the market.
│   ├── events # Access events reference data (calendar, etc.).
│   │   ├── calendar() [VCI] -> DataFrame # Retrieve events calendar (dividends, AGM, new listings, ...) from the default data source.
│   │   ├── market() -> DataFrame # Retrieve special stock market events (holidays, system incidents, ...)
│   ├── fund # Master data for Mutual Funds (Chứng Chỉ Quỹ).
│   │   ├── list() [FMARKET] -> DataFrame # Extracts the list of all available mutual funds.
│   ├── futures() # Access index futures reference data (listing or symbol-specific info).
│   │   ├── info() [KBS] -> DataFrame # Get info and realtime information for the specific index future.
│   │   ├── list() [VCI] -> DataFrame # List all available futures indices with metadata.
│   ├── index # Access index reference data.
│   │   ├── groups() [KBS] -> DataFrame # List all supported index groups and categories.
│   │   ├── list() [KBS] -> DataFrame # List all standardized market indices with metadata.
│   │   ├── list_by_group() -> DataFrame # List market indices by group/category.
│   │   ├── members() [KBS] -> Series # List constituents/members of the specified index.
│   ├── industry # Access industry reference data.
│   │   ├── list() [VCI] -> DataFrame # List ICB industry classifications for all symbols in the market.
│   │   ├── sectors() [VCI] -> DataFrame # List all symbols by their industry sectors.
│   ├── market # Access live market status.
│   │   ├── status() [MAS] -> DataFrame # Retrieve live stock market status (OPEN, CLOSED, ATO, ATC, etc.)
│   ├── search # Access global symbol search.
│   │   ├── symbol() [MSN] -> DataFrame # Retrieves a list of symbols from the market matching the query.
│   └── warrant() # Access covered warrant reference data (info, specifications, pricing).
│       ├── info() [KBS] -> DataFrame # Get info and realtime information for the specific covered warrant.
│       ├── list() [VCI] -> DataFrame # List all available covered warrants.
├── Market
│   ├── commodity() # Access commodity market data (e.g., 'GC=F').
│   │   ├── ohlcv() [MSN] -> DataFrame # Historical OHLCV bars.
│   │   ├── quote() -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── summary() -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   ├── crypto() # Access crypto market data (e.g., 'BTC').
│   │   ├── ohlcv() [MSN] -> DataFrame # Historical OHLCV bars.
│   │   ├── quote() -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── summary() -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   ├── equity() # Access equity market data.
│   │   ├── block_trades() [KBS] -> DataFrame # Real-time or historical data for negotiated/block trades (giao dịch thoả thuận).
│   │   ├── foreign_flow() [VCI] -> DataFrame # Historical or daily foreign buy/sell volume and value.
│   │   ├── odd_lot() [KBS] -> DataFrame # Real-time pricing or trades for odd-lot execution (Lô lẻ).
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars.
│   │   ├── order_book() [KBS] -> DataFrame # Order book levels (Best Bid/Ask L2/L3).
│   │   ├── proprietary_flow() [VCI] -> DataFrame # Trade data for proprietary desks (Tự doanh).
│   │   ├── quote() [KBS] -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── session_stats() [VCI] -> DataFrame # End-of-session aggregate statistics.
│   │   ├── summary() [KBS] -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   │   ├── trade_history() [KBS] -> DataFrame # Historical trading statistics (price, volume, value) for Equities.
│   │   ├── trades() [KBS] -> DataFrame # Real-time or intraday tick-by-tick trading tape (Time & Sales).
│   │   ├── volume_profile() [KBS] -> DataFrame # Aggregated volume distributed across executed price levels (Volume Profile).
│   ├── etf() # Access ETF market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars.
│   │   ├── order_book() [KBS] -> DataFrame # Order book levels (Best Bid/Ask L2/L3).
│   │   ├── quote() [KBS] -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── session_stats() [VCI] -> DataFrame # End-of-session aggregate statistics.
│   │   ├── summary() [KBS] -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   │   ├── trades() [KBS] -> DataFrame # Real-time or intraday tick-by-tick trading tape (Time & Sales).
│   ├── forex() # Access forex market data (e.g., 'USDVND').
│   │   ├── ohlcv() [MSN] -> DataFrame # Historical OHLCV bars.
│   │   ├── quote() -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── summary() -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   ├── fund() # Access historical NAVs and portfolio compositions for a specific Mutual Fund.
│   │   ├── asset_holding() [FMARKET] -> DataFrame # Extracts the asset allocation (Equities vs Cash/Bonds) of the fund.
│   │   ├── industry_holding() [FMARKET] -> DataFrame # Extracts the industry weighting inside the fund's portfolio.
│   │   ├── top_holding() [FMARKET] -> DataFrame # Extracts the top equity/bond holdings of the fund.
│   ├── futures() # Access futures market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars.
│   │   ├── order_book() [KBS] -> DataFrame # Order book levels (Best Bid/Ask L2/L3).
│   │   ├── quote() [KBS] -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── summary() [KBS] -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   │   ├── trades() [KBS] -> DataFrame # Real-time or intraday tick-by-tick trading tape (Time & Sales).
│   ├── index() # Access index market data.
│   │   ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars.
│   │   ├── quote() [KBS] -> DataFrame # Real-time single-symbol pricing snapshot.
│   │   ├── summary() [KBS] -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│   └── warrant() # Access warrant market data.
│       ├── ohlcv() [KBS] -> DataFrame # Historical OHLCV bars.
│       ├── order_book() [KBS] -> DataFrame # Order book levels (Best Bid/Ask L2/L3).
│       ├── quote() [KBS] -> DataFrame # Real-time single-symbol pricing snapshot.
│       ├── summary() [KBS] -> DataFrame # Stock Info / Snapshot summary metrics including pricing,
│       ├── trades() [KBS] -> DataFrame # Real-time or intraday tick-by-tick trading tape (Time & Sales).
├── Fundamental
│   └── equity() # Access financial data for a specific corporate equity (Fundamental Layer).
│       ├── balance_sheet() [KBS] -> DataFrame # Extracts Balance Sheet.
│       ├── cash_flow() [KBS] -> DataFrame # Extracts Cash Flow statement.
│       ├── income_statement() [KBS] -> DataFrame # Extracts Income Statement.
│       ├── note() [VCI] -> DataFrame # Extracts Footnotes (Thuyết minh Báo cáo tài chính).
│       ├── ratio() [KBS] -> DataFrame # Extracts key financial ratios (P/E, ROE, Debt/Equity, etc.).
├── Analytics
│   └── valuation() # Access historical valuation multiples for market indices (Analytics Layer).
│       ├── evaluation() [VND] -> DataFrame # Retrieves an overview of the market with both P/E and P/B ratios.
│       ├── pb() [VND] -> DataFrame # Retrieves P/B (Price-to-Book) ratio data.
│       ├── pe() [VND] -> DataFrame # Retrieves P/E (Price-to-Earnings) ratio data.
├── Macro
│   ├── commodity() # Access global and local commodity prices (Macro Layer - Commodity Domain).
│   │   ├── coke() [SPL] -> DataFrame # Coke (Coal) prices.
│   │   ├── corn() [SPL] -> DataFrame # Corn prices.
│   │   ├── fertilizer_ure() [SPL] -> DataFrame # Fertilizer URE prices.
│   │   ├── gas() -> DataFrame # Gas prices. Note: 'GLOBAL' returns natural gas futures. 'VN' returns aggregated RON/DO prices.
│   │   ├── gold() -> DataFrame # Gold prices.
│   │   ├── iron_ore() [SPL] -> DataFrame # Iron ore prices.
│   │   ├── oil_crude() [SPL] -> DataFrame # Crude Oil prices.
│   │   ├── pork() -> DataFrame # Pork prices. 'VN' for local North Pig, 'CHINA' for China market.
│   │   ├── soybean() [SPL] -> DataFrame # Soybean prices.
│   │   ├── steel() -> DataFrame # Steel prices. 'GLOBAL' for HRC1!, 'VN' for D10.
│   │   ├── sugar() [SPL] -> DataFrame # Sugar prices.
│   ├── currency() # Access foreign exchange rates and interest rate data (Macro Layer - Currency Domain).
│   │   ├── exchange_rate() [MBK] -> DataFrame # Foreign exchange rates.
│   │   ├── interest_rate() [MBK] -> DataFrame # Interest rates data.
│   └── economy() # Access standard macroeconomic indicators (Macro Layer - Economy Domain).
│       ├── cpi() [MBK] -> DataFrame # Consumer Price Index data.
│       ├── fdi() [MBK] -> DataFrame # Foreign Direct Investment data.
│       ├── gdp() [MBK] -> DataFrame # GDP data.
│       ├── import_export() [MBK] -> DataFrame # Import/Export macro data.
│       ├── industry_prod() [MBK] -> DataFrame # Industrial Production data.
│       ├── money_supply() [MBK] -> DataFrame # Money supply data.
│       ├── population_labor() [MBK] -> DataFrame # Population and Labor data.
│       ├── retail() [MBK] -> DataFrame # Retail macro data.
└── Insights
    ├── ranking() # Access market ranking metrics - Top movers by various criteria (Insights Layer).
    │   ├── deal() [VND] -> DataFrame # Top 10 stocks with highest put-through/deal volume spikes.
    │   ├── foreign_buy() [VND] -> DataFrame # Top 10 stocks with highest foreign net buy value.
    │   ├── foreign_sell() [VND] -> DataFrame # Top 10 stocks with highest foreign net sell value.
    │   ├── gainer() [VND] -> DataFrame # Top 10 stocks with highest price increase.
    │   ├── loser() [VND] -> DataFrame # Top 10 stocks with highest price decrease.
    │   ├── value() [VND] -> DataFrame # Top 10 stocks with highest trading value.
    │   ├── volume() [VND] -> DataFrame # Top 10 stocks with highest volume spikes.
    └── screener() # Access stock screener functionality (Insights Layer).
        ├── criteria() [VCI] -> DataFrame # Retrieves the mapping list of criteria to explain field names (data columns).
        ├── filter() [VCI] -> DataFrame # Retrieves full market data (all stocks) with all available criteria (ratios, metrics)

Tip: Sử dụng show_doc(node) để đọc docstring.
[Navigation] = Intermediate methods returning domain objects
```

### Thảo luận

Đang tải bình luận...