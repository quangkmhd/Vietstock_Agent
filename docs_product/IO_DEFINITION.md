# Input / Output Definition

## Vietstock Agent — Multi-Agent Financial Advisor

| Field        | Value                                            |
| ------------ | ------------------------------------------------ |
| Version      | 10.0                                             |
| Status       | Draft                                            |
| Last Updated | 2026-04-25                                       |
| Audience     | Engineers, AI Agents, Reviewers                   |

---

## 1. User Input

### 1.1 Natural Language Query

```
Input:
  - Type: Text (câu hỏi ngôn ngữ tự nhiên tiếng Việt)
  - Source: CLI / Web UI / MCP Client
  - Format: UTF-8 string, max ~2000 chars
  - Examples:
      - "Cho tôi thông tin về VCB"
      - "Giá FPT 3 tháng gần nhất"
      - "RSI 14 ngày của HPG?"
      - "Sentiment ngành thép gần đây?"
      - "Tôi nên mua hay bán VCB?"
  - Issues:
      - Ticker có thể viết sai case hoặc có ký tự thừa → cần chuẩn hóa
      - Time range mô tả mơ hồ ("gần đây") → cần LLM parse
      - Câu hỏi đa ý (hỏi cả giá lẫn sentiment) → cần intent decomposition
```

### 1.2 File Upload

```
Input:
  - Type: Document (báo cáo tài chính, analyst report)
  - Source: Web UI upload
  - Format: PDF (text-based hoặc scanned)
  - Issues:
      - Scanned PDF cần OCR → doc_reader fallback
      - File lớn → cần chunk trước khi đưa vào context
      - Encoding không chuẩn → validate trước khi process
```

---

## 2. Data Source Inputs

### 2.1 Market Data (vnstock3 — Primary)

```
Input:
  - Type: OHLCV + Company metadata
  - Source: vnstock3 Python library
  - Format: JSON / pandas DataFrame
  - Fields: ticker, open, high, low, close, volume, date, company_name, industry, exchange, market_cap
  - Issues:
      - API có thể thay đổi breaking changes
      - Rate limiting không rõ ràng
      - Một số ticker nhỏ có thể thiếu data
```

### 2.2 Market Data (yfinance — Fallback)

```
Input:
  - Type: OHLCV + Company metadata
  - Source: yfinance Python library
  - Format: JSON / pandas DataFrame
  - Fields: Tương tự vnstock3 nhưng ticker format khác (e.g., VCB.VN)
  - Issues:
      - Mapping ticker VN → yfinance format cần maintain
      - Data có thể delay hoặc thiếu cho sàn VN
      - Terms of service thay đổi
```

### 2.3 News Content

```
Input:
  - Type: Tin tức tài chính
  - Source: DuckDuckGo API → CafeF, Vietstock, VnEconomy (via web_search + web_reader)
  - Format: HTML → Clean Markdown (Jina Reader)
  - Issues:
      - Website có thể block scraping
      - Nội dung trùng lặp giữa các nguồn
      - Tin cũ lẫn với tin mới → cần filter theo date
```

### 2.4 Indexed Documents (RAG)

```
Input:
  - Type: Báo cáo tài chính, analyst reports đã index
  - Source: Vector Store (pgvector hoặc tương đương)
  - Format: Embedding vectors + metadata
  - Issues:
      - Index có thể stale → cần re-index strategy
      - Retrieval quality phụ thuộc embedding model
      - Top-k selection cần tuning
```

---

## 3. Intermediate I/O (Inter-Agent)

### 3.1 Swarm Task Assignment

```
Input (to Agent):
  - Type: Task descriptor
  - Source: SwarmRuntime
  - Format: JSON
  - Schema:
      {
        "task_id": "string",
        "agent_type": "macro|technical|fundamental|sentiment",
        "ticker": "string",
        "context": { ... },
        "skill_file": "string (optional)"
      }

Output (from Agent):
  - Type: Analysis result
  - Format: JSON
  - Schema:
      {
        "task_id": "string",
        "agent_type": "string",
        "result": {
          "summary": "string",
          "data": { ... },
          "evidence": [{ "source": "string", "snippet": "string" }],
          "confidence": "high|medium|low"
        }
      }
  - Consumer: Mailbox → Portfolio Manager Agent
  - Constraints: Phải có ít nhất 1 evidence item
```

### 3.2 Mailbox Message

```
Input/Output:
  - Type: Inter-agent message
  - Source: Any specialized agent
  - Format: JSON
  - Consumer: Portfolio Manager Agent
  - Constraints: 
      - Message size < context window budget per agent
      - Metadata phải include quality/confidence indicator
```

### 3.3 Cross-Agent Signal

```
Input/Output:
  - Type: Pub/Sub Event (Giao tiếp chéo)
  - Source: Macro Agent / Sentiment Agent / Any Agent
  - Format: JSON
  - Schema:
      {
        "signal_type": "SHOCK|TREND|UPDATE",
        "keyword": "string",
        "action": "re_evaluate|focus",
        "confidence": "high|medium|low"
      }
  - Consumer: Fundamental Agent / Technical Agent / Any Subscribing Agent
  - Constraints:
      - Phải trigger event loop để agent khác chạy lại hoặc cập nhật prompt
```

---

## 4. System Outputs

### 4.1 Company Profile (US-1)

```
Output:
  - Type: Company information
  - Format: Markdown (structured text)
  - Consumer: User (via SSE stream)
  - Schema:
      - Tên công ty
      - Mã chứng khoán (ticker)
      - Ngành
      - Sàn giao dịch
      - Vốn hóa
      - Chỉ số cơ bản
      - Nguồn dữ liệu (citation)
  - Constraints:
      - Không suy diễn vượt data gốc
      - Chỉ trả trường user hỏi (không dump toàn bộ)
```

### 4.2 OHLCV Data (US-2)

```
Output:
  - Type: Historical price data + statistics
  - Format: Markdown table + text summary
  - Consumer: User (via SSE stream)
  - Schema:
      - Bảng: date, open, high, low, close, volume
      - Summary: min/max price, %change, avg volume, số phiên
  - Constraints:
      - Summary trước, chi tiết theo yêu cầu mở rộng
      - Nêu rõ khoảng thời gian thực tế được trả
```

### 4.3 Technical Indicators (US-3)

```
Output:
  - Type: Calculated indicator values
  - Format: Markdown text
  - Consumer: User (via SSE stream)
  - Schema:
      - Indicator name + window_size
      - Current value
      - Signal interpretation (overbought/oversold/neutral)
      - Data limitation warning (nếu có)
  - Constraints:
      - Giá trị PHẢI tính bằng code deterministic
      - KHÔNG được dùng LLM để ước lượng số
```

### 4.4 Sentiment Analysis (US-4)

```
Output:
  - Type: Sentiment assessment
  - Format: Markdown text
  - Consumer: User (via SSE stream)
  - Schema:
      - Overall sentiment: positive / neutral / negative
      - Sentiment score (nếu applicable)
      - Top evidence snippets (tối đa N bài)
      - Source citations (URL + tên nguồn)
  - Constraints:
      - Mỗi nhận định sentiment phải có ≥1 source
      - Loại trùng lặp bài viết trước khi scoring
```

### 4.5 Fundamental Analysis (US-5)

```
Output:
  - Type: Financial health assessment
  - Format: Structured Markdown
  - Consumer: User (via SSE stream)
  - Schema:
      - Facts: Số liệu cụ thể (ROE, biên LN, nợ/vốn, ...)
      - Interpretation: Đánh giá dựa trên facts
      - Risks/Uncertainty: Điểm chưa rõ / rủi ro
      - Citations: Nguồn cụ thể cho mỗi fact
  - Constraints:
      - Mọi kết luận phải truy được về nguồn
      - Chỉ dùng top-k chunks quan trọng nhất
```

### 4.6 Investment Recommendation (US-6)

```
Output:
  - Type: Comprehensive investment advice
  - Format: Structured Markdown via SSE stream
  - Consumer: User
  - Schema:
      - Luận điểm chính (bull case / bear case)
      - Kịch bản tăng/giảm với xác suất tương đối
      - Mức rủi ro (high/medium/low)
      - Khuyến nghị tham khảo
      - Evidence summary từ 4 agents
      - Disclaimer rủi ro (MANDATORY)
  - Constraints:
      - PHẢI có disclaimer rủi ro đầu tư
      - PHẢI loại bỏ khẳng định thiếu nguồn
      - Output stream (không chờ toàn bộ kết thúc)
      - Compliance Gate PHẢI pass trước khi gửi user
```

### 4.7 Compliance Trace (Internal)

```
Output:
  - Type: Audit log
  - Format: Structured JSON log
  - Consumer: System / Audit team
  - Schema:
      {
        "request_id": "string",
        "timestamp": "ISO8601",
        "has_disclaimer": true/false,
        "citation_count": number,
        "uncited_claims": ["string"],
        "gate_result": "pass|fail",
        "reason": "string (if fail)"
      }
  - Constraints:
      - Log mọi request qua Compliance Gate
      - Retain logs theo policy (tối thiểu 30 ngày)
```

---

## 5. Error Responses

```
Output:
  - Type: Error message
  - Format: Markdown text via SSE stream
  - Consumer: User
  - Schema:
      - Error type: data_unavailable | source_error | timeout | compliance_fail
      - Human-readable message (tiếng Việt)
      - Suggested action (retry / rephrase / upload different file)
  - Constraints:
      - Không expose internal stack traces
      - Không expose API keys hoặc internal URLs
```
