---
url: "https://vnstocks.com/docs/vnstock-insider-api/lich-su-phien-ban"
title: "Lịch sử phiên bản | Vnstock"
---

## Mục lục

## 23-04-2026 (v3.1.3)

- **Chuẩn hoá & Mở rộng Báo cáo Tài chính (Fundamental & Financial Health)**:
  - Mở rộng Schema tài chính với các trường dữ liệu chi tiết từ nguồn MAS.
  - Định chuẩn hóa bộ tiêu chí đánh giá cho 4 nhóm ngành: Ngân hàng, Chứng khoán, Bảo hiểm và Đa ngành theo tiêu chuẩn phân tích chung tương tự giao diện tại TCBS.
- **Hạ tầng & Tối ưu hóa (Infrastructure & Refactoring)**:
  - Nâng cấp các module tiện ích lõi (`client.py`, `user_agent.py`) để cải thiện hiệu năng kết nối và quản lý User-Agent.
- **Sửa lỗi & Ổn định hệ thống (Bug Fixes)**:
  - Khắc phục triệt để lỗi sai tỷ lệ giá (price scaling) cho các tài sản Chỉ số (Index) và Phái sinh (Derivative) tại module `quote` (nguồn KBS).
  - Sửa lỗi truy xuất dữ liệu danh sách niêm yết (listing) và báo giá (quote) cho nguồn Dukascopy.
  - Xử lý các lỗi nhỏ trong UI Registry và logic phân loại ngành giúp hệ thống hoạt động chính xác hơn.
- **Chuyển đổi giao thức dữ liệu VCI (API Migration)**:
  - Chuyển đổi toàn bộ quy trình lấy danh sách (Listing) và mã ngành (ICB) từ nguồn VCI từ GraphQL sang REST API để tăng độ ổn định và tốc độ phản hồi.

## 12-04-2026

> Phần mềm `vnstock_data` cập nhật phiên bản 3.1.0: Hoàn thiện bộ dữ liệu hợp nhất (Unified UI) và bổ sung bổ sung dữ liệu thị trường Quốc tế.

- **Thị trường Quốc tế & Crypto**:

  - Tích hợp dữ liệu tiền mã hoá (Cryptocurrency) thông qua API Binance Spot (hỗ trợ dữ liệu `ohlcv`, `order_book`, `intraday`, `quote`). Khung kiến trúc được trang bị thuật toán chờ và gửi lại để duy trì kết nối khi gặp giới hạn truy vấn API.
  - Xây dựng kiến trúc Explorer cung cấp biểu đồ đa khung thời gian cho Ngoại hối (Forex), Hàng hoá (Commodity) và các chỉ số toàn cầu thông qua Dukascopy và ForexSB. Cung cấp bộ cấu hình Múi giờ gốc sang múi giờ Hệ thống (`Asia/Ho_Chi_Minh`).
- **Thị trường Nội địa (Unified UI)**:

  - Nâng cấp API cho thị trường chỉ số (Index Market): Hệ thống hỗ trợ lấy bộ dữ liệu thống kê giao dịch lịch sử của tất cả các loại chỉ số thông qua phương thức `trade_history()`. Hỗ trợ tên chỉ số quy chuẩn để tra lệnh.
  - Bổ sung hàm tóm tắt bức tranh tài chính tổng hợp `financial_health` (tổ hợp 3 bảng báo cáo tài chính và các chỉ số tài chính). Chuẩn hoá chuyển ngữ thẻ Scorecard chuyên ngành: Ngân hàng, Chứng khoán, Bảo hiểm, hỗ trợ trích lọc linh hoạt. Quy chuẩn này lấy cảm hứng từ cấu trúc báo cáo của nền tảng TCBS, giúp duy trì sự nhất quán trong bộ tiêu chí cố định trong phân tích cơ bản cho doanh nghiệp, tránh phải xử lý bộ tiêu chí không thống nhất trong các báo cáo tài chính vốn có nhiều khác biệt giữa các nguồn khác nhau. Sử dụng bộ tiêu chí này giúp người dùng hạn chế phải thay đổi code khi nguồn dữ liệu gặp sự cố hoặc phiên bản phần mềm thay đổi ảnh hưởng tới bộ tiêu chí này.
    -Nguồn dữ liệu cung cấp dữ liệu tài chính cho các hàm tại Unified UI được chuyển đổi từ KBS sang MAS để tăng số kỳ báo cáo tài chính lên trên 10 năm, thay vì bị giới hạn 4 kỳ mặc định của API từ KBS.
  - Tối ưu tra cứu dữ liệu Vĩ mô (Macro) và Hàng hoá: Áp dụng kỹ thuật quét lùi tự động và đắp điền dữ liệu khuyết rỗng (Forward-fill) để xử lý hoàn thiện độ trễ công bố thông tin, giảm thiểu phát sinh lỗi.
  - Cải thiện khả năng chuẩn hoá symbol nhập nhập vào hàm của CafeF để nhận diện các chỉ số chính xác VNINDEX/HOSE, HNXINDEX/HNX, UPCOMINDEX/UPCOM và VN30.
  - Tái cấu trúc chuẩn thư viện: Áp dụng chuẩn hoá, bổ sung tham số định danh nhà cung cấp `source` theo yêu cầu từ phiên bản.
- **Tài liệu Agent Guide**:

  - Cập nhật mô tả các hàm và nguồn dữ liệu bổ sung
  - Cung cấp schema dữ liệu chuẩn hoá giúp xác định mô hình dữ liệu và xây dựng sản phẩm tin cậy hơn, giảm thiểu việc phải chạy từng đoạn code để kiểm tra cấu trúc dữ liệu.
- **Bổ sung bộ Notebook hoàn chỉnh**:

  - Bổ sung bộ Notebook hoàn chỉnh về các hàm tại Unified UI và theo kiểu gọi Adapter Pattern (thay đổi tham số source kiểu cũ) phản ánh đầy đủ trạng thái mới nhất của thư viện.

## 07-04-2026

> Phát hành `vnstock_data` phiên bản 3.0.1 sửa các lỗi quan trọng và tinh chỉnh trải nghiệm người dùng.

- **Unified UI**: Bổ sung hàm `cash_flow` vào giao diện hợp nhất; cập nhật mô tả cho hàm `trade_history` (thống kê giao dịch, giá chứng khoán trước khi pha loãng).
- **Nguồn KBS**: Sửa lỗi chia điểm index cho 1000 và lỗi 502 Bad Gateway do web phân định lại cấu trúc URL; tinh chỉnh chuẩn hoá tên chỉ tiêu tài chính và thông tin định danh User Agent.
- **Nguồn MBK (Vĩ mô)**: Cải thiện thuật toán truy xuất dữ liệu theo tham số `length` và tự động _forward fill_ để khắc phục lỗi trả về dữ liệu rỗng.
- **Nguồn SPL (Hàng hoá)**: Sửa lỗi truy xuất dữ liệu null sinh ra do không khớp cấu hình múi giờ.
- **Nguồn VCI**: Bổ sung cơ chế tương thích pandas cho hàm map và applymap để hoạt động tốt cho tất cả phiên bản từ 2.1.0 và trước đó.

## 03-04-2026

> **Phát hành vnstock\_news 2.2.0: Công cụ truy xuất dữ liệu tin tức hiệu suất cao**
>
> Bản phát hành mới giải phóng bạn khỏi những lỗi xảy ra trong quá trình xử lý dữ liệu, mang tới sự ổn định khi trích xuất dữ liệu tin tức từ 21 trang tin nổi bật tại Việt Nam.

### ✨ Nâng cấp nổi bật

- **Kiến trúc Crawler Hợp Nhất (Unified Crawler):** Khai thác song song và tự động dự phòng chéo (fallback) giữa luồng RSS và Sitemap, đảm bảo hệ thống bạn luôn có tin mới khi một trong hai luồng gặp sự cố.
- **Trích xuất metadata linh hoạt:** Tăng cường khả năng bắt chính xác Selector qua các thuộc tính linh hoạt (`id`, `data-slot`, `rel`) thay vì phụ thuộc mỗi thẻ `class` theo CSS Selector truyền thống. Chủ động trích xuất thêm thẻ Tags, Lượt xem và Chuyên mục của bài.
- **Làm sạch tự động & Xử lý thời gian:**
  - **Date Parser:** Tự động "thấu hiểu" và ép kiểu mọi định dạng thời gian lạ lẻ (như _15 phút trước_, _Thứ năm..._) về chuẩn ISO thống nhất cho Database.
  - **Spam/Media Link Filter:** Rà soát và loại bỏ link nhiễu phân trang, hình ảnh, URL rác đính kèm trong RSS.
  - Tự động bỏ qua lỗi chứng chỉ SSL để duy trì kết nối cho những tòa soạn chưa nâng cấp máy chủ hiện đại.

### 🐛 Vận hành trơn tru hơn

- Sửa dứt điểm tình trạng trả về Data nhưng cột Nội dung trống rỗng (Missing Content 100%) gây ra bởi lỗi đọc JSON.
- **Bổ sung đầu báo mới được hỗ trợ:** Bổ sung và tinh chỉnh cấu trúc CSS cho hàng loạt trang báo mới (Tiền Phong, Người Lao Động, Thanh Niên, Znews, Dân Trí, Đầu Tư, VnEconomy).
- Bổ sung bộ kịch bản dùng thử "All-in-one" và tái cấu trúc tài liệu ví dụ, tự động dọn dẹp kết quả xuất file vào phân vùng tĩnh `/output/`.

**Nhấp để xem danh sách 21 trang báo được hỗ trợ sẵn**

| STT | Tên Báo | Tên Config | Loại Hình | RSS | Sitemap |
| --- | --- | --- | --- | --- | --- |
| 1 | **Nhân Dân** | nhandan | Cơ quan TW | ✅ | ✅ |
| 2 | **Tiền Phong** | tienphong | Cơ quan TW | ✅ | ✅ |
| 3 | **VietNamNet** | vietnamnet | Bộ Ngành | ✅ | ✅ |
| 4 | **Dân Trí** | dantri | Bộ Ngành | ✅ | ✅ |
| 5 | **VnExpress** | vnexpress | Bộ Ngành | ✅ | ✅ |
| 6 | **Báo Đầu Tư** | baodautu | Bộ Ngành | ✅ | ✅ |
| 7 | **Thời Báo Tài Chính** | thoibaotaichinhvietnam | Bộ Ngành | ✅ | ✅ |
| 8 | **Thanh Niên** | thanhnien | Tổ chức TW | ✅ | ✅ |
| 9 | **Tuổi Trẻ** | tuoitre | Địa phương | ✅ | ✅ |
| 10 | **Người Lao Động** | nld | Địa phương | ✅ | ✅ |
| 11 | **Pháp Luật TP.HCM** | plo | Địa phương | ✅ | ✅ |
| 12 | **Kinh Tế Sài Gòn** | ktsg | Địa phương | ✅ | ✅ |
| 13 | **VnEconomy** | vneconomy | Chuyên ngành | ✅ | ✅ |
| 14 | **Diễn Đàn Doanh Nghiệp** | dddn | Chuyên ngành | ✅ | ✅ |
| 15 | **PetroTimes** | petrotimes | Chuyên ngành | ✅ | ✅ |
| 16 | **Znews (Tri thức)** | znews | Chuyên ngành | ✅ | ✅ |
| 17 | **CafeF** | cafef | Trang tin | ✅ | ✅ |
| 18 | **CafeBiz** | cafebiz | Trang tin | ✅ | ✅ |
| 19 | **VietStock** | vietstock | Trang tin | ✅ | ✅ |
| 20 | **24h** | 24h | Tổng hợp | ✅ | ✅ |
| 21 | **Người Quan Sát** | nguoiquansat | Tổng hợp | ✅ | ✅ |

## 11-03-2026

> **Phát hành vnstock\_data 3.0.0: Thế hệ mới với Unified UI và Thị trường Quốc tế.**
>
> Phiên bản 3.0.0 không chỉ là một bản cập nhật thông thường, mà là bước chuyển mình quan trọng của hệ sinh thái Vnstock. Chúng tôi mang đến kiến trúc 7 lớp tiêu chuẩn nghiệp vụvà trải nghiệm lập trình (DX) được nâng cấp vượt trội.

- **Kiến trúc 7 Lớp & Unified UI (U2)**:
  - Hoàn thiện mô hình **Unified UI** với 7 phân vùng chức năng rõ rệt: `Reference`, `Market`, `Fundamental`, `Analytics`, `Alternative`, `Macro`, và `Insights`.
  - Cách tiếp cận "Vấn đề là trên hết": Bạn không còn phải lo lắng về việc dữ liệu đến từ đâu, chỉ cần tập trung vào việc bạn muốn làm gì (định giá, xem bảng giá hay tra cứu thông tin cơ bản). Chất lượng và nguồn dữ liệu tốt nhất sẽ được Vnstock khuyến nghị. Bạn có thể cá nhân hoá nguồn dữ liệu như cách lập trình cũ nếu muốn để khai thác các chức năng có sẵn nhưng ẩn sâu trong mã nguồn.
  - Bổ sung thông tin hồ sơ (profile) chi tiết cho **Chứng quyền** và **Hợp đồng tương lai**, giúp bạn nắm bắt đầy đủ thông tin sản phẩm trước khi giao dịch.
  - Tích hợp **Lịch sự kiện thị trường** toàn diện: từ dữ liệu lịch sử (nghỉ lễ, sự cố thị trường... từ năm 2000) đến các sự kiện hiện tại và tương lai giúp bạn bao quát toàn cảnh thị trường một cách chuyên sâu.
- **Trợ lý lập trình thông minh (Next-Gen DX)**:
  - Tái kích hoạt tính năng **Autocomplete** và **Docstring** vượt trội trên các IDE (VSCode, PyCharm), giúp việc viết code nhanh và ít lỗi hơn.
  - Bổ sung bộ công cụ khám phá API: `show_api()` để vẽ sơ đồ thư viện ngay trong terminal và `show_doc()` để đọc nhanh hướng dẫn sử dụng cho từng hàm.
  - Tài liệu (Docstrings) đã được chuyển đổi sang tiếng Anh chuẩn để dễ dàng tiếp cận và phù hợp với tiêu chuẩn lập trình hiện đại và tương tác với AI Agent.
- **Chuẩn hóa & Tối ưu hóa hệ thống**:
  - **Chuẩn hoá dữ liệu bảng giá từ nguồn KBS**: Giải quyết triệt để các vấn đề về hiển thị lô chẵn, lô lẻ; đồng bộ hóa dữ liệu cho đa dạng loại tài sản từ cổ phiếu, phái sinh, chứng quyền đến trái phiếu.
  - Dữ liệu được **tự động chuẩn hóa (Normalization)** từ nhiều nguồn khác nhau về một định dạng duy nhất, giúp việc tính toán và phân tích nhất quán hơn.
  - Cơ chế **Lọc tham số (Kwargs Filtering)**: Giúp giảm thiểu lỗi runtime khi bạn vô tình truyền thừa tham số, tăng tính ổn định cho chương trình.
  - Tối ưu hóa tốc độ tải dữ liệu và cấu trúc nội bộ để sẵn sàng cho các bài toán phân tích dữ liệu lớn.
- **Cập nhật Vnstock Agent Guide**: Tài liệu hướng dẫn chi tiết và các quy tắc cho AI Agent trong lập trình tự động được cập nhật qua Agent Guide [tại đây](https://github.com/vnstock-hq/vnstock-agent-guide/blob/main/docs/vnstock-data/14-unified-ui.md)


* * *

## 05-03-2026

- **Cập nhật module Unified UI (U2)**: Cập nhật các lớp UI cung cấp cấu trúc lệnh hợp nhất với phân nhóm chặt chẽ lấy cảm hứng từ chuẩn FIX và Bloomberg Terminal giúp điều hướng dễ dàng theo mặc định do Vnstock thiết kế và người dùng không cần cài đặt nguồn dữ liệu. Tài liệu hướng dẫn chi tiết được cập nhật qua Agent Guide [tại đây](https://github.com/vnstock-hq/vnstock-agent-guide/blob/main/docs/vnstock-data/14-unified-ui.md)

- **Bổ sung hàm lấy thông tin Chứng quyền và hợp đồng tương lai**:
  - Cung cấp hàm trong giao diện U2 để lấy thông tin chứng quyền và hợp đồng tương lai thông qua Reference().derivatives().warrant() và Reference().derivatives().futures()
- **Bổ sung hàm lấy thông tin bộ lọc cổ phiếu từ VCI** thông qua U2 tại `Insights().screener()`

- **Cải thiện & bổ sung API nguồn Vĩ mô**:
  - Bổ sung method `interest_rate` để lấy dữ liệu Lãi suất bình quân & Doanh số trên thị trường liên ngân hàng. Hỗ trợ tham số `format='pivot'` (mặc định) để trả về bảng dạng nhóm cột (MultiIndex giống biểu diễn trên website) hoặc `format='long'` để trả về định dạng phẳng (raw format).
  - Tích hợp thêm tham số khoảng thời gian tương đối `length` (ví dụ: `90`, `1Y`, `30D`, `100b`) tương tự như cách sử dụng trong `quote.history`. Tính năng này áp dụng đồng bộ cho tất cả các hàm vĩ mô (`gdp`, `cpi`, `interest_rate`, `exchange_rate` v.v...) để bỏ qua việc nhập ngày bắt đầu `start` và kết thúc `end`.
  - Thay đổi thời gian lấy dữ liệu mặc định ( _khi không cung cấp `start`, `end`, hoặc `length`_) là 1 năm (`1Y`) để trả về thông tin ở khoảng thời gian phù hợp và nhẹ.
  - Tài liệu hướng dẫn chi tiết được cập nhật qua Agent Guide [tại đây](https://github.com/vnstock-hq/vnstock-agent-guide/blob/main/docs/vnstock-data/09-macro.md)
- **Cải thiện trải nghiệm sử dụng module lấy dữ liệu hàng hoá**:
  - Tích hợp khả năng lấy thời gian tương đối thông qua tham số `length` tương tự như module `macro` và `quote.history`.
  - Thay đổi thời gian lấy dữ liệu mặc định ( _khi không cung cấp `start`, `end`, hoặc `length`_) về 1 năm (`1Y`) thay vì lấy toàn bộ lịch sử như trước đây.
  - Tài liệu hướng dẫn chi tiết được cập nhật qua Agent Guide [tại đây](https://github.com/vnstock-hq/vnstock-agent-guide/blob/main/docs/vnstock-data/10-commodity.md)

## 31-01-2026

> Phát hành phiên bản 2.3.4, sửa lỗi và cải thiện trải nghiệm người dùng

- Chuẩn hoá định dạng dữ liệu giá thành dạng thập phân xx.xx (ngàn) thay vì xxxx (đồng) cho các hàm `history` và `intraday` trong lớp Quote của nguồn dữ liệu KBS.
- Sửa lỗi không cho phép gọi tham số length trong hàm `history` của lớp Quote của nguồn dữ liệu VCI, VND, MAS khi không truyền tham số `start` và `end`.
- Sửa lỗi không nhận diện nguồn VND cho lớp hàm Market
- Cập nhật chương trình cài đặt vnstock installer chế độ GUI và CLI sử dụng `uv` là công cụ quản lý gói thư viện thay cho `pip`, tăng tốc độ cài đặt và giảm 30% thời gian hoàn thành.

## 28-01-2026

> Phát hành phiên bản 2.3.2, sửa lỗi và cải thiện trải nghiệm người dùng

- Chuẩn hoá tham số `period` để lấy dữ liệu báo cáo tài chính cho các phương thức trong lớp Finance của nguồn dữ liệu KBS - cho phép gọi tham số này khi khởi tạo lớp Finance thay vì gọi ở mỗi phương thức.
- Bổ sung tham số `length` cho phép lấy dữ liệu hàng hoá theo cách tính thời gian tương đối so với hiện tại thay vì bắt buộc nhập ngày bắt đầu và kết thúc.
- Tinh chỉnh nhỏ cho lớp Commodity giúp nạp thư viện chính xác, loại bỏ lỗi liên quan nested f-string sinh ra trong quá trình bảo mật mã nguồn.

## 27-01-2026

> Phát hành phiên bản 2.3.1, bổ sung tài liệu hướng dẫn chi tiết Vnstock Agent Guide.

- Bổ sung hàm tiện ích `convert_derivative_symbol` giúp chuyển đổi mã hợp đồng tương lai kiểu cũ (VN30F1M) sang kiểu mới sau áp dụng KRX (tương đương 41I1G2000 tại thời điểm tháng 1/2026)

- Cải thiện nguồn KBS
  - Sửa lỗi không nhận diện nguồn dữ liệu KBS từ Finance wrapper
  - Bổ sung khả năng lấy dữ liệu báo cáo tài chính nhiều năm thay vì cố định 4 năm như phiên bản trước
  - Tự động nhận diện và chuyển đổi mã hợp đồng tương lai sang kiểu mới để gọi các hàm `history` và `intraday` trong lớp hàm Quote.
  - Bổ sung khả năng lấy dữ liệu các mã index phổ biến HNXINDEX, HNXINDEX, UPCOMINDEX, VN30, VN100, HNX30 trong hàm `history` của lớp Quote.
- Cải thiện chung
  - Hiện cảnh báo mã index không có dữ liệu `intraday`.

## 23-01-2026

- Phát hành phiên bản 2.2.0, bổ sung nguồn dữ liệu KBS cho phép truy cập từ các dịch vụ cloud của Google như Google Colab, Kaggle thay vì nguồn VCI bị chặn IP.
- Bổ sung khả năng truy xuất thông tin các bộ chỉ số đầu tư và chỉ số ngành từ HOSE vào Listing class, truy cập được từ mọi giá trị source.
- Cập nhật yêu cầu phiên bản gói phụ thuộc tương thích.

## 31-08-2025

> Phát hành phiên bản Vnstock News 2.1.0 nâng cấp toàn diện cơ chế tải dữ liệu và cung cấp khả năng tuỳ biến linh hoạt, bổ sung tài liệu hướng dẫn chi tiết.

[Xem hướng dẫn](https://vnstocks.com/docs/vnstock-news)

Để cài đặt bản cập nhật, vui lòng chạy lại chương trình cài đặt của Vnstock [tại đây](https://vnstocks.com/onboard-member/cai-dat-go-loi/cai-dat-phan-mem).

- Thay đổi hoàn toàn cấu trúc chương trình theo hướng chặt chẽ và module hoá
- Cung cấp cơ chế tự xử lý link sitemap và rss linh hoạt đối với các website sử dụng cơ chế động ví dụ sitemap theo năm-tháng, sitemap với số đếm tăng dần.
- Hỗ trợ đầy đủ 10 trang web có sẵn trong danh sách định nghĩa sẵn, người dùng có thể tự bổ sung thêm cấu hình để dùng vnstock\_news như một chương trình crawler đọc tin tức hàng loạt.

## 29-08-2025

> Phát hành phiên bản Vnstock Pipeline 2.0.1 nâng cấp cơ chế tải dữ liệu Intraday và Streaming dữ liệu thời gian thực.

[Xem hướng dẫn](https://vnstocks.com/docs/vnstock-pipeline)

Để cài đặt bản cập nhật, vui lòng chạy lại chương trình cài đặt của Vnstock [tại đây](https://vnstocks.com/onboard-member/cai-dat-go-loi/cai-dat-phan-mem).

- Bổ sung tài liệu hướng dẫn tuỳ biến chương trình
- Cải thiện trải nghiệm sử dụng: tuỳ chọn địa điểm lưu file khi streaming, lọc dữ liệu mong muốn thay vì tự lưu toàn bộ.
- Cải thiện khả năng truy cập dữ liệu intraday liên tục trong phiên giao dịch và ghép nối thông minh hơn.
- Bổ sung tính năng Data Manager cho phép quản lý cấu trúc dữ liệu lưu trữ khoa học và chặt chẽ
- Bổ sung khả năng lưu trữ dữ liệu định dạng parquet, nén dữ liệu ~75% so với CSV và tăng hiệu năng xử lý.

## 21-07-2025

> Phát hành phiên bản Vnstock Data 2.1.3 và nâng cấp cơ chế quản lý license chính xác hơn.

Để thực hiện nâng cấp phiên bản, các bạn vui lòng chạy lại chương trình cài đặt, lưu ý nên chạy thử và trải nghiệm qua môi trường như Github Codespace để hình dung các thay đổi để không làm ảnh hưởng đến chương trình hiện có. Hệ thống **không thể quay lại phiên bản cú sau nâng cấp**.

[Nâng cấp](https://vnstocks.com/onboard-member/cai-dat-go-loi/cai-dat-phan-mem)

### Ads Free

Ẩn banner quảng cáo đối với người dùng đang duy trì gói sponsor trừ những thông báo đặc biệt liên quan đến trải nghiệm người dùng hoặc yêu cầu nâng cấp bắt buộc.

### Vnstock Data Explorer

- Bổ sung nguồn Fmarket vào mã nguồn
- Bổ sung và nâng cấp các API của nguồn VCI
  - Thay thế API các nhóm hàm Quote, Listing class gặp lỗi từ chối truy cập và đổi url
  - Bổ sung bộ API mới cho nhóm hàm thuộc Financial class
    - Cập nhật API mới
    - Cho phép sử dụng tiếp API cũ từ máy tính local nếu muốn.
  - Sửa đổi nhóm hàm Trading cho phép lấy dữ liệu phân tích lịch sử giao dịch & bảng giá
    - Thêm các hàm `foreign_trade` để lấy riêng thông tin giao dịch nước ngoài
    - Loại bỏ các hàm `trading_stats` và `side_stats` trong nhóm hàm thuộc Trading class để không trùng thông tin với hàm `price_board`

## 02-06-2025

### Vnstock Data Explorer

Cập nhật phiên bản 2.1.2

Bổ sung hàm truy xuất dữ liệu lịch sử giao dịch từ VCI với Trading class thay thế dữ liệu từ CafeF gặp lỗi.

Chi tiết hàm bổ sung tại [Nguồn VCI - Thống kê giao dịch](https://vnstocks.com/vnstock-insider-api/vnstock-data/du-lieu-giao-dich#ngu%E1%BB%93n-vci)

## 06-05-2024

### Vnstock Data Explorer

Cập nhật phiên bản 2.1.1

Cập nhật phiên bản Vnstock Data 2.1.1 sửa lỗi hàm Intraday sau khi triển khai hệ thống KRX từ 5/5/2025 và cải thiện trải nghiệm người dùng.

- [Issue 164](https://github.com/thinh-vu/vnstock/issues/164): Cập nhật tính năng thay đổi user\_agent ngẫu nhiên không sử dụng gói fake\_user\_agent
- [Issue 172](https://github.com/thinh-vu/vnstock/issues/172): Bổ sung hàm `price_board` cho Trading class thuộc nguồn dữ liệu VCI
- [Issue 178](https://github.com/thinh-vu/vnstock/issues/178) và sửa lỗi dữ liệu Intraday sau cập nhật hệ thống KRX cho nguồn VCI và MAS.
- Đóng [Issue 169](https://github.com/thinh-vu/vnstock/issues/169) vì dữ liệu khung thời gian `1W` đã được hỗ trợ sẵn trong thư viện.
- [Issue 166](https://github.com/thinh-vu/vnstock/issues/166) Cập nhật thiết lập rate limit cho các nguồn dữ liệu trong gói tài trợ, tránh hiển thị nhầm thông báo nâng cấp.

## 22-04-2025

### Vnstock Data Explorer

> Phiên bản `vnstock_data` **2.1.0** đánh dấu bước tiến lớn trong khả năng quản lý và mở rộng dữ liệu, với việc áp dụng **cấu trúc Adapter** chuẩn hóa toàn bộ giao tiếp với nguồn cấp dữ liệu.

#### ✨ Những Thay Đổi Quan Trọng

| Hạng mục | Thay đổi |
| --- | --- |
| **Cấu trúc thư viện** | Triển khai mô hình **Adapter Pattern** cho tất cả các lớp dữ liệu (Quote, Trading, Finance, Listing, Company, Macro, Commodity, v.v.). |
| **Cách gọi hàm** | Các hàm khi sử dụng Adapter cần truyền **tham số `source`** để xác định rõ nhà cung cấp dữ liệu mong muốn. |
| **Mặc định `source`** | Tham số `source` **không còn mặc định ngầm định** như phiên bản trước. Nếu không truyền `source` đúng, hàm có thể gây lỗi `NotSupportedError`. |
| **Hướng dẫn chi tiết hơn** | Bổ sung [bảng tra cứu](https://vnstocks.com/vnstock-insider-api/vnstock-data/kien-truc-thu-vien) phương thức hỗ trợ theo nguồn cấp dữ liệu, và sơ đồ hệ thống trực quan. |

#### 🚨 Lưu Ý Ảnh Hưởng Đến Đoạn Mã Cũ

Nếu bạn đang sử dụng `vnstock_data` theo cách cũ

Python

```python
from vnstock_data import Trading
trading = Trading(symbol='MSN')
quote.history(start="2024-01-01", end="2024-04-01")
```

➡️ Từ phiên bản 2.1.0, đoạn code trên **sẽ lỗi** nếu thông tin `source` không trùng khớp với nguồn cấp dữ liệu hỗ trợ. Cụ thể, bạn cần sửa lại thành:

Python

```python
from vnstock_data import Trading
quote = Quote(source="cafef", symbol="VCI")
quote.history(start="2024-01-01", end="2025-04-18", interval="1D")
```

### Thảo luận

Đang tải bình luận...