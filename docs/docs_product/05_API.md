# API Documentation — Vietstock Agent

> Version: 10.0 | Status: Draft | Updated: 2026-04-25

---

## Endpoint: `/chat`

### Method
`POST`

### Description
Gửi câu hỏi tài chính bằng ngôn ngữ tự nhiên. Server trả kết quả qua SSE stream.

### Request
```json
{
  "query": "string (required) — Câu hỏi NL tiếng Việt",
  "session_id": "string (optional) — ID session để giữ context",
  "ticker": "string | string[] (optional) — Ticker(s) cụ thể, nếu biết trước"
}
```

### Response (SSE Stream)
Mỗi event theo format Server-Sent Events:
```
event: chunk
data: {"type": "chunk", "content": "Phân tích VCB cho thấy..."}

event: chunk
data: {"type": "chunk", "content": "ROE đạt 23.5%..."}

event: done
data: {"type": "done", "metadata": {"tokens_used": 1234, "agents_used": ["technical", "fundamental"], "citations": 3}}
```

### Response fields

| Field           | Type   | Description                                  |
| --------------- | ------ | -------------------------------------------- |
| `type`          | string | `chunk` (partial) / `done` (complete) / `error` |
| `content`       | string | Markdown text (trong `chunk` events)         |
| `metadata`      | object | Chỉ trong `done` event                       |
| `metadata.tokens_used` | int | Tổng token đã dùng                    |
| `metadata.agents_used` | array | Danh sách agent đã chạy              |
| `metadata.citations`   | int | Số citation trong response             |

### Error
```json
{"type": "error", "code": 400, "message": "Query không được để trống"}
{"type": "error", "code": 422, "message": "Ticker không hợp lệ: XYZ123"}
{"type": "error", "code": 500, "message": "Lỗi hệ thống, vui lòng thử lại"}
{"type": "error", "code": 503, "message": "Nguồn dữ liệu tạm thời không khả dụng"}
```

| Code | Description                                |
| ---- | ------------------------------------------ |
| 400  | Bad request (query rỗng, format sai)       |
| 422  | Unprocessable (ticker invalid, params sai) |
| 500  | Internal server error                      |
| 503  | Data source unavailable                    |

### Example
```bash
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"query": "RSI 14 ngày của HPG hiện tại là bao nhiêu?"}'
```

---

## Endpoint: `/upload`

### Method
`POST` (multipart/form-data)

### Description
Upload báo cáo tài chính (PDF) để agent phân tích.

### Request
```
Content-Type: multipart/form-data

Fields:
  - file: binary (PDF, max 20MB)
  - ticker: string (optional) — Mã chứng khoán liên quan
  - query: string (optional) — Câu hỏi cụ thể về file
```

### Response (SSE Stream)
Tương tự `/chat` — trả phân tích qua SSE stream.

### Error

| Code | Description                            |
| ---- | -------------------------------------- |
| 400  | File không phải PDF hoặc quá lớn       |
| 422  | PDF không đọc được (corrupt/encrypted) |
| 500  | OCR/processing error                   |

### Example
```bash
curl -N -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@bctc_vnm_2024.pdf" \
  -F "ticker=VNM" \
  -F "query=Đánh giá sức khỏe tài chính"
```

---

## Endpoint: `/health`

### Method
`GET`

### Description
Health check endpoint cho monitoring.

### Response
```json
{
  "status": "ok",
  "version": "10.0.0",
  "data_sources": {
    "vnstock3": "ok",
    "yfinance": "ok",
    "vector_store": "ok"
  }
}
```

---

## Authentication

- **v10:** API key via `Authorization: Bearer <key>` header
- **Future:** OAuth 2.0

## Rate Limiting

- 60 requests/minute per API key (v10)
- Swarm queries (investment advice) count as 1 request
