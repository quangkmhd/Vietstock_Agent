# PRD — Vietstock Agent (Multi-Agent Financial Advisor)

> Version: 2.0 | Status: Draft | Updated: 2026-04-25

---

## 1. Executive Summary

**Problem Statement:** Nhà đầu tư cá nhân và tổ chức tại thị trường chứng khoán Việt Nam phải mất hàng giờ mỗi ngày để tổng hợp dữ liệu giá, tin tức, báo cáo tài chính từ nhiều nguồn rời rạc (CafeF, Vietstock, BCTC PDF...) trước khi ra quyết định đầu tư. Hiện chưa có giải pháp multi-agent nào phục vụ thị trường này.

**Proposed Solution:** Xây dựng hệ thống đa tác tử (multi-agent) tiếp nhận câu hỏi bằng ngôn ngữ tự nhiên tiếng Việt, tự động điều phối 4 agent chuyên biệt chạy song song (Macro, Technical, Fundamental, Sentiment), truy xuất dữ liệu thực từ nhiều nguồn, và trả về phân tích có chứng cứ kèm trích dẫn qua SSE streaming.

**Success Criteria:**

| #  | KPI                                | Target                                        | Cách đo                                |
| -- | ---------------------------------- | --------------------------------------------- | -------------------------------------- |
| S1 | Thời gian nghiên cứu cổ phiếu     | Giảm từ hàng giờ xuống < 5 phút               | User survey, session duration          |
| S2 | Latency (time to first token)      | < 15s (single-agent), < 30s (swarm)            | Latency p95 monitoring                 |
| S3 | Token cost per query               | Giảm ≥ 40% so với naive single-prompt approach | Token counter per session              |
| S4 | SMA/RSI calculation accuracy       | 100% exact match với pandas-ta library         | Unit test suite, zero tolerance        |
| S5 | Citation coverage                  | 100% — mọi factual claim phải có source        | Compliance Gate pass rate              |
| S6 | Sentiment classification F1        | ≥ 0.80 agreement với human-labeled test set    | Benchmark evaluation suite             |

### Technical Summary (for AI agents)

```
Architecture : 5-layer (Interface → Gateway → Swarm → Agents → Tools/Data)
Reasoning    : ReAct loop + 3-layer context compression
Orchestration: DAG-based Swarm parallel execution
Output       : SSE streaming, evidence-gated, compliance-checked
Stack        : Python 3.11+, FastAPI, React 19, vnstock3, yfinance
DB           : PostgreSQL + pgvector
Package mgr  : uv (KHÔNG dùng venv/virtualenv)
```

---

## 2. User Experience & Functionality

### 2.1 User Personas

| Persona              | Mô tả                                                      | Nhu cầu chính                                        |
| -------------------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| **Nhà đầu tư cá nhân** | Người chơi chứng khoán VN, hiểu biết tài chính trung bình | Tra cứu nhanh, tổng hợp sentiment, tư vấn đơn giản  |
| **Nhà phân tích tài chính** | Analyst tại CTCK, cần dữ liệu chính xác để viết report | OHLCV chi tiết, SMA/RSI chính xác, BCTC analysis     |
| **Quỹ đầu tư / tổ chức** | Quỹ cần multi-dimensional analysis trước khi ra quyết định | Tư vấn tổng hợp đa chiều (swarm), evidence-based    |

### 2.2 User Stories & Acceptance Criteria

**US-1: Tra cứu thông tin doanh nghiệp**

1. As a nhà đầu tư cá nhân, I want to tra cứu thông tin doanh nghiệp bằng mã chứng khoán, so that tôi nắm được hồ sơ cơ bản của công ty trước khi nghiên cứu sâu.

- **AC-1.1:** Nhập ticker (`VCB`, `FPT`, `HPG`) → trả về tên công ty, ngành, sàn, vốn hóa, chỉ số cơ bản trong < 10s.
- **AC-1.2:** Ticker viết sai case (`vcb`, `Vcb`) vẫn nhận diện đúng.
- **AC-1.3:** Ticker không tồn tại → trả thông báo lỗi rõ ràng, không hallucinate.
- **AC-1.4:** Output ghi rõ nguồn dữ liệu (vnstock3/yfinance) và ngày cập nhật.
- **AC-1.5:** Chỉ trả trường user hỏi (không dump toàn bộ JSON) để tiết kiệm token.

**US-2: Truy xuất giá lịch sử (OHLCV)**

2. As a nhà phân tích tài chính, I want to truy xuất dữ liệu OHLCV theo khung thời gian linh hoạt, so that tôi có data chính xác để phân tích kỹ thuật.

- **AC-2.1:** Hỗ trợ time range bằng NL ("3 tháng gần nhất") và explicit dates ("2023-01-01 đến 2023-06-30").
- **AC-2.2:** Trả bảng OHLCV + summary (min/max price, %change, avg volume, số phiên).
- **AC-2.3:** Nếu vnstock3 lỗi → tự fallback yfinance + thông báo user nguồn đã đổi.
- **AC-2.4:** Summary trước, chi tiết theo yêu cầu mở rộng (2-layer output).

**US-3: Tính chỉ báo kỹ thuật (SMA, RSI)**

3. As a nhà đầu tư cá nhân, I want to hỏi chỉ số SMA/RSI bằng ngôn ngữ tự nhiên với window_size tùy ý, so that tôi đánh giá được tín hiệu kỹ thuật mà không cần tự tính.

- **AC-3.1:** Trích xuất đúng indicator type + window_size từ câu hỏi NL.
- **AC-3.2:** Giá trị tính ra phải **100% match** với pandas-ta (deterministic code, KHÔNG dùng LLM để ước lượng).
- **AC-3.3:** Trả: giá trị hiện tại + diễn giải signal (overbought/oversold/neutral) + cảnh báo nếu data không đủ window.
- **AC-3.4:** Tự động lấy OHLCV đủ dài cho window_size yêu cầu.

**US-4: Đánh giá sentiment tin tức**

4. As a nhà đầu tư cá nhân, I want to biết sentiment tin tức gần đây của một mã hoặc ngành, so that tôi nắm được tâm lý thị trường trước khi quyết định.

- **AC-4.1:** Tìm tin tức từ ≥ 2 nguồn tài chính VN (CafeF, Vietstock, VnEconomy...).
- **AC-4.2:** Trả sentiment tổng hợp (positive/neutral/negative) + confidence level.
- **AC-4.3:** Kèm top-N evidence snippets + URL nguồn cho mỗi nhận định.
- **AC-4.4:** Loại trùng lặp bài viết giữa các nguồn trước khi scoring.
- **AC-4.5:** Mỗi nhận định sentiment phải có ≥ 1 source trích dẫn.

**US-5: Phân tích báo cáo tài chính**

5. As a nhà phân tích tài chính, I want to upload BCTC (PDF) hoặc query từ reports đã index, so that tôi có đánh giá fundamental có cấu trúc và truy nguồn được.

- **AC-5.1:** Hỗ trợ PDF text-based + scanned (OCR fallback).
- **AC-5.2:** Trả output theo cấu trúc: Facts → Interpretation → Risks/Uncertainty → Citation.
- **AC-5.3:** Mỗi fact/số liệu phải ghi rõ nguồn (page, section trong report).
- **AC-5.4:** Nếu PDF không đọc được → thông báo lỗi rõ ràng + gợi ý re-upload.
- **AC-5.5:** Chỉ dùng top-k chunks quan trọng nhất từ RAG (không nhồi full report).

**US-6: Tư vấn đầu tư tổng hợp**

6. As a quỹ đầu tư, I want to nhận khuyến nghị đầu tư tổng hợp từ 4 góc nhìn (macro, technical, fundamental, sentiment), so that tôi có cái nhìn đa chiều trước khi ra quyết định.

- **AC-6.1:** Kích hoạt Swarm chạy 4 agent song song (Macro, Technical, Fundamental, Sentiment).
- **AC-6.2:** Portfolio Manager tổng hợp: luận điểm chính (bull/bear case), kịch bản tăng/giảm, mức rủi ro, khuyến nghị tham khảo.
- **AC-6.3:** **Bắt buộc** disclaimer rủi ro đầu tư ở cuối output.
- **AC-6.4:** Loại bỏ mọi khẳng định thiếu nguồn trích dẫn (Compliance Gate).
- **AC-6.5:** SSE streaming — user thấy kết quả sớm, không phải chờ toàn bộ.
- **AC-6.6:** Latency < 30s (p95) cho full swarm execution.

**US-7: Multi-turn conversation**

7. As a nhà đầu tư cá nhân, I want to hỏi follow-up questions dựa trên context trước đó, so that tôi không phải lặp lại thông tin đã cung cấp.

- **AC-7.1:** Agent nhớ context trong cùng session (ticker, time range, kết quả trước).
- **AC-7.2:** 3-layer compression giữ context quan trọng khi conversation dài.
- **AC-7.3:** User có thể đổi ticker/topic mà không cần mở session mới.

**US-8: Error handling & graceful degradation**

8. As a user, I want to nhận thông báo rõ ràng khi hệ thống gặp lỗi, so that tôi biết phải làm gì tiếp theo.

- **AC-8.1:** Khi data source down → thông báo rõ nguồn nào lỗi + fallback tự động nếu có.
- **AC-8.2:** Khi LLM timeout → retry 1x + thông báo nếu vẫn lỗi.
- **AC-8.3:** Không expose stack traces, API keys, hay internal URLs.
- **AC-8.4:** Mọi error message bằng tiếng Việt + gợi ý action (retry/rephrase/re-upload).

### 2.3 Non-Goals (v10)

- Auto-trading (thực thi giao dịch tự động)
- Portfolio tracking (quản lý danh mục thực, P&L tracking)
- Real-time intraday data (v10 chỉ end-of-day)
- Mobile app
- Đa ngôn ngữ (v10 chỉ tiếng Việt + ticker quốc tế hạn chế)
- User authentication / multi-tenancy (v10 dùng API key đơn giản)

---

## 3. AI System Requirements

### 3.1 Tool Requirements

| Tool          | API/Library        | Mục đích                                 | Fallback             |
| ------------- | ------------------ | ---------------------------------------- | -------------------- |
| `get_company_info` | vnstock3      | Lấy company metadata                    | yfinance             |
| `get_ohlcv`        | vnstock3      | Lấy dữ liệu OHLCV theo range           | yfinance             |
| `calculate_indicator` | Python code | Tính SMA/RSI deterministic               | Không (critical)     |
| `web_search`       | DuckDuckGo API | Tìm tin tức tài chính VN                | —                    |
| `web_reader`       | Jina Reader    | Extract clean text/markdown từ URL       | —                    |
| `doc_reader`       | pdfplumber+OCR | Đọc PDF (text + scanned)                | —                    |
| `load_skill`       | File loader    | Nạp SKILL.md on-demand (progressive)     | —                    |
| `run_swarm`        | SwarmRuntime   | Chạy 4 agent song song + Portfolio Manager | Sequential fallback |

### 3.2 LLM Usage Rules

| Task                      | Dùng LLM? | Phương pháp                           |
| ------------------------- | --------- | ------------------------------------- |
| Intent classification     | ✅ Yes    | ReAct reasoning                       |
| Time range parsing (NL)   | ✅ Yes    | Structured extraction                 |
| SMA/RSI calculation       | ❌ **No** | **Deterministic Python code only**    |
| Sentiment scoring         | ✅ Yes    | Classification on clean text          |
| Report summarization      | ✅ Yes    | Structured extraction from RAG chunks |
| Final recommendation      | ✅ Yes    | Synthesis + evidence gating           |

### 3.3 Evaluation Strategy

| Khía cạnh              | Benchmark                                               | Pass threshold      |
| ---------------------- | ------------------------------------------------------- | -------------------- |
| SMA/RSI correctness    | 50 test cases so sánh output vs pandas-ta               | 100% exact match     |
| Intent classification  | 100 câu hỏi test (phân bổ đều 6 use cases)              | ≥ 95% correct intent |
| Sentiment accuracy     | 100 bài viết tài chính VN đã human-labeled              | F1 ≥ 0.80           |
| Citation coverage      | 200 output samples checked cho uncited claims            | 100% cited           |
| Hallucination rate     | 200 output samples checked cho fabricated info           | < 5%                |
| End-to-end latency     | 100 queries mixed (single + swarm)                       | p95 < 30s           |

> Chi tiết evaluation framework: xem [`EVALUATION.md`](./EVALUATION.md)
> Chi tiết prompt versions: xem [`PROMPTS.md`](./PROMPTS.md)

---

## 4. Technical Specifications

### 4.1 Architecture Overview

5-layer architecture:

```
Layer 1: Interface        → CLI/TUI, React 19 Web UI (SSE), MCP Client
Layer 2: Gateway & Engine → FastAPI (SSE), AgentLoop (ReAct), Context Builder, 3-Layer Compression
Layer 3: Swarm            → SwarmRuntime, Worker Registry, Mailbox, Policy & Compliance Gate
Layer 4: Agents           → Macro, Technical, Fundamental, Sentiment, Portfolio Manager
Layer 5: Tools & Data     → vnstock3, yfinance, DuckDuckGo, Jina, doc_reader, pgvector
```

> Chi tiết architecture & data flow: xem [`DESIGN.md`](./DESIGN.md)

### 4.2 Integration Points

| Integration     | Protocol      | Direction    | Notes                              |
| --------------- | ------------- | ------------ | ---------------------------------- |
| vnstock3        | Python lib    | Inbound data | Primary market data, no auth       |
| yfinance        | Python lib    | Inbound data | Fallback, ticker mapping required  |
| DuckDuckGo      | HTTP API      | Inbound data | News search, no auth               |
| Jina Reader     | HTTP API      | Inbound data | URL → markdown extraction          |
| LLM Provider    | HTTP API      | Outbound     | GPT-4o/Claude/Gemini, API key auth |
| PostgreSQL      | TCP (psycopg) | Bidirectional| Metadata, sessions, audit          |
| pgvector        | TCP (psycopg) | Bidirectional| RAG embeddings                     |
| Object Storage  | HTTP/S3 API   | Outbound     | PDF report storage                 |

### 4.3 Security & Privacy

- API key authentication (v10); OAuth 2.0 (future)
- Credentials chỉ trong env vars, không bao giờ trong code/logs
- Input sanitization chống LLM prompt injection
- Không lưu trữ câu hỏi user lâu dài (v10)
- Rate limiting: 60 req/min per API key
- Mandatory disclaimer trên mọi output tư vấn
- Không expose stack traces / internal URLs cho user

> Chi tiết API spec: xem [`API.md`](./API.md)

---

## 5. Implementation Decisions

### 5.1 Deep Modules (testable in isolation)

| Module                    | Interface                                           | Encapsulates                                        |
| ------------------------- | --------------------------------------------------- | --------------------------------------------------- |
| **DataSourceAdapter**     | `get_company(ticker) → CompanyInfo`<br>`get_ohlcv(ticker, start, end) → DataFrame` | vnstock3/yfinance switching, ticker normalization, caching, fallback logic |
| **IndicatorCalculator**   | `calculate(ticker, indicator, window) → IndicatorResult` | OHLCV fetching, SMA/RSI computation (deterministic), data validation |
| **ContextCompressor**     | `compress(context, budget) → CompressedContext`     | Micro/Auto/Manual compression, token counting, priority ranking |
| **ComplianceGate**        | `check(response) → GateResult`                      | Disclaimer validation, citation checking, uncited claim detection |
| **SentimentPipeline**     | `analyze(ticker_or_sector) → SentimentResult`       | web_search → web_reader → dedup → LLM scoring → aggregation |
| **SwarmRuntime**          | `run(task) → SwarmResult`                            | Event-driven fan-out, Pub/Sub event bus, Shared State, timeout handling |

### 5.2 Architectural Decisions

- **LLM for reasoning only** — Mọi tính toán (SMA, RSI) phải deterministic bằng Python code
- **Agents as single-task microservices** — Mỗi agent có 1 responsibility duy nhất
- **Evidence-gated output** — ComplianceGate reject output thiếu citation
- **Progressive skill loading** — `load_skill()` on-demand để giảm base token cost
- **Fallback-first data layer** — DataSourceAdapter tự switch vnstock3 → yfinance
- **SSE streaming** — Output stream để giảm perceived latency

### 5.3 Database Schema

> Chi tiết từ `docs/DATA_ARCHITECTURE.md`

| Table               | Key Fields                                                              | Purpose           |
| ------------------- | ----------------------------------------------------------------------- | ------------------ |
| `stock_price`       | ticker (VARCHAR), date (DATE), open/high/low/close (DECIMAL), volume (BIGINT) | OHLCV time-series |
| `company_profile`   | ticker, company_name, sector, industry, summary                          | Company metadata   |
| `financial_news`    | id (UUID), ticker_tags[], macro_tags[], title, summary, published_at, source | News + sentiment  |
| `report_chunks`     | id (UUID), ticker, report_type, published_date, text_content, embedding (vector) | RAG for BCTC/reports |
| `audit_log`         | request_id, timestamp, gate_result, citation_count, reason               | Compliance trace   |

### 5.4 API Contracts

> Chi tiết: xem [`API.md`](./API.md)

- `POST /chat` — SSE streaming query (JSON → SSE events)
- `POST /upload` — PDF upload + analysis (multipart → SSE events)
- `GET /health` — Health check (JSON)

---

## 6. Testing Decisions

### 6.1 Testing Philosophy

- Chỉ test **external behavior** (input → output), không test implementation details
- Mỗi deep module (Section 5.1) phải có test suite riêng
- Integration tests cho end-to-end flows (US-1 → US-8)

### 6.2 Module Test Plan

| Module                | Test Type     | Cần test gì                                                    |
| --------------------- | ------------- | -------------------------------------------------------------- |
| DataSourceAdapter     | Unit          | Ticker normalization, fallback logic, cache hit/miss           |
| IndicatorCalculator   | Unit          | SMA/RSI correctness vs pandas-ta (100% exact match required)  |
| ContextCompressor     | Unit          | Token count reduction, important context retention             |
| ComplianceGate        | Unit          | Reject uncited claims, require disclaimer, pass valid output   |
| SentimentPipeline     | Integration   | End-to-end: query → search → extract → score → aggregate      |
| SwarmRuntime          | Integration   | Parallel execution, timeout handling, result aggregation       |
| API endpoints         | E2E           | Request → SSE stream → correct output format                  |

### 6.3 What Makes a Good Test

```diff
# BAD — tests implementation details
- assert agent._internal_state == "reasoning"
- assert len(agent._tool_calls) == 3

# GOOD — tests external behavior
+ assert calculate_sma("VCB", 20) == pandas_ta_sma("VCB", 20)
+ assert "disclaimer" in compliance_gate.check(investment_advice).output
+ assert sentiment_result.citations >= 1
```

### 6.4 Evaluation vs Unit Tests

- **Unit tests:** Correctness (deterministic, pass/fail)
- **Evaluation:** Quality metrics (accuracy, F1, latency) — tracked in [`EVALUATION.md`](./EVALUATION.md)
- **Prompt regression:** Track prompt version changes → re-run eval suite — tracked in [`PROMPTS.md`](./PROMPTS.md)

---

## 7. Risks & Roadmap

### 7.1 Technical Risks

| Risk                              | Impact | Likelihood | Mitigation                                                  |
| --------------------------------- | ------ | ---------- | ----------------------------------------------------------- |
| vnstock3 API breaking changes     | High   | Medium     | DataSourceAdapter abstraction + yfinance fallback            |
| LLM hallucination tài chính      | High   | High       | Evidence gating + citation bắt buộc + deterministic calc    |
| Token cost vượt budget (swarm)    | Medium | High       | 3-layer compression + progressive skill loading             |
| Web scraping bị block             | Medium | Medium     | Rate limiting + domain rotation + fallback                  |
| Context window overflow           | Medium | Medium     | Auto-compression + chunk splitting                          |
| Prompt injection attacks          | Medium | Low        | Input sanitization + system prompt hardening                |

### 7.2 Phased Rollout

| Phase    | Deliverable                                          | Duration     |
| -------- | ---------------------------------------------------- | ------------ |
| **v10**  | Core Engine + Data Layer + Technical/Fundamental Agent + CLI | 5–8 tuần |
| **v10** | + Sentiment/Macro Agent + Swarm + Compliance Gate + Web UI   | 4–6 tuần |
| **v11** | + Performance optimization + evaluation suite + monitoring    | 2–3 tuần |
| **v20** | + Multi-tenancy + advanced indicators + mobile               | TBD      |

---

## 8. Constraints

### Data
- vnstock3 là nguồn chính; yfinance là fallback — cả hai phụ thuộc upstream API
- Lịch sử giá cần ≥ 2-3 năm (cho SMA200); tin tức cần ≥ 6 tháng; BCTC cần ≥ 4 quý
- Vector Store cần re-index strategy cho báo cáo mới

### Legal
- Mọi output tư vấn **phải** kèm disclaimer rủi ro đầu tư
- Không được đưa ra khẳng định thiếu nguồn trích dẫn
- Không auto-trading → tránh trách nhiệm pháp lý

### Tech
- LLM **không** được tính toán chỉ báo kỹ thuật → code deterministic bắt buộc
- Token budget giới hạn → 3-layer compression
- SSE streaming bắt buộc cho output
- Package management: `uv` (không venv/virtualenv)

---

## 9. Further Notes

- IO Definition chi tiết: [`IO_DEFINITION.md`](./IO_DEFINITION.md)
- Data schemas & sources: [`DATA.md`](./DATA.md)
- Prompt versions & documentation: [`PROMPTS.md`](./PROMPTS.md)
- Production runbook: [`RUNBOOK.md`](./RUNBOOK.md)
- Troubleshooting: [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md)
OTING.md)
NG.md)
