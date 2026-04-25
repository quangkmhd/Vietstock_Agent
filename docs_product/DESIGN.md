# System Design Doc — Vietstock Agent

> Version: 10.0 | Status: Draft | Updated: 2026-04-25

---

## 1. Overview

- **Mục tiêu system:** Hệ thống multi-agent financial advisor cho thị trường Việt Nam. Nhận câu hỏi NL tiếng Việt, điều phối agent chuyên biệt song song, trả phân tích evidence-based qua SSE streaming.
- **High-level architecture:** 5-layer (Interface → Gateway/Engine → Swarm Orchestrator → Specialized Agents → Tools/Data). ReAct reasoning loop, DAG-based swarm, 3-layer context compression.

---

## 2. Architecture Diagram

```
User (CLI / Web UI / MCP Client)
  │
  ▼
FastAPI Gateway (SSE Streaming)
  │
  ▼
AgentLoop (ReAct Engine)
  ├── Simple query → Direct answer → SSE → User
  ├── Need data? → Call tool → Observe → Loop
  └── Complex (multi-dimension)? → run_swarm()
        │
        ▼
  SwarmRuntime (DAG Fan-out)
  ┌──────┼──────┼──────┐
  ▼      ▼      ▼      ▼
Macro  Tech   Fund   Sentiment    ← Specialized Agents
  └──────┼──────┼──────┘
         ▼
  Mailbox (collect results)
         │
         ▼
  Portfolio Manager Agent
         │
         ▼
  Policy & Compliance Gate
         │
         ▼
  SSE Stream → User
```

**Data layer connections:**
```
Specialized Agents
  ├── vnstock3 (primary market data)
  ├── yfinance (fallback market data)
  ├── web_search → web_reader (news)
  ├── doc_reader (PDF + OCR)
  ├── Vector Store / RAG
  └── load_skill (SKILL.md on-demand)
```

---

## 3. Components

### 3.1 API Layer

- **Endpoint:** `POST /chat` (SSE streaming), `POST /upload` (PDF)
- **Input:** JSON `{ "query": string, "ticker?": string, "file?": binary }`
- **Output:** SSE events `{ "type": "chunk|done|error", "data": string }`
- **Auth:** API key (v10); OAuth 2.0 (future)
- **Framework:** FastAPI + SSE

### 3.2 Processing Layer

**Preprocessing:**
- Chuẩn hóa ticker: upper-case, loại ký tự thừa
- Parse time range từ NL: "3 tháng gần nhất" → `start_date`, `end_date`
- Intent classification: company_lookup / ohlcv / technical / sentiment / fundamental / investment_advice
- Context assembly: system prompt + workspace memory + conversation history

**Business logic:**
- AgentLoop (ReAct): Reason → Act → Observe → Loop
- 3-Layer Compression:
  - Micro: cắt tool result cũ sau mỗi call
  - Auto: tóm tắt khi vượt ngưỡng token
  - Manual: agent gọi `compact()`
- SwarmRuntime: DAG fan-out 4 agents song song → Mailbox → Portfolio Manager
- Policy & Compliance Gate: check disclaimer + citation trước output

### 3.3 Model Layer

- **Model dùng gì:** LLM (GPT-4o / Claude / Gemini — configurable)
- **Vì sao chọn:** LLM chỉ dùng cho reasoning/NLP — intent classification, time parsing, sentiment scoring, report synthesis, final recommendation. Mọi tính toán kỹ thuật (SMA, RSI) phải deterministic bằng Python code.

**Skill loading:**
- Agent gọi `load_skill(domain)` khi cần → nạp SKILL.md chứa rules/formulas
- Progressive disclosure: giảm base token cost

### 3.4 Data Layer

- **DB:** PostgreSQL (metadata, market data, news, audit logs)
- **Vector DB:** pgvector extension cho RAG — index BCTC, analyst reports
- **Object Storage:** PDF report originals (S3-compatible)
- **Cache:** In-memory (v10) → Redis (v20)
- **Schema chính** (chi tiết: xem [`DATA.md`](./DATA.md)):

| Table              | Key Fields                                                                  | Type         |
| ------------------ | --------------------------------------------------------------------------- | ------------ |
| `stock_price`      | ticker (VARCHAR), date (DATE), open/high/low/close (DECIMAL), volume (BIGINT) | SQL          |
| `company_profile`  | ticker, company_name, sector, industry, summary                              | SQL          |
| `financial_news`   | id (UUID), ticker_tags[], macro_tags[], title, summary, published_at, source | SQL          |
| `report_chunks`    | id (UUID), ticker, report_type, published_date, text_content, embedding (vector) | pgvector  |
| `indicator_cache`  | ticker, indicator, window, date, value                                       | SQL (cache)  |
| `audit_log`        | request_id, timestamp, gate_result, citation_count, reason                   | SQL          |

**Data volume requirements:**
- Market data: ≥ 2-3 năm lịch sử (cho SMA200), cronjob cào end-of-day
- News: ≥ 6 tháng - 1 năm, cào mỗi giờ hoặc real-time
- BCTC: 4 quý gần nhất + BCTC kiểm toán năm trước, 5-10 analyst reports/ticker

---

## 4. Data Flow

### Step-by-step request flow

```
1. User gửi query từ CLI/Web/MCP
2. FastAPI nhận request → mở SSE stream
3. AgentLoop lấy context từ Context Builder
4. Context Builder: system prompt + memory + conversation history
5. Nén context (nếu cần) qua 3-layer compression
6. AgentLoop quyết định:
   a. Simple → trả lời trực tiếp → stream về user
   b. Need data → gọi tool (vnstock3/yfinance/web_search) → observe → loop
   c. Complex → run_swarm()
7. SwarmRuntime fan-out: Macro, Technical, Fundamental, Sentiment (parallel)
8. Mỗi agent gọi tools riêng, load skill nếu cần
9. Kết quả trung gian → Mailbox
10. Portfolio Manager Agent tổng hợp → khuyến nghị
11. Policy & Compliance Gate kiểm tra:
    - Có disclaimer? Có citation?
    - Loại bỏ claim thiếu nguồn
12. SSE stream kết quả → User
```

### Search Flow (Sentiment)

```
Sentiment Analyst → web_search(ticker/sector)
  → DuckDuckGo API → URLs (ưu tiên CafeF, Vietstock, VnEconomy)
  → web_reader(url) → Jina Reader → clean markdown
  → LLM scoring → sentiment + evidence
  → Output: score + snippets + citations
```

### Caching Strategy

| Cache Key                             | TTL  | Data            |
| ------------------------------------- | ---- | --------------- |
| `{ticker}:{date}`                     | 24h  | Company info    |
| `{ticker}:{start}:{end}`             | 24h  | OHLCV           |
| `{ticker}:{indicator}:{window}:{date}`| 24h  | Indicators      |
| `{query_hash}:{date}`                 | 1h   | Search results  |

---

## 5. Scaling Strategy

### Horizontal scaling
- Phase 1 (v10): FastAPI single process, in-memory cache
- Phase 2 (v20): FastAPI behind load balancer, Redis cache, Celery/RQ queue cho swarm
- Phase 3 (v30): Kubernetes, auto-scaling, CDN cho Web UI

### Caching
- Multi-layer: company info (24h) → OHLCV (24h) → indicators (24h) → search (1h)
- Cache invalidation: TTL-based + manual purge

### Queue
- Swarm tasks qua task queue (Phase 2+)
- Priority: investment advice > single-agent queries

---

## 6. Failure Handling

### Timeout
- vnstock3/yfinance: 10s timeout → fallback hoặc error
- Web scraping: 5s timeout per URL → skip, use remaining
- LLM call: 30s timeout → retry 1x → error

### Retry
- Data source API: retry 1x với exponential backoff
- LLM call: retry 1x
- Web scraping: không retry (skip URL, dùng nguồn khác)

### Fallback & Guardrails
- vnstock3 down → yfinance (ticker mapping: `VCB` → `VCB.VN`)
- yfinance cũng down → trả error + gợi ý retry sau
- Web reader bị block (403/429/Captcha) → Thêm guardrail filter text (chặn "cloudflare", "verify you are human"). Nếu dính, lập tức skip URL, dùng URLs còn lại để tránh LLM hallucinate.
- LLM context overflow → trigger auto-compression → retry
- Compliance Gate reject → trả partial result + disclaimer
- PDF OCR fail → fallback báo warning không trích xuất được bảng số liệu (khuyến khích dùng model `camelot` thay vì OCR thuần túy).

### Client Disconnect (Zombie Task Prevention)
- Khi client ngắt kết nối đột ngột (SSE disconnect), FastAPI sẽ bắt event `request.is_disconnected()` và lập tức gọi `agent_loop.cancel()`.
- Việc này giúp ngắt ngay lập tức toàn bộ Swarm/Event Bus đang chạy ngầm, tránh lãng phí hàng nghìn token LLM vô ích.

---

## 7. Security

### Auth
- API key authentication (v10)
- OAuth 2.0 (future)
- Rate limiting per API key

### Data privacy
- Không lưu trữ câu hỏi user lâu dài (v10)
- API keys/credentials chỉ trong env vars, không bao giờ trong code/logs
- Input sanitization chống prompt injection
- Không expose stack traces / internal URLs cho user

---

## 8. Cost Estimation

| Item                  | Ước tính cost/request     | Monthly (1000 req/day) |
| --------------------- | ------------------------- | ---------------------- |
| LLM (single-agent)    | ~$0.01–0.03               | ~$300–900              |
| LLM (swarm, 5 calls)  | ~$0.05–0.15               | ~$1500–4500            |
| Data API (vnstock3)   | Free (open-source)        | $0                     |
| Web search (DDG)      | Free                      | $0                     |
| Hosting (single VPS)  | —                         | ~$20–50                |

**Tối ưu cost:**
- 3-layer compression giảm ~40% token
- Progressive skill loading giảm base cost
- Cache giảm duplicate data API calls
- Swarm chỉ kích hoạt cho US-6 (investment advice)

---

## 9. Trade-offs

| Chọn                                | Thay vì                    | Vì sao                                                    |
| ------------------------------------ | -------------------------- | ---------------------------------------------------------- |
| Swarm Event-driven (Pub/Sub)        | Sequential agent calls     | Nhanh hơn, hỗ trợ suy luận động (Dynamic Reasoning) giữa các agents |
| vnstock3 primary + yfinance fallback | Chỉ dùng 1 source         | Ưu tiên data VN, thêm reliability dù phức tạp hơn         |
| SSE streaming                       | Batch response             | UX tốt hơn (thấy kết quả sớm), chấp nhận error handling phức tạp |
| Skill loading on-demand             | Preload tất cả skills      | Tiết kiệm token, chấp nhận latency lần load đầu           |
| Evidence gating bắt buộc            | Cho phép output không citation | Tin cậy hơn, chấp nhận có thể refuse khi thiếu source    |
| Deterministic calc (SMA/RSI)        | LLM tính toán              | Chính xác 100%, phải maintain code riêng cho mỗi indicator |
| Python + FastAPI                     | Node.js / Go               | Ecosystem ML/data tốt nhất, team familiarity              |
se khi thiếu source    |
| Deterministic calc (SMA/RSI)        | LLM tính toán              | Chính xác 100%, phải maintain code riêng cho mỗi indicator |
| Python + FastAPI                     | Node.js / Go               | Ecosystem ML/data tốt nhất, team familiarity              |
