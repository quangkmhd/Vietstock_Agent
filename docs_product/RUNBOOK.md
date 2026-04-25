# Runbook — Vietstock Agent

> Version: 10.0 | Status: Draft | Updated: 2026-04-25

---

## System Overview

Vietstock Agent là hệ thống multi-agent financial advisor gồm:
- **FastAPI Gateway:** Tiếp nhận request, SSE streaming
- **AgentLoop:** ReAct reasoning engine
- **SwarmRuntime:** Orchestrate 4 specialized agents song song
- **Data sources:** vnstock3, yfinance, DuckDuckGo, Jina Reader, Vector Store

---

## How to Run

### Prerequisites
```bash
# Python 3.11+
python --version

# uv package manager
uv --version
```

### Start service
```bash
# Install dependencies
uv pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env: LLM_API_KEY, VECTOR_STORE_URL, etc.

# Run development server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Environment variables

| Variable          | Required | Description                       | Example                     |
| ----------------- | -------- | --------------------------------- | --------------------------- |
| `LLM_API_KEY`     | Yes      | API key cho LLM provider          | `sk-...`                    |
| `LLM_MODEL`       | Yes      | Model name                        | `gpt-4o`                    |
| `VECTOR_STORE_URL`| No       | Connection string vector DB       | `postgresql://...`          |
| `CACHE_TTL`       | No       | Default cache TTL (seconds)       | `86400`                     |
| `LOG_LEVEL`       | No       | Logging level                     | `INFO`                      |
| `API_KEY`         | Yes      | API key cho authentication        | `vsa-...`                   |

---

## Common Issues

### Issue 1: API timeout (> 30s)

**Nguyên nhân:**
- LLM provider chậm hoặc rate limited
- Swarm chạy quá nhiều agent song song
- Data source (vnstock3/yfinance) timeout

**Cách fix:**
1. Check LLM provider status page
2. Check logs: `grep "timeout" logs/app.log`
3. Giảm swarm concurrency nếu cần
4. Kiểm tra data source health: `curl localhost:8000/health`

### Issue 2: vnstock3 trả về lỗi / empty data

**Nguyên nhân:**
- vnstock3 upstream API thay đổi
- Ticker không tồn tại hoặc đã hủy niêm yết
- Rate limiting

**Cách fix:**
1. Check vnstock3 version: `uv pip show vnstock3`
2. Test trực tiếp: `python -c "from vnstock3 import Vnstock; print(Vnstock().stock('VCB').quote.history())"`
3. Update vnstock3: `uv pip install --upgrade vnstock3`
4. Nếu vẫn lỗi → system tự fallback yfinance (check logs)

### Issue 3: LLM hallucination / output thiếu citation

**Nguyên nhân:**
- Prompt bị drift sau update
- Context quá dài → compression cắt mất evidence
- Model mới chưa test

**Cách fix:**
1. Check Compliance Gate logs: `grep "gate_result.*fail" logs/compliance.log`
2. Review prompt version trong `PROMPTS.md`
3. Chạy evaluation test: xem `EVALUATION.md`
4. Rollback prompt nếu cần

### Issue 4: Web search/reader bị block (403/429)

**Nguyên nhân:**
- Website target block IP/user-agent
- Rate limiting

**Cách fix:**
1. Check error logs: `grep "403\|429" logs/app.log`
2. Hệ thống tự skip URL lỗi, dùng URLs còn lại
3. Nếu tất cả nguồn bị block → sentiment analysis sẽ trả "không đủ dữ liệu"
4. Cân nhắc thêm delay giữa requests

### Issue 5: Vector Store / RAG trả kết quả không liên quan

**Nguyên nhân:**
- Index stale (chưa re-index báo cáo mới)
- Chunking strategy không phù hợp
- Embedding model quality thấp

**Cách fix:**
1. Check index date: `SELECT MAX(updated_at) FROM documents;`
2. Re-index: `uv run python scripts/reindex.py`
3. Review chunk size / overlap settings

---

## Monitoring

### Log location
- Application log: `logs/app.log`
- Compliance log: `logs/compliance.log`
- Access log: stdout (uvicorn)

### Dashboard
- Health check: `GET /health`
- Metrics: Prometheus endpoint (v20+)
- Grafana dashboard (v20+)

### Key metrics to watch

| Metric              | Normal Range     | Alert If               |
| -------------------- | --------------- | ---------------------- |
| API latency p95      | < 30s           | > 30s                  |
| Error rate           | < 5%            | > 5%                   |
| Compliance pass rate | > 95%           | < 95%                  |
| Cache hit ratio      | > 50%           | < 30%                  |
| Token usage/query    | < budget        | > 2x budget            |

---

## Emergency

### Rollback
```bash
# Rollback to previous version
git checkout <previous-tag>
uv pip install -r requirements.txt
# Restart service
sudo systemctl restart vietstock-agent
```

### Disable feature
```bash
# Disable swarm (fallback to single-agent for all queries)
export SWARM_ENABLED=false
sudo systemctl restart vietstock-agent

# Disable specific data source
export VNSTOCK3_ENABLED=false  # force yfinance only
sudo systemctl restart vietstock-agent
```

### Emergency contacts
- System owner: quangnhvn34
- LLM provider support: (theo provider)
