# Data Documentation — Vietstock Agent

> Version: 20.0 | Status: Draft | Updated: 2026-04-25

---

## Storage Architecture

| Storage             | Technology         | Purpose                          |
| ------------------- | ------------------ | -------------------------------- |
| Relational DB       | PostgreSQL         | Market data, company info, news, audit |
| Vector DB           | pgvector (PG ext)  | RAG embeddings cho BCTC/reports  |
| Object Storage      | S3-compatible      | PDF report originals             |
| Cache               | In-memory (v10) → Redis (v20) | OHLCV, indicators, search |

---

## Table 1: `stock_price` — Dữ liệu giá lịch sử

### Source
- **Primary:** vnstock3 Python library (HOSE/HNX/UPCOM)
- **Fallback:** yfinance (ticker format: `VCB.VN`)
- **Ingestion:** Cronjob cào end-of-day

### Schema

| Field    | Type        | Constraint       | Description            |
| -------- | ----------- | ---------------- | ---------------------- |
| ticker   | VARCHAR(10) | NOT NULL, INDEX  | Mã chứng khoán         |
| date     | DATE        | NOT NULL         | Ngày giao dịch         |
| open     | DECIMAL     | NOT NULL         | Giá mở cửa            |
| high     | DECIMAL     | NOT NULL         | Giá cao nhất           |
| low      | DECIMAL     | NOT NULL         | Giá thấp nhất          |
| close    | DECIMAL     | NOT NULL         | Giá đóng cửa          |
| volume   | BIGINT      | NOT NULL         | Khối lượng giao dịch   |

- **PK:** (ticker, date)
- **Data Volume:** ~1,800 ticker × 250 phiên/năm × ≥ 2-3 năm = ~1M+ rows
- **Note:** SMA/RSI KHÔNG lưu ở đây — Agent tính deterministic từ OHLCV

### Cleaning
- Chuẩn hóa ticker: upper-case, strip whitespace
- Loại phiên không giao dịch (volume = 0 vào ngày nghỉ)
- Xử lý stock split / adjusted price (nếu có)

### Issues
- vnstock3 API có thể breaking changes không báo trước
- Một số ticker penny stock có thể thiếu data
- yfinance fallback: ticker mapping `VCB` → `VCB.VN` cần maintain thủ công

---

## Table 2: `company_profile` — Hồ sơ doanh nghiệp

### Source
- vnstock3 company metadata API

### Schema

| Field         | Type         | Constraint       | Description                          |
| ------------- | ------------ | ---------------- | ------------------------------------ |
| ticker        | VARCHAR(10)  | PK               | Mã chứng khoán                       |
| company_name  | VARCHAR(255) | NOT NULL         | Tên đầy đủ công ty                   |
| sector        | VARCHAR(100) |                  | Ngành (cho Knowledge Graph)          |
| industry      | VARCHAR(100) |                  | Phân ngành chi tiết                  |
| summary       | TEXT         |                  | Mô tả ngắn về công ty               |

- **Data Volume:** ~1,800 rows (1 per ticker)
- **Cache TTL:** 24h per ticker

---

## Table 3: `financial_news` — Tin tức tài chính

### Source
- DuckDuckGo API → ưu tiên domain tài chính VN: CafeF, Vietstock, VnEconomy, DNSE
- Content extraction: Jina Reader (HTML → clean Markdown)

### Schema

| Field         | Type         | Constraint       | Description                              |
| ------------- | ------------ | ---------------- | ---------------------------------------- |
| id            | UUID         | PK               | ID tin tức                               |
| ticker_tags   | VARCHAR[]    | INDEX            | Mã CK được đề cập (VD: `['PLX','GAS']`) |
| macro_tags    | VARCHAR[]    |                  | Tags vĩ mô (VD: `['oil_price','war']`)  |
| title         | VARCHAR(500) | NOT NULL         | Tiêu đề bài viết                        |
| summary       | TEXT         |                  | Tóm tắt (LLM tóm khi cào, tiết kiệm token) |
| published_at  | TIMESTAMP    | NOT NULL, INDEX  | Thời gian xuất bản                       |
| source        | VARCHAR(100) | NOT NULL         | Nguồn (CafeF, Vietstock...)             |

- **Data Volume:** ≥ 6 tháng - 1 năm lịch sử, cào mỗi giờ hoặc real-time
- **Ingestion:** summary được LLM nhỏ tóm tắt lúc cào để tiết kiệm token khi Agent đọc

### Cleaning
- Loại HTML tags, ads, navigation → Jina Reader tự xử lý
- Deduplicate bài viết giống nhau giữa các nguồn
- Filter theo date: ưu tiên tin mới (< 7 ngày)

### Issues
- Website có thể block scraping (403/429)
- Nội dung trùng lặp giữa các nguồn (syndicated content)
- Bias nguồn tin VN (thiên tích cực hoặc tiêu cực theo trend)

---

## Table 4: `report_chunks` — Vector DB cho RAG (pgvector)

### Source
- User upload (PDF via `/upload` endpoint)
- Pre-indexed: BCTC công ty niêm yết, analyst reports từ CTCK (SSI, VNDirect, HSC...)

### Schema

| Field           | Type         | Constraint       | Description                            |
| --------------- | ------------ | ---------------- | -------------------------------------- |
| id              | UUID         | PK               | Chunk ID                               |
| ticker          | VARCHAR(10)  | NOT NULL, INDEX  | Mã CK liên quan                       |
| report_type     | VARCHAR(50)  | NOT NULL         | `BCTC_Q3`, `Bao_cao_phan_tich`, etc.  |
| published_date  | DATE         |                  | Ngày phát hành report                  |
| text_content    | TEXT         | NOT NULL         | Đoạn text đã chunk từ PDF             |
| embedding       | VECTOR(1536) | NOT NULL         | Embedding vector (dimension tùy model) |

- **Data Volume:** 4 quý BCTC gần nhất + BCTC kiểm toán năm trước + 5-10 analyst reports per ticker
- **Chunk config:** ~500-1000 tokens per chunk, overlap 100 tokens
- **Object Storage:** PDF gốc lưu S3, chỉ chunks + embedding trong pgvector

### Cleaning & Guardrails
- PDF text extraction (pdfplumber)
- OCR fallback cho scanned PDF (Tesseract)
- Normalize Vietnamese text encoding (UTF-8)
- Metadata extraction: year, quarter, company, CTCK name (semi-auto via LLM)
- **RAG Guardrail:** BẮT BUỘC thực hiện Pre-filter Metadata theo thời gian (`WHERE published_date >= NOW() - INTERVAL '2 years'`) TRƯỚC khi chạy Vector Similarity Search để tránh "bóng ma" BCTC cũ.

### Issues
- Scanned PDF quality ảnh hưởng OCR accuracy (khuyến nghị dùng table detection model như `camelot` thay vì OCR thuần túy)
- Table extraction từ PDF rất khó → có thể mất data bảng, cần trả warning nếu extraction fail
- Index stale → cần re-index strategy
- Retrieval quality phụ thuộc embedding model + chunk strategy

---

## Table 5: `indicator_cache` — Cache chỉ báo kỹ thuật

### Schema

| Field      | Type        | Constraint       | Description              |
| ---------- | ----------- | ---------------- | ------------------------ |
| ticker     | VARCHAR(10) | NOT NULL         | Mã CK                   |
| indicator  | VARCHAR(10) | NOT NULL         | `SMA` / `RSI`           |
| window     | INTEGER     | NOT NULL         | Window size (14, 20, 50) |
| date       | DATE        | NOT NULL         | Ngày tính                |
| value      | DECIMAL     | NOT NULL         | Giá trị calculated       |

- **PK:** (ticker, indicator, window, date)
- **TTL:** 24h — invalidate khi có OHLCV mới
- **Note:** Values tính deterministic bằng Python code, KHÔNG bởi LLM

---

## Table 6: `audit_log` — Compliance trace

### Schema

| Field          | Type         | Constraint       | Description                    |
| -------------- | ------------ | ---------------- | ------------------------------ |
| request_id     | UUID         | PK               | Request identifier             |
| timestamp      | TIMESTAMP    | NOT NULL, INDEX  | Thời điểm check                |
| gate_result    | VARCHAR(10)  | NOT NULL         | `pass` / `fail` / `partial`   |
| citation_count | INTEGER      | NOT NULL         | Số citations trong output      |
| reason         | TEXT         |                  | Lý do reject (nếu fail)       |

---

## Version History

| Version | Changes                                            |
| ------- | -------------------------------------------------- |
| v10    | Initial schema design                              |
| v20    | Aligned with canonical schema from `docs/note.md`; added data volume requirements, SQL types, constraints |
