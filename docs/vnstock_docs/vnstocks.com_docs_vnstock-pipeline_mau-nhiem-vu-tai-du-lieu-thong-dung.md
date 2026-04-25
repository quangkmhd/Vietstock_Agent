---
url: "https://vnstocks.com/docs/vnstock-pipeline/mau-nhiem-vu-tai-du-lieu-thong-dung"
title: "Mẫu Tải Dữ Liệu Thông Dụng | Vnstock"
---

Toggle Sidebar

### Mục lục

## 📚 Giới thiệu

Trang này cung cấp các mẫu code **sẵn sàng sử dụng** (plug-and-play) cho các tác vụ thường gặp khi làm việc với dữ liệu thị trường chứng khoán Việt Nam.

Mẹo

**💡 Hai Chế độ Sử dụng:**

- **🚀 Chế độ Đơn giản** \- Tải về, chạy ngay lập tức, không cần chỉnh sửa. Lý tưởng cho người mới hoặc cần kết quả nhanh.
- **⚙️ Chế độ Tùy chỉnh** \- Tuần tự toàn bộ tham số (nhóm mã, khoảng thời gian, chu kỳ, v.v.). Phù hợp cho phân tích chi tiết hoặc tích hợp vào pipeline.

Hướng dẫn Nhanh

1. Nhấn **Xem Code** để xem nội dung script
2. Nhấn **Tải về** để download file Python (.py)
3. Chạy: `python filename.py`
4. Dữ liệu sẽ lưu trong thư mục: `./data/[loại_dữ_liệu]/`

* * *

## OHLCV

Tải dữ liệu giá cổ phiếu theo chu kỳ (ngày, giờ, phút). Dữ liệu bao gồm giá mở, cao, thấp, đóng, và khối lượng giao dịch.

**Dùng cho:** Phân tích kỹ thuật, backtest strategy, khảo sát xu hướng giá lịch sử.

### Đơn giản - OHLCV

ohlcv\_simple\_pipeline.py25 lines • 1.1 KB

Xem CodeTải về

Kết quả

CSV files lưu trong `./data/ohlcv/` với cấu trúc: `[ticker]_[interval].csv`

### Tùy chỉnh - OHLCV

ohlcv\_custom\_pipeline.py70 lines • 2.2 KB

Xem CodeTải về

Kết quả

CSV files lưu trong `./data/ohlcv/` với cấu trúc: `[ticker]_[interval].csv`

* * *

## Khớp Lệnh (Intraday)

Dữ liệu giao dịch thực tế xảy ra trong phiên giao dịch: từng lệnh khớp, thời gian, giá, khối lượng.

**Dùng cho:** Phân tích dòng tiền, theo dõi khối lượng giao dịch lớn, phát hiện bất thường trong giao dịch.

### Đơn giản - Intraday

Pipeline đơn giản lưu trữ dữ liệu khớp lệnh bằng cách nối dữ liệu liên tục trong phiên hoặc tải một lần vào cuối ngày với định dạng CSV.

intraday\_simple\_pipeline.py47 lines • 1.8 KB

Xem CodeTải về

Kết quả

CSV files lưu trong `./data/intraday/`.

### Tùy chỉnh - Intraday

Pipeline lưu trữ dữ liệu khớp lệnh cuối ngày bằng định dạng Parquet giúp tối ưu dung lượng lưu trữ và cho phép đọc ghi dữ liệu nhanh hơn CSV.

intraday\_custom\_pipeline.py175 lines • 5.9 KB

Xem CodeTải về

* * *

## Bảng Giá

Snapshot giá của tất cả mã hoặc một nhóm mã cụ thể. Mỗi lần chạy sẽ lấy giá hiện tại nhất.

**Dùng cho:** Tạo bảng giá, theo dõi biến động realtime, so sánh giá giữa các mã.

### Đơn giản - Price Board

price\_board\_simple\_pipeline.py24 lines • 1.1 KB

Xem CodeTải về

Kết quả

File CSV lưu trong `./data/price_board/`.

* * *

## Dư Mua/Dư Bán

**Dữ liệu thống kê Dư mua - Dư bán:** Khối lượng dư mua (BID) và dư bán (ASK) theo từng mức giá trong order book.

**Dùng cho:** Phát hiện các hành vi đặt giá ảo, phân tích sâu độ thanh khoảng, theo dõi sự chuyển động tiền mặt.

### Đơn giản - Price Depth

price\_depth\_simple\_pipeline.py69 lines • 2.5 KB

Xem CodeTải về

Kết quả

CSV files lưu trong `./data/price_depth/YYYY-MM-DD/`. Mỗi file chứa thông tin BID/ASK depth cho một mã.

### Tùy chỉnh - Price Depth

price\_depth\_custom\_pipeline.py281 lines • 10.3 KB

Xem CodeTải về

Kết quả

**Intraday mode:** CSV files lưu trong `./data/price_depth/YYYY-MM-DD/` với dữ liệu append liên tục.

**EOD mode:** CSV files lưu trong `./data/price_depth/YYYY-MM-DD/` với snapshot cuối ngày.

* * *

## Báo Cáo Tài Chính

Tải báo cáo tài chính: Bảng cân đối kế toán (BCĐKT), Kết quả kinh doanh (KQKD), Lưu chuyển tiền tệ (LCTT). Dữ liệu hàng năm hoặc quý.

**Dùng cho:** Phân tích cơ bản (fundamental analysis), so sánh tài chính giữa các công ty, tính toán các chỉ số tài chính.

### Đơn giản - Financial

financial\_simple\_pipeline.py41 lines • 1.5 KB

Xem CodeTải về

Kết quả

CSV files lưu trong `./data/financial/`. Bao gồm báo cáo hàng năm hoặc quý theo cấu hình.

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập