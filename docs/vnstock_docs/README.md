---
title: VNStock 3.4.0 - Tài Liệu Hướng Dẫn
tags:
- vnstock
- documentation
aliases:
- README
---

# VNStock 3.4.0 - Tài Liệu Hướng Dẫn

## 🎯 Giới Thiệu

**VNStock** là thư viện Python để lấy dữ liệu chứng khoán Việt Nam từ nhiều nguồn uy tín. Thiết kế với kiến trúc provider-based, cho phép chuyển đổi linh hoạt giữa các nguồn dữ liệu khác nhau.

### ✨ Tính Năng Chính

- ✅ **Nhiều nguồn dữ liệu**: VCI, KBS, MSN (API công khai); FMP, DNSE (API chính thức)
- ⚠️ **TCBS**: Ngưng cập nhật thêm từ v3.4.0, sẽ loại bỏ trong v3.5.0 (tháng 3/2026)
- ✅ **API thống nhất**: Cùng interface cho tất cả nguồn
- ✅ **Dữ liệu lịch sử & Real-time**: Giá, công ty, tài chính
- ✅ **Dữ liệu công ty**: Hồ sơ, cổ đông, nhân viên quản lý
- ✅ **Dữ liệu tài chính**: Báo cáo, chỉ số, lưu chuyển tiền tệ
- ✅ **Lọc & Phân loại**: Theo ngành, sàn giao dịch, chỉ số

## 📚 Hướng Dẫn Sử Dụng

| Tài Liệu | Nội Dung | Mức Độ |
|---------|---------|--------|
| **[[01-overview]]** | Tổng quan kiến trúc, các loại dữ liệu | Cơ bản |
| **[[02-installation]]** | Cài đặt, thiết lập, kiểm tra | Cơ bản |
| **[[03-listing-api|03-Listing API]]** | API tìm kiếm và lọc chứng khoán | Cơ bản |
| **[[04-company-api|04-Company API]]** | Thông tin công ty, cổ đông, nhân viên quản lý | Cơ bản |
| **[[05-trading-api|05-Trading API]]** | Dữ liệu giao dịch, bid/ask, thống kê | Cơ bản |
| **[[06-quote-price-api|06-Quote & Price]]** | API lấy giá lịch sử và real-time | Cơ bản |
| **[[07-financial-api|07-Financial API]]** | API dữ liệu tài chính và báo cáo | Trung cấp |
| **[[08-fund-api|08-Fund API]]** | Dữ liệu quỹ đầu tư mở (Fmarket) | Trung cấp |
| **[[09-screener-api|09-Screener API]]** | Công cụ lọc chứng khoán nâng cao | Nâng cao |
| **[[10-connector-guide|10-Connector Guide]]** | Hướng dẫn API bên ngoài (FMP, XNO, DNSE) | Nâng cao |
| **[[11-best-practices|11-Best Practices]]** | Mẹo tối ưu hóa, xử lý lỗi, security | Nâng cao |

## 🚀 Bắt Đầu Nhanh

### Cài Đặt

```bash
pip install vnstock
```

Xem chi tiết tại **[[02-installation]]**

## 📖 Cấu Trúc Tài Liệu

Tài liệu được chia thành 11 phần theo thứ tự từ cơ bản đến nâng cao:

1. **[[01-overview]]** - Hiểu kiến trúc và các loại dữ liệu
2. **[[02-installation]]** - Cài đặt và kiểm tra môi trường
3. **[[03-listing-api|03-Listing API]]** - Tìm kiếm danh sách chứng khoán
4. **[[04-company-api|04-Company API]]** - Lấy thông tin công ty chi tiết
5. **[[05-trading-api|05-Trading API]]** - Dữ liệu giao dịch thị trường
6. **[[06-quote-price-api|06-Quote & Price]]** - Lấy dữ liệu giá
7. **[[07-financial-api|07-Financial API]]** - Truy cập dữ liệu tài chính
8. **[[08-fund-api|08-Fund API]]** - Thông tin quỹ đầu tư mở
9. **[[09-screener-api|09-Screener API]]** - Lọc chứng khoán nâng cao
10. **[[10-connector-guide|10-Connector Guide]]** - Sử dụng API bên ngoài
11. **[[11-best-practices|11-Best Practices]]** - Tối ưu hóa và xử lý lỗi

## Kiến Trúc Hệ Thống

VNStock sử dụng kiến trúc provider-based cho phép chuyển đổi linh hoạt giữa các nguồn dữ liệu:

```
Ứng Dụng
   ↓
API Thống Nhất (Quote, Listing, Finance, Company)
   ↓
Adapter Layer (Chuẩn hóa dữ liệu)
   ↓
Các Nguồn Dữ Liệu (Web Scraping & API bên ngoài)
```

## 📊 Nguồn Dữ Liệu

### Web Scraping

| Nguồn | Danh Sách | Giá | Công Ty | Tài Chính | Trạng Thái |
|-------|----------|-----|--------|----------|-----------|
| **VCI** | ✅ | ✅ | ✅ | ✅ | Hoạt động |
| **KBS** | ✅ | ✅ | ✅ | ✅ | Mới (v3.4.0) |
| **MSN** | ✅ | ✅ | ❌ | ❌ | Hoạt động |

### API Bên Ngoài

| API | Giá | Tài Chính | Công Ty |
|-----|-----|----------|---------|
| **FMP** | ✅ | ✅ | ✅ |
| **XNO** | ✅ | ✅ | ✅ |
| **DNSE** | ✅ | ❌ | ❌ |

## 🎓 Lộ Trình Học Tập

Khuyến nghị làm theo thứ tự từ trên xuống để hiểu toàn bộ hệ thống:

1. **[[01-overview]]** - Nắm vững kiến trúc và các khái niệm cơ bản
2. **[[02-installation]]** - Cài đặt và xác nhận môi trường hoạt động
3. **[[03-listing-api|03-Listing API]]** - Tìm kiếm chứng khoán theo tiêu chí
4. **[[03a-company-api|03a-Company API]]** - Tìm hiểu chi tiết về công ty
5. **[[03b-trading-api|03b-Trading API]]** - Phân tích dữ liệu giao dịch
6. **[[04-quote-price-api|04-Quote & Price]]** - Truy cập dữ liệu giá chứng khoán
7. **[[05-financial-api|05-Financial API]]** - Lấy dữ liệu tài chính chi tiết
8. **[[05a-fund-api|05a-Fund API]]** - Khám phá quỹ đầu tư mở
9. **[[06-connector-guide|06-Connector Guide]]** - Sử dụng API bên ngoài (FMP, XNO, DNSE)
10. **[[06a-screener-api|06a-Screener API]]** - Lọc chứng khoán theo tiêu chí nâng cao
11. **[[07-best-practices|07-Best Practices]]** - Áp dụng tối ưu hóa, xử lý lỗi, security

## 🔗 Liên Kết Hữu Ích

- **[GitHub](https://github.com/thinh-vu/vnstock)** - Mã nguồn và issue tracking
- **[PyPI](https://pypi.org/project/vnstock)** - Cài đặt package
- **[Website](https://vnstocks.com)** - Trang chính thức

## ℹ️ Thông Tin Phiên Bản

- **Phiên bản**: 3.4.0
- **Cập nhật lần cuối**: 2024-12-17
- **Trạng thái**: Đang bảo trì ✅
- **Thông báo**: TCBS đã ngưng được cập nhật, sẽ loại bỏ trong v3.5.0 (tháng 3/2026)
- **License**: MIT
