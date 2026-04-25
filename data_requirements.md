# Data Requirements: Production-Grade VN Market Data Pipeline

## 1. Dữ liệu cần thu thập
Để phục vụ hệ thống Multi-Agent Financial Advisor, cần thu thập 3 nhóm dữ liệu lõi cho mỗi doanh nghiệp:
1. **Historical Price (OHLCV)**: Giá open, high, low, close, volume hàng ngày.
2. **Fundamental Data (Thông tin doanh nghiệp)**: 
   - Thông tin tổng quan (Overview): Số cổ phiếu phát hành, vốn điều lệ, mô hình kinh doanh.
   - Cấu trúc cổ đông (Shareholders) và Cấu trúc sở hữu (Ownership).
   - Ban lãnh đạo (Officers).
   - Công ty con (Subsidiaries).
   - Lịch sử thay đổi vốn (Capital History).
   - Giao dịch nội bộ (Insider Trading).
3. **Financial Data (Dữ liệu tài chính)**: 
   - Báo cáo kết quả kinh doanh (Income Statement).
   - Bảng cân đối kế toán (Balance Sheet).
   - Báo cáo lưu chuyển tiền tệ (Cash Flow).
   - Chỉ số tài chính (Ratio).
   - *Chu kỳ*: Lấy theo cả Quý (Quarter) và Năm (Year).
4. **Events & News**: 
   - Tin tức doanh nghiệp.
   - Sự kiện doanh nghiệp (Trả cổ tức, phát hành thêm...).

## 2. Nguồn dữ liệu (Source)
Sử dụng thư viện `vnstock` v3.4.0+.
- Nguồn mặc định ưu tiên: **KBS** (Khuyến nghị, ổn định hơn cho batch processing, có dữ liệu chi tiết).
- Nguồn dự phòng (Fallback): **VCI** (Sẽ được gọi khi KBS trả về rỗng, lỗi, hoặc không hỗ trợ, vd: `events`, `subsidiaries`).
- Các hàm tương ứng:
  - Giá: `Quote(source="KBS").history()`
  - Thông tin: `Company(source="KBS").overview()`, `shareholders()`, `ownership()`, vv.
  - Tài chính: `Finance(source="KBS").income_statement(display_mode="all")`, vv.

## 3. Coverage (Phạm vi dữ liệu)
- **Timeframe**: Từ năm 2000 (tương đương `length="25Y"`) đến thời điểm hiện tại.
- **Tickers (10 mã đại diện)**: `FPT`, `HPG`, `VCB`, `MBB`, `TCB`, `VNM`, `VIC`, `SSI`, `VND`, `MWG`. (Đây là các mã Bluechip có dữ liệu lịch sử đầy đủ và ổn định).

## 4. Schema Definition

Do lưu trữ raw data từ `vnstock`, schema sẽ tương ứng với dataframe trả về. Một số field quan trọng:

### 4.1. Historical Price (OHLCV)
- `time` (string/date): Thời gian giao dịch (VD: `2024-12-17`) - Not null
- `open` (float): Giá mở cửa - Not null
- `high` (float): Giá cao - Not null
- `low` (float): Giá thấp - Not null
- `close` (float): Giá đóng cửa - Not null
- `volume` (int): Khối lượng khớp - Not null

### 4.2. Company Overview
- `symbol` (string): Mã CK - Not null
- `founded_date` (string): Ngày thành lập - Nullable
- `charter_capital` (int): Vốn điều lệ - Nullable
- `exchange` (string): Sàn (HOSE/HNX/UPCOM) - Nullable
- `business_model` (string): Mô tả - Nullable

### 4.3. Financial Statements (All mode)
- `item` (string): Tên chỉ tiêu (VN) - Not null
- `item_en` (string): Tên chỉ tiêu (EN) - Nullable
- `item_id` (string): ID chuẩn hóa - Not null
- `periods` (float): Các cột năm/quý tương ứng (vd `2024`, `2024-Q1`) - Nullable

### 4.4. Events
- `id` (int/string): Event ID
- `event_title` (string): Tiêu đề
- `public_date` (string): Ngày công bố
- `event_list_code` (string): Loại sự kiện (DIV, ISS...)

## 5. Data Format
- **Raw format khi crawl**: Pandas DataFrame.
- **Format lưu trữ**: `Parquet` (Giữ nguyên schema, dung lượng tối ưu, tốc độ đọc/ghi nhanh cho pipeline). File metadata/log sẽ lưu dưới dạng `JSON`.

## 6. Storage Design
Dữ liệu được tổ chức trên disk (Local Data Lake) theo partition ticker và loại dữ liệu:
```text
data_lake/
└── raw/
    ├── price/
    │   └── history/
    │       └── {ticker}.parquet
    ├── company/
    │   ├── overview/
    │   │   └── {ticker}.parquet
    │   ├── officers/
    │   │   └── {ticker}.parquet
    │   ├── shareholders/
    │   │   └── {ticker}.parquet
    │   ├── ownership/
    │   │   └── {ticker}.parquet
    │   ├── subsidiaries/
    │   │   └── {ticker}.parquet
    │   ├── affiliate/
    │   │   └── {ticker}.parquet
    │   ├── news/
    │   │   └── {ticker}.parquet
    │   ├── events/
    │   │   └── {ticker}.parquet
    │   ├── capital_history/
    │   │   └── {ticker}.parquet
    │   └── insider_trading/
    │       └── {ticker}.parquet
    └── finance/
        ├── income_statement_year/
        │   └── {ticker}.parquet
        ├── income_statement_quarter/
        │   └── {ticker}.parquet
        ├── balance_sheet_year/
        │   └── {ticker}.parquet
        ├── balance_sheet_quarter/
        │   └── {ticker}.parquet
        ├── cash_flow_year/
        │   └── {ticker}.parquet
        ├── cash_flow_quarter/
        │   └── {ticker}.parquet
        ├── ratio_year/
        │   └── {ticker}.parquet
        └── ratio_quarter/
            └── {ticker}.parquet
```

## 7. Data Volume Estimation
- **10 tickers, 25 năm**:
  - `price`: ~6,250 records/ticker → 62,500 records tổng cộng (~2MB).
  - `finance`: ~150 rows * 4 báo cáo * 2 chu kỳ (năm/quý) = ~1,200 rows/ticker → 12,000 records tổng cộng (<1MB).
  - `company`: Tổng các file metadata dưới 100 rows/ticker → <1,000 records tổng cộng.
- **Tổng dung lượng**: Dự kiến dưới `10 MB` cho raw data của 10 mã (rất nhỏ và dễ dàng xử lý).

## 8. Crawling Strategy
- **Chiến lược**: Batch crawl toàn bộ lịch sử từ đầu đến hiện tại.
- **Retry Logic**: Bọc mọi hàm fetch API bằng thư viện `tenacity`.
  - Cơ chế: `wait_exponential(multiplier=1, min=2, max=10)`, retry tối đa 3 lần.
- **Rate Limit Handling**: Bổ sung `time.sleep(1)` giữa mỗi nhóm API call của một ticker để tránh bị block.
- **Fallback Logic**: Nếu `Company.events()` bằng KBS trả về rỗng, tự động gọi `Company.events()` bằng VCI.
- **Checkpointing**: Trước khi fetch một file (VD: `events/FPT.parquet`), kiểm tra nếu file đã tồn tại trên disk thì bỏ qua (skip), giúp resume dễ dàng nếu quá trình bị crash.
- **Logging**: Mọi trạng thái (Success, Skip, Error) phải được ghi nhận vào `logs/download_log.json` kèm theo record count.
