# Evaluation Doc — Vietstock Agent

> Version: 20.0 | Status: Template | Updated: 2026-04-25
>
> Cross-ref: PRD §3.3 Evaluation Strategy → [`PRD.md`](./PRD.md#33-evaluation-strategy)

---

## Dataset

- **Số lượng:** 120 câu hỏi (planned)
- **Phân bổ:**

| Use Case                        | # Câu hỏi | Loại câu hỏi                                |
| ------------------------------- | ---------- | -------------------------------------------- |
| US-1: Company lookup            | 15         | Ticker VN phổ biến + edge cases              |
| US-2: OHLCV                     | 15         | Time range NL + explicit dates               |
| US-3: Technical indicators      | 20         | SMA/RSI với window_size khác nhau            |
| US-4: Sentiment                 | 15         | Ticker + sector queries                      |
| US-5: Fundamental               | 15         | BCTC analysis + PDF upload                   |
| US-6: Investment advice (swarm) | 20         | Multi-dimension, cần 4 agents                |
| US-7: Multi-turn conversation   | 10         | Follow-up questions, context retention       |
| US-8: Error handling            | 10         | Invalid ticker, timeout, missing data        |

- **Ground truth:** Human-annotated expected outputs

---

## Metrics

| Metric                | Áp dụng cho       | Cách đo                                            | Pass threshold |
| --------------------- | ------------------ | -------------------------------------------------- | -------------- |
| Factual Accuracy      | US-1, US-2, US-3   | So sánh output vs data source (exact match)        | ≥ 95%          |
| SMA/RSI Correctness   | US-3               | So sánh vs pandas-ta library                       | 100%           |
| Intent Classification | All                | Correct use case routing vs expected intent         | ≥ 95%          |
| Sentiment F1          | US-4               | F1 score vs human labels (positive/neutral/negative)| ≥ 0.80        |
| Citation Coverage     | All                | % claims có source / total claims                  | 100%           |
| Hallucination Rate    | All                | % responses chứa thông tin không có trong source   | < 5%           |
| BLEU/ROUGE (optional) | US-5, US-6         | So sánh summary quality vs reference               | TBD            |
| Latency               | All                | TTFT (time to first token), p50/p95                | p95 < 30s      |
| Token Usage           | All                | Tokens per query (input + output)                  | < budget       |

---

## Result

> Điền khi chạy evaluation.

| Case ID | Use Case | Query                                  | Expected                  | Output | Pass | Notes |
| ------- | -------- | -------------------------------------- | ------------------------- | ------ | ---- | ----- |
| E001    | US-1     | "Thông tin VCB"                        | Company profile VCB       | —      | —    | TBD   |
| E002    | US-2     | "Giá FPT 3 tháng gần nhất"            | OHLCV table + summary     | —      | —    | TBD   |
| E003    | US-3     | "SMA 20 của HPG"                       | Exact SMA value           | —      | —    | TBD   |
| E004    | US-3     | "RSI 14 của VCB"                       | Exact RSI value           | —      | —    | TBD   |
| E005    | US-4     | "Sentiment ngành thép"                 | Sentiment + evidence      | —      | —    | TBD   |
| E006    | US-5     | "Đánh giá tài chính VNM"              | Facts/Interp/Risks/Cite   | —      | —    | TBD   |
| E007    | US-6     | "Nên mua hay bán VCB?"                | Full recommendation       | —      | —    | TBD   |
| ...     | ...      | ...                                    | ...                       | —      | —    | TBD   |

### Aggregate Results

| Metric                | Target    | Actual | Status |
| --------------------- | --------- | ------ | ------ |
| Factual Accuracy      | ≥ 95%     | —      | TBD    |
| SMA/RSI Correctness   | 100%      | —      | TBD    |
| Sentiment F1          | ≥ 0.80    | —      | TBD    |
| Citation Coverage     | 100%      | —      | TBD    |
| Hallucination Rate    | < 5%      | —      | TBD    |
| Latency p95 (single)  | < 15s     | —      | TBD    |
| Latency p95 (swarm)   | < 30s     | —      | TBD    |

---

## Error Analysis

> Điền sau khi chạy evaluation.

### Sai do Retrieval
- Mô tả: RAG trả về chunk không liên quan
- Tần suất: TBD
- Fix: Cải thiện embedding model / chunking strategy

### Sai do Prompt
- Mô tả: Agent không follow instruction đúng
- Tần suất: TBD
- Fix: Cập nhật prompt (xem `PROMPTS.md`)

### Sai do Model
- Mô tả: LLM hallucinate dù prompt và retrieval đúng
- Tần suất: TBD
- Fix: Đổi model / thêm evidence gating rule

### Sai do Data
- Mô tả: Data source thiếu hoặc sai
- Tần suất: TBD
- Fix: Thêm data source / cải thiện data cleaning

---

## Conclusion

> Điền sau khi hoàn thành evaluation cycle đầu tiên.
