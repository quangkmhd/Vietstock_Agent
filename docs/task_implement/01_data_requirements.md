# Data Requirements: Production-Grade VN Market Data Pipeline

## 1. Dữ liệu cần thu thập
Để phục vụ hệ thống Multi-Agent Financial Advisor, cần thu thập 5 nhóm dữ liệu lõi cho mỗi doanh nghiệp và thị trường:
1. **Historical Price (OHLCV)**: Giá open, high, low, close, volume hàng ngày.
2. **Intraday & Cash Flow Data**: 
   - Giao dịch khớp lệnh chi tiết (Intraday).
   - Dữ liệu dòng tiền khối ngoại (Foreign Flow).
   - Dữ liệu dòng tiền tự doanh (Prop-trading Flow).
3. **Fundamental Data (Thông tin doanh nghiệp)**: 
   - Thông tin tổng quan (Overview): Số cổ phiếu phát hành, vốn điều lệ, mô hình kinh doanh.
   - Cấu trúc cổ đông (Shareholders) và Cấu trúc sở hữu (Ownership).
   - Ban lãnh đạo (Officers).
   - Công ty con (Subsidiaries).
   - Lịch sử thay đổi vốn (Capital History).
   - Giao dịch nội bộ (Insider Trading).
4. **Financial Data (Dữ liệu tài chính)**: 
   - Báo cáo kết quả kinh doanh (Income Statement).
   - Bảng cân đối kế toán (Balance Sheet).
   - Báo cáo lưu chuyển tiền tệ (Cash Flow).
   - Chỉ số tài chính (Ratio).
   - *Chu kỳ*: Lấy theo cả Quý (Quarter) và Năm (Year).
5. **Events & News**: 
   - Tin tức doanh nghiệp (được làm sạch HTML rác, lưu định dạng Markdown kèm Metadata).
   - Sự kiện doanh nghiệp (Trả cổ tức, phát hành thêm...).
   - Sự kiện vĩ mô thị trường (Market Events: ngày nghỉ lễ, nghẽn lệnh hệ thống từ năm 2000).

## 2. Nguồn dữ liệu (Source)
Sử dụng thư viện `vnstock` v3.4.0+ (hệ sinh thái mới, ưu tiên Vnstock News, Market Events, TA).
- Nguồn mặc định ưu tiên: **KBS** (Khuyến nghị, ổn định hơn cho batch processing, có dữ liệu chi tiết).
- Nguồn dự phòng (Fallback): **VCI** hoặc **DNSE** cho các trường hợp đặc thù (VD: Intraday, News).
- Các hàm tương ứng:
  - Giá/Flow: `Quote().history()`, `Quote().intraday()`, `StockTrading().foreign()`, `StockTrading().prop_trading()`.
  - Thông tin: `Company().overview()`, vv.
  - Tài chính: `Finance().income_statement()`, vv.
  - Tin tức: `Company().news()` lấy Markdown.

## 3. Coverage (Phạm vi dữ liệu)
- **Timeframe**: 
  - Fundamental/Price: Từ năm 2000 (tương đương `length="25Y"`) đến thời điểm hiện tại.
  - Intraday/Flow/News: Tùy thuộc vào giới hạn api của nhà cung cấp (thường vài năm gần nhất).
- **Tickers (10 mã đại diện)**: `FPT`, `HPG`, `VCB`, `MBB`, `TCB`, `VNM`, `VIC`, `SSI`, `VND`, `MWG`. (Đây là các mã Bluechip có dữ liệu lịch sử đầy đủ và ổn định).

## 4. Schema Definition

Do lưu trữ raw data từ `vnstock`, schema sẽ tương ứng với dataframe trả về. Một số field bổ sung quan trọng:

### 4.1. Dòng tiền (Foreign/Prop-trading)
- `time` / `date` (string/date): Ngày giao dịch.
- `net_buy_value` / `net_sell_value` (float): Giá trị mua/bán ròng.
- `net_buy_volume` / `net_sell_volume` (int): Khối lượng mua/bán ròng.

### 4.2. News (Markdown Format)
- `id` (string): ID bài viết.
- `title` (string): Tiêu đề.
- `publish_date` (string): Ngày xuất bản.
- `content` (string): Nội dung Markdown đã làm sạch.
- `source` (string): Nguồn (CafeF, Vietstock...).

## 5. Data Format
- **Raw format khi crawl**: Pandas DataFrame.
- **Format lưu trữ**: `Parquet` cho data bảng (Price, Flow, Finance, Fundamental), `JSON/JSONL` cho Tin tức (News) và Sự kiện (Market Events) để giữ định dạng văn bản tốt nhất. File metadata/log sẽ lưu dưới dạng `JSON`.

## 6. Storage Design
Dữ liệu được tổ chức trên disk (Local Data Lake) theo partition ticker và loại dữ liệu:
```text
data/data_lake/
└── raw/
    ├── price/
    │   └── history/
    ├── flow/
    │   ├── foreign/
    │   ├── prop_trading/
    │   └── intraday/
    ├── company/
    ├── finance/
    ├── news/
    │   └── {ticker}.jsonl
    └── market_events/
        └── vn_market_events.json
```

## 7. Crawling Strategy
- **Chiến lược**: Batch crawl toàn bộ lịch sử từ đầu đến hiện tại đối với dữ liệu mới. Bỏ qua những file đã cào (`skip if exists`).
- **Retry Logic**: Bọc mọi hàm fetch API bằng thư viện `tenacity`.
- **Rate Limit Handling**: Bổ sung `time.sleep(1)` giữa mỗi nhóm API call của một ticker để tránh bị block.
- **Logging**: Mọi trạng thái (Success, Skip, Error) phải được ghi nhận vào `logs/download_log.json` kèm theo record count.
