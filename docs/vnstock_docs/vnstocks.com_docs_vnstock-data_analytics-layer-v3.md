---
url: "https://vnstocks.com/docs/vnstock-data/analytics-layer-v3"
title: "Thống kê & Định giá | Vnstock"
---

Toggle Sidebar

### Mục lục

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock-agent-guide/blob/main/notebooks/01_unified_ui/04_Analytics.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Tổng quan

**Analytics Layer** cung cấp dữ liệu **định giá thị trường** bao gồm P/E, P/B lịch sử, và đánh giá tổng quan cho các chỉ số thị trường. Layer được tách riêng từ Insights để tập trung vào phân tích định giá toàn thị trường.

## Khởi tạo

Python

```python
from vnstock_data import Analytics
ana = Analytics()
```

## Cấu trúc Domain

```
Analytics()
└── .valuation(index)
    ├── .pe(duration)         # P/E ratio lịch sử
    ├── .pb(duration)         # P/B ratio lịch sử
    └── .evaluation(duration) # Đánh giá tổng hợp
```

Cập nhật Migration

Nếu bạn từng dùng `Market().pe()` hay `Insights().valuation.pe()`, hãy chuyển sang `Analytics().valuation(index).pe()`. Các phương thức cũ sẽ sớm bị gỡ bỏ.

## Hướng dẫn chi tiết

### 1\. Định giá thị trường

Lấy chuỗi thời gian lịch sử của P/E, P/B cho các chỉ số thị trường — phục vụ backtest và đánh giá chu kỳ định giá.

| Phương thức | Tham số | Mô tả |
| --- | --- | --- |
| `pe()` | `duration` | P/E ratio lịch sử |
| `pb()` | `duration` | P/B ratio lịch sử |
| `evaluation()` | `duration` | Đánh giá tổng hợp (P/E + P/B) |

**Tham số:**

- `index` (str) — Chỉ số: `"VNINDEX"`, `"HNX"`, `"UPCOM"`. Mặc định `"VNINDEX"`.
- `duration` (str) — `"1Y"`, `"2Y"`, `"3Y"`, `"5Y"`. Mặc định `"5Y"`.

Python

```python
from vnstock_data import Analytics

ana = Analytics()

# P/E VNINDEX — 1 năm gần nhất
df_pe_1y = ana.valuation("VNINDEX").pe(duration="1Y")

# P/B HNX — 5 năm
df_pb_5y = ana.valuation("HNX").pb(duration="5Y")

# Đánh giá tổng hợp P/E + P/B
df_eval = ana.valuation("VNINDEX") \
              .evaluation(duration="5Y")
```

**Kết quả mẫu P/E**
Output trả về dạng DataFrame với cột `reportDate` và `pe`. Ví dụ: `2025-03-11  13.22`.

* * *

### 2\. So sánh định giá giữa các sàn

Python

```python
from vnstock_data import Analytics

ana = Analytics()

# So sánh P/E giữa HOSE và HNX
pe_vn = ana.valuation("VNINDEX").pe(duration="1Y")
pe_hnx = ana.valuation("HNX").pe(duration="1Y")

print(f"VNINDEX PE: {pe_vn['pe'].iloc[-1]:.2f}")
print(f"HNX PE: {pe_hnx['pe'].iloc[-1]:.2f}")
```

* * *

### 3\. Đánh giá mức định giá hiện tại

So sánh P/E hiện tại với trung bình 5 năm để xác định thị trường đang rẻ hay đắt.

Python

```python
from vnstock_data import Analytics

ana = Analytics()

# P/E 5 năm để so sánh
pe_5y = ana.valuation("VNINDEX").pe(duration="5Y")

pe_avg = pe_5y['pe'].mean()
pe_current = pe_5y['pe'].iloc[-1]

print(f"P/E hiện tại: {pe_current:.2f}")
print(f"P/E trung bình 5 năm: {pe_avg:.2f}")

if pe_current < pe_avg * 0.9:
    print("Thị trường đang định giá thấp hơn trung bình")
elif pe_current > pe_avg * 1.1:
    print("Thị trường đang định giá cao hơn trung bình")
else:
    print("Thị trường quanh mức định giá trung bình")
```

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập