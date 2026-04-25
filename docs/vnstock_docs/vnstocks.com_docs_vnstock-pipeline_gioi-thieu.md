---
url: "https://vnstocks.com/docs/vnstock-pipeline/gioi-thieu"
title: "Giới thiệu Vnstock Pipeline | Vnstock"
---

## Mục lục

Thành công

**Vnstock Pipeline** là một thư viện Python được thiết kế như một chương trình quản lý dữ liệu tự động hiện đại (data pipeline) – giúp bạn tự động hóa toàn bộ quy trình kết nối dữ liệu chứng khoán từ các nguồn dữ liệu công khai một cách tối ưu, nhanh chóng và linh hoạt. Thay vì tải từng phần dữ liệu nhỏ lẻ, Vnstock Pipeline cho phép bạn xây dựng các dòng chảy dữ liệu với khả năng đọc thông tin từ API được tăng tốc tối đa nhờ thuật toán tối ưu, nhanh gấp 10 lần so với cách làm truyền thống.

Bạn có thể dễ dàng sử dụng file Notebook minh họa để chạy lệnh hoặc sao chép các đoạn mã vào chương trình Python của mình. Để sử dụng thư viện, bạn chỉ cần đăng ký tối thiểu [**gói tài trợ Golden**](https://vnstocks.com/insiders-program) và nhận quyền truy cập vào repository riêng tư trên Github để cài đặt.

[Notebook minh hoạ](https://colab.research.google.com/github/vnstock-hq/vnstock_insider_guide/blob/main/demo/4-vnstock_pipeline_demo.ipynb) [Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

## Giới thiệu

Với cách tiếp cận “pipeline”, thư viện giúp bạn:

- **Tự động hóa hoàn toàn** việc truy xuất dữ liệu: định nghĩa nguồn, lịch trình, định dạng đầu ra.

- **Tối ưu hiệu năng tải dữ liệu**: sử dụng kỹ thuật xử lý đa nhiệm, xử lý bất đồng bộ và cache thông minh.

- **Tích hợp liền mạch** vào các quy trình phân tích dữ liệu, mô hình hoá hoặc dashboard của bạn.


Bạn có thể bắt đầu nhanh chóng bằng cách sử dụng các đoạn [code mẫu](https://vnstocks.com/vnstock-insider-api/vnstock-pipeline/mau-nhiem-vu-tai-du-lieu-thong-dung) trong Jupyter Notebook, hoặc xây dựng các Python script để hẹn giờ tải dữ liệu định kỳ.

Để tận dụng toàn bộ tính năng nâng cao của thư viện, bạn cần nắm vững cấu trúc pipeline và linh hoạt mở rộng các tác vụ phù hợp với dự án thực tế của mình.

![Giao diện trang Github của thành viên gói tài trợ Silver](https://vnstocks.com/images/silver_sponsor_github_private_repo.jpg)Giao diện trang Github của thành viên gói tài trợ Silver

### Đặc điểm chính:

- **Kiến trúc module hóa**: Tách biệt các thành phần xử lý dữ liệu thành các module riêng biệt
- **Khả năng mở rộng**: Dễ dàng mở rộng với các nguồn dữ liệu và định dạng xuất mới
- **Xử lý song song**: Tự động xử lý song song cho danh sách tải gồm nhiều mã chứng khoán
- **Xử lý lỗi mạnh mẽ**: Cơ chế thử lại khi gặp lỗi và báo lỗi chi tiết
- **Tùy biến linh hoạt**: Cho phép tùy chỉnh từng thành phần trong chương trình

## Hướng dẫn cài đặt

### Yêu cầu hệ thống

- Python 3.10 trở lên
- Các thư viện phụ thuộc: pandas, numpy, requests, duckdb

### Cài đặt

Sử dụng chương trình cài đặt cung cấp bởi Vnstock cho từng hệ điều hành cụ thể.

## Kiến trúc tổng quan

vnstock\_pipeline được xây dựng dựa trên kiến trúc pipeline với các thành phần chính sau:

### Các thành phần cốt lõi

- **Fetcher**: Lấy dữ liệu thô từ nguồn (API Vnstock)
- **Validator**: Kiểm tra tính toàn vẹn và đầy đủ của dữ liệu
- **Transformer**: Chuyển đổi dữ liệu thô thành định dạng chuẩn, xử lý missing values
- **Exporter**: Xuất dữ liệu đã xử lý ra hệ thống lưu trữ (CSV, Parquet, DuckDB)
- **Scheduler**: Điều phối toàn bộ quy trình xử lý dữ liệu, xử lý lỗi và thử lại

### Luồng xử lý dữ liệu

```
Fetcher → Validator → Transformer → Exporter
                         ↓
                   Scheduler (điều phối)
```

Scheduler điều phối toàn bộ quy trình này:

- Xử lý song song các mã chứng khoán
- Thử lại khi gặp lỗi (với cơ chế backoff)
- Ghi log chi tiết từng bước xử lý
- Xử lý các ngoại lệ và dừng graceful

### Các Exporter Có Sẵn

vnstock\_pipeline cung cấp các exporter linh hoạt để xuất dữ liệu:

- **CSVExport**: Xuất dữ liệu ra file CSV
- **ParquetExport**: Xuất dữ liệu ra file Parquet (tối ưu dung lượng)
- **DuckDBExport**: Xuất dữ liệu vào cơ sở dữ liệu DuckDB
- **TimeSeriesExporter**: Exporter generic cho tất cả loại time-series data (price\_depth, ohlcv, intraday, financial, etc.)

Bạn có thể dễ dàng mở rộng bằng cách tạo custom exporter kế thừa từ `Exporter` base class.

## Bản quyền dữ liệu

Công cụ **Vnstock Pipeline** tối ưu kết nối thông qua các chức năng gốc của **Vnstock Data Explorer**. Tất cả dữ liệu bạn truy cập thông qua Pipeline thuộc sở hữu và chịu sự quản lý của các nguồn dữ liệu gốc. Vnstock không lưu trữ, sao chép, hay tái phân phối bất kỳ dữ liệu nào từ các nguồn gốc đó. Công cụ này chỉ cung cấp khả năng kết nối và truy cập trực tiếp vào dữ liệu từ các nguồn dữ liệu công khai hoặc các nguồn mà người dùng có quyền truy cập.

## Miễn trừ trách nhiệm

Chú ý

Dự án **Vnstock** được xây dựng và cung cấp **chỉ nhằm mục đích nghiên cứu, giáo dục và sử dụng cá nhân.** Dữ liệu thu được thông qua công cụ này có thể tồn tại các giới hạn nhất định như không đầy đủ, không liên tục hoặc có sai lệch so với nguồn dữ liệu chính thức. Do đó, người dùng không được sử dụng công cụ này như cơ sở duy nhất để ra quyết định giao dịch thực tế, phát triển thuật toán đầu tư hoặc bất kỳ quyết định tài chính nào.

**Vnstock và tác giả không chịu trách nhiệm** đối với bất kỳ thiệt hại hay tổn thất nào, bao gồm nhưng không giới hạn bởi mất mát tài chính, tổn thất cơ hội, hoặc các hậu quả phát sinh từ việc sử dụng dữ liệu hoặc mã nguồn được cung cấp.

**Vnstock không cung cấp bất kỳ tư vấn đầu tư hoặc tín hiệu giao dịch nào.** Việc sử dụng dữ liệu và các thông tin liên quan hoàn toàn là trách nhiệm cá nhân của người dùng.

### Thảo luận

Đang tải bình luận...