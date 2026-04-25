---
url: "https://vnstocks.com/docs/du-lieu-tong-hop/co-phieu"
title: "Dữ liệu cổ phiếu | Vnstock"
---

Toggle Sidebar

Lưu ý

Bảng thông tin dưới đây mô tả về độ phủ (coverage) của dữ liệu có thể truy xuất từ Vnstock3. Lưu ý: Vnstock3 hoạt động như một trình duyệt web cho phép kết nối tới các API dữ liệu công khai từ công ty chứng khoán đồng thời tải dữ liệu vào môi trường Python. Dữ liệu từ Vnstock3 phản ánh dữ liệu được cập nhật từ website gốc. Thông tin tần suất cập nhật dựa vào kinh nghiệm quan sát các thay đổi trong đặc tính và cập nhật của dữ liệu.

| Nhóm thông tin | Lớp | Mục | Hàm | Tần suất cập nhật | Nguồn truy xuất |
| --- | --- | --- | --- | --- | --- |
| Danh sách niêm yết | Listing | [Tất cả mã](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#liet-ke-tat-ca-ma-cp) | `all_symbols()` | - | VCI |
|  |  | [Tất cả mã chia theo sàn](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#liet-ke-ma-cp-theo-san) | `symbols_by_exchange()` | - | VCI |
|  |  | [Tất cả mã chia theo nhóm](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#liet-ke-cp-theo-phan-nhom) | `symbols_by_group('VN30')` | - | VCI |
|  |  | [Tất cả mã chia theo ngành](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#cp-theo-nganh-icb) | `symbols_by_industries()` | - | VCI |
|  |  | [Danh sách ngành icb](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#danh-sach-nganh-icb) | `industries_icb()` | - | VCI |
|  |  | [Danh sách mã CK quốc tế](https://vnstocks.com/docs/vnstock/thong-tin-niem-yet#tim-ma-chung-khoan-quoc-te) | `search_symbol_id('USD')` | thời gian thực | MSN |
| Thông tin công ty | Company | [Tổng quan](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#thong-tin-cong-ty) | `overview()` | - | TCBS |
|  |  | [Hồ sơ công ty](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#ho-so-cong-ty) | `profile()` | - | TCBS |
|  |  | [Cổ đông lớn](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#co-dong-lon) | `shareholders()` | - | TCBS |
|  |  | [Lãnh đạo](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#ban-lanh-dao) | `officers()` | - | TCBS |
|  |  | [Công ty con](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#cong-ty-con) | `subsidiaries()` | - | TCBS |
|  |  | [Cổ tức](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#lich-su-chia-co-tuc) | `dividends()` | - | TCBS |
|  |  | [Giao dịch nội bộ](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#giao-dich-noi-bo) | `insider_deals()` | - | TCBS |
|  |  | [Sự kiện](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#su-kien) | `events()` | - | TCBS |
|  |  | [Tin tức](https://vnstocks.com/docs/vnstock/thong-tin-cong-ty#tin-tuc) | `news()` | - | TCBS |
| Báo cáo tài chính | Finance | Báo cáo kết quả kinh doanh | `income_statement()` | Tháng đầu tiên mỗi quý. Chậm so với thông tin công bố trên website UBCK trong 1 tuần. | [VCI](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#bao-cao-ket-qua-kinh-doanh), [TCBS](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#bao-cao-ket-qua-kinh-doanh) |
|  |  | Bảng cân đối kế toán | `balance_sheet()` | Tháng đầu tiên mỗi quý. Chậm so với thông tin công bố trên website UBCK trong 1 tuần. | [VCI](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#bang-can-doi-ke-toan), [TCBS](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#bang-can-doi-ke-toan) |
|  |  | Báo cáo lưu chuyển tiền tệ | `cash_flow()` | Tháng đầu tiên mỗi quý. Chậm so với thông tin công bố trên website UBCK trong 1 tuần. | [VCI](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#bao-cao-luu-chuyen-tien-te), [TCBS](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#bao-cao-luu-chuyen-tien-te) |
|  |  | Chỉ số tài chính | `ratio()` | Tháng đầu tiên mỗi quý. Chậm so với thông tin công bố trên website UBCK trong 1 tuần. | [VCI](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#chi-so-tai-chinh), [TCBS](https://vnstocks.com/docs/vnstock/bao-cao-tai-chinh#chi-so-tai-chinh) |
| Giá chứng khoán | Quote | Giá lịch sử (đồ thị nến) | `history(start='2020-01-01', end='2024-12-31')` | Theo thời gian thực, chi tiết đến cấp độ phút | [VCI](https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su#gia-lich-su), TCBS |
|  |  | Khớp lệnh trong ngày | `intraday(symbol='ACB', show_log=False)` | Thời gian thực theo từng giao dịch xuất hiện, chi tiết đến cấp độ giây | [VCI](https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su#du-lieu-khop-lenh), TCBS |
|  |  | Khối lượng giao dịch theo bước giá. | `price_depth('ACB')` | Theo thời gian thực | VCI, TCBS |
| Thông tin Giao dịch | Trading | Thông tin bảng giá | `price_board(['ACB'])` | Thời gian thực | [VCI](https://vnstocks.com/docs/vnstock/bang-gia-giao-dich), TCBS |

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập