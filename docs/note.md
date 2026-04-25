 1. Cần cào (scrape) những dữ liệu gì?
   4 loại dữ liệu chính để phục vụ 4 Agent tương ứng:
   - Dữ liệu giao dịch (Market Data): Giá mở cửa, đóng cửa, cao nhất, thấp nhất, khối lượng giao dịch (OHLCV).
   - Thông tin & Hồ sơ doanh nghiệp: Ngành nghề, vốn hóa, thông tin cơ bản.
   - Tin tức & Sự kiện vĩ mô (News & Macro): Tin tức báo chí về công ty, ngành, và các yếu tố vĩ mô (giá dầu, chiến tranh, lãi suất...).
   - Báo cáo chuyên sâu (Fundamental Data): Báo cáo tài chính (BCTC) các quý/năm, báo cáo phân tích từ các công ty chứng khoán (SSI, VNDirect, HSC...).

  2. Định dạng & Nơi lưu trữ

   * Dữ liệu dạng chuỗi thời gian (Giá, Khối lượng) & Thông tin cơ bản: 
       * Nơi lưu trữ: Cơ sở dữ liệu quan hệ PostgreSQL, có thể cài thêm extension TimescaleDB cho dữ liệu time-series hoặc pgvector cho vector.
       * Định dạng: Các dòng dữ liệu trong bảng SQL.
   * Tin tức (News): 
       * Nơi lưu trữ: PostgreSQL để search text nhanh hơn.
       * Định dạng: dùng llm để tạo ra JSON có cấu trúc từ raw data  
   * Báo cáo tài chính & Báo cáo phân tích (RAG System):
       * Nơi lưu trữ: File gốc (PDF) lưu ở Object Storage
       * Vector Database: Các file PDF này phải được đọc ra, chia nhỏ (chunking), biến thành vector (embedding) và lưu vào Vector DB (pgvector của PostgreSQL).

  3. Lưu các trường (fields) gì?
  Dưới đây là schema thiết kế cơ bản cho các luồng dữ liệu:

  A. Bảng Dữ liệu giá (SQL - Bảng stock_price)
   * ticker (Mã CK - VARCHAR)
   * date (Ngày giao dịch - DATE)
   * open (Giá mở cửa - DECIMAL)
   * high (Giá cao nhất - DECIMAL)
   * low (Giá thấp nhất - DECIMAL)
   * close (Giá đóng cửa - DECIMAL)
   * volume (Khối lượng - BIGINT)
  (Chỉ số SMA, RSI không cần cào mà Agent sẽ tự tính toán dựa trên các trường này).

  B. Bảng Thông tin doanh nghiệp (SQL - Bảng company_profile)
   * ticker (Mã CK)
   * company_name (Tên công ty)
   * sector / industry (Ngành nghề - phục vụ cho Knowledge Graph)
   * summary (Mô tả ngắn về công ty)

  C. Bảng Tin tức (SQL hoặc MongoDB - Bảng financial_news)
   * id (UUID)
   * ticker_tags (Danh sách các mã CK được nhắc đến trong bài, VD: ['PLX', 'GAS'])
   * macro_tags (Tag vĩ mô, VD: ['oil_price', 'war'] - phục vụ Knowledge Graph)
   * title (Tiêu đề)
   * summary (Tóm tắt nội dung - dùng LLM nhỏ tóm tắt lúc cào để tiết kiệm token khi Agent đọc)
   * published_at (Thời gian xuất bản)
   * source (Nguồn: CafeF, Vietstock...)

  D. Vector DB cho Báo cáo (Dùng cho Fundamental Agent)
   * id (UUID chunk)
   * ticker (Mã CK)
   * report_type (Loại báo cáo: BCTC_Q3, Bao_cao_phan_tich)
   * published_date (Ngày phát hành)
   * text_content (Đoạn text đã được chunk từ PDF)
   * embedding (Vector array)

  4. Cào bao nhiêu là đủ? (Khối lượng dữ liệu)
   * Dữ liệu giá (Market Data): Nên cào lịch sử ít nhất 2 đến 3 năm để Agent có đủ data tính các đường MA dài hạn (như
     SMA200) và để đối chiếu chu kỳ. Sau đó, setup cronjob cào hàng ngày (End of Day).
   * Tin tức (News): Lịch sử khoảng 6 tháng đến 1 năm gần nhất để có thể phân tích sentiment và các sự kiện vĩ mô ảnh
     hưởng. Sau đó cào real-time hoặc mỗi giờ.
   * Báo cáo (PDF): Cần BCTC của 4 quý gần nhất (1 năm) + BCTC kiểm toán năm trước đó. Báo cáo phân tích của các công ty
     chứng khoán thì cào khoảng 5 - 10 báo cáo mới nhất cho mỗi mã.
