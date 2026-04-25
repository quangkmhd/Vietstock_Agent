# Troubleshooting Guide — Vietstock Agent

> Version: 10.0 | Status: Draft | Updated: 2026-04-25

---

## Symptom 1: Model trả sai số liệu (SMA/RSI sai)

### Possible Causes
1. LLM tự tính thay vì gọi tool deterministic
2. OHLCV data thiếu (không đủ datapoints cho window_size)
3. Tool `calculate_indicator` có bug

### Debug Steps
1. Check tool call log: agent có gọi `calculate_indicator()` không?
   ```bash
   grep "calculate_indicator" logs/app.log | tail -20
   ```
2. Nếu không có tool call → prompt issue (LLM tự tính)
3. Nếu có tool call → check input data: OHLCV có đủ datapoints?
4. So sánh output với pandas-ta:
   ```python
   import pandas_ta as ta
   df.ta.rsi(length=14)
   ```

### Fix
- **Prompt issue:** Reinforced "KHÔNG BAO GIỜ tự tính" trong system prompt
- **Data thiếu:** Thêm validation: if len(data) < window_size → trả warning
- **Tool bug:** Fix tool code, thêm unit test

---

## Symptom 2: Model trả lời "tôi không biết" khi data có sẵn

### Possible Causes
1. Intent classification sai → không gọi đúng tool
2. Context compression cắt mất data quan trọng
3. Ticker chuẩn hóa sai (lowercase, ký tự thừa)

### Debug Steps
1. Check intent classification trong log
2. Check context size trước/sau compression
3. Check ticker normalization: input vs processed
   ```bash
   grep "ticker.*normalized" logs/app.log
   ```

### Fix
- **Intent sai:** Thêm examples cho edge cases trong prompt
- **Compression cắt mất:** Tăng ngưỡng auto-compression
- **Ticker sai:** Fix normalization logic

---

## Symptom 3: Sentiment analysis sai hoặc thiên lệch

### Possible Causes
1. Retrieval sai — web_search trả bài không liên quan
2. Prompt scoring thiên lệch
3. Nguồn tin bias (VD: chỉ có tin tích cực từ 1 nguồn)

### Debug Steps
1. Check web_search results: query gì? trả bài nào?
   ```bash
   grep "web_search" logs/app.log | tail -10
   ```
2. Check web_reader output: nội dung extract có đúng không?
3. Check LLM scoring: sentiment + evidence có match không?
4. Check source diversity: bao nhiêu nguồn khác nhau?

### Fix
- **Retrieval sai:** Improve search query (thêm "chứng khoán" / ticker keyword)
- **Prompt bias:** Thêm instruction "Nếu mixed → NEUTRAL"
- **Source bias:** Thêm domain diversity requirement

---

## Symptom 4: Swarm quá chậm (> 30s)

### Possible Causes
1. LLM provider latency cao
2. Một agent bị block (data source timeout)
3. Mailbox congestion

### Debug Steps
1. Check timing per agent:
   ```bash
   grep "agent.*completed" logs/app.log | tail -20
   ```
2. Identify bottleneck: agent nào chậm nhất?
3. Check data source health: `/health` endpoint

### Fix
- **LLM chậm:** Switch model hoặc provider
- **Agent bị block:** Thêm timeout per agent, skip nếu quá lâu
- **Mailbox issue:** Check queue size, increase workers

---

## Symptom 5: Compliance Gate reject rate cao (> 5%)

### Possible Causes
1. Agents không attach evidence vào output
2. Disclaimer template bị xóa/thay đổi trong prompt
3. Compression cắt mất citations

### Debug Steps
1. Check compliance logs:
   ```bash
   grep "gate_result.*fail" logs/compliance.log | tail -20
   ```
2. Check rejection reason: missing_disclaimer? missing_citation? uncited_claim?
3. Review agent output trước khi qua gate

### Fix
- **Missing evidence:** Reinforce citation rule trong agent prompts
- **Missing disclaimer:** Check Portfolio Manager prompt — disclaimer section
- **Compression issue:** Mark citations as non-compressible

---

## Symptom 6: PDF upload analysis trả kết quả rỗng

### Possible Causes
1. PDF encrypted hoặc corrupt
2. Scanned PDF + OCR fail
3. PDF quá lớn (> 20MB)

### Debug Steps
1. Check doc_reader log:
   ```bash
   grep "doc_reader" logs/app.log | tail -10
   ```
2. Test PDF manually:
   ```python
   import pdfplumber
   with pdfplumber.open("test.pdf") as pdf:
       print(pdf.pages[0].extract_text())
   ```
3. Check file size và format

### Fix
- **Encrypted:** Thông báo user unlock PDF trước khi upload
- **OCR fail:** Improve OCR quality (higher DPI, preprocessing)
- **Quá lớn:** Trả error 400 với message rõ ràng
