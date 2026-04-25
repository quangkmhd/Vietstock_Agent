# Model / Experiment Doc — Vietstock Agent

> Version: 10.0 | Status: Template (chưa có experiment) | Updated: 2026-04-25

---

## Experiment 1: LLM Selection for AgentLoop

### Goal
- Chọn LLM phù hợp nhất cho AgentLoop: cân bằng accuracy, latency, cost.

### Setup
- **Model candidates:** GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet, Gemini 2.0 Flash
- **Data:** 50 câu hỏi test (10 per use case US-1 → US-5), 10 câu US-6 (swarm)
- **Prompt:** System prompt v10 (xem `PROMPTS.md`)
- **Metrics tracked:** Accuracy, latency (TTFT), cost per query

### Metrics

| Model             | Accuracy | Latency (TTFT) | Cost/query | Notes |
| ----------------- | -------- | --------------- | ---------- | ----- |
| GPT-4o            | —        | —               | —          | TBD   |
| GPT-4o-mini       | —        | —               | —          | TBD   |
| Claude 3.5 Sonnet | —        | —               | —          | TBD   |
| Gemini 2.0 Flash  | —        | —               | —          | TBD   |

### Result
- TBD — chạy experiment khi v10 (Core Engine) hoàn thành.

### Conclusion
- TBD

### Next Step
- Implement evaluation harness (xem `EVALUATION.md`)
- Chạy experiment sau v10

---

## Experiment 2: Embedding Model for RAG

### Goal
- Chọn embedding model cho Vector Store: cân bằng retrieval quality và cost.

### Setup
- **Model candidates:** OpenAI text-embedding-3-small, text-embedding-3-large, Cohere embed-v3, local model (bge-m3)
- **Data:** 20 báo cáo tài chính VN (PDF), 100 câu hỏi test
- **Metrics tracked:** Retrieval accuracy (top-5 hit rate), embedding cost, latency

### Metrics

| Model                        | Top-5 Hit Rate | Cost/1K docs | Latency | Notes |
| ---------------------------- | -------------- | ------------ | ------- | ----- |
| text-embedding-3-small       | —              | —            | —       | TBD   |
| text-embedding-3-large       | —              | —            | —       | TBD   |
| Cohere embed-v3              | —              | —            | —       | TBD   |
| bge-m3 (local)               | —              | —            | —       | TBD   |

### Result
- TBD

### Conclusion
- TBD

### Next Step
- Chuẩn bị test set báo cáo tài chính VN
- Implement retrieval benchmark

---

## Experiment 3: Context Compression Effectiveness

### Goal
- Đo hiệu quả 3-layer compression: giảm bao nhiêu % token mà không mất accuracy.

### Setup
- **Model:** Chọn từ Experiment 1
- **Data:** 30 multi-turn conversations (5-10 turns mỗi conversation)
- **Prompt:** System prompt v10
- **Compare:** No compression vs Micro-only vs Micro+Auto vs Full (Micro+Auto+Manual)

### Metrics

| Strategy         | Avg tokens/turn | Accuracy drop | Cost saving | Notes |
| ---------------- | --------------- | ------------- | ----------- | ----- |
| No compression   | —               | baseline      | 0%          | TBD   |
| Micro only       | —               | —             | —           | TBD   |
| Micro + Auto     | —               | —             | —           | TBD   |
| Full (3-layer)   | —               | —             | —           | TBD   |

### Result
- TBD

### Conclusion
- TBD

### Next Step
- Implement compression layers
- Create multi-turn test conversations
