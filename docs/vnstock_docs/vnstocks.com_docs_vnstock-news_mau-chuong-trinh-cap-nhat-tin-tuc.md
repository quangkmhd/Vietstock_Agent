---
url: "https://vnstocks.com/docs/vnstock-news/mau-chuong-trinh-cap-nhat-tin-tuc"
title: "Mẫu Chương trình Cập nhật Tin tức | Vnstock"
---

Toggle Sidebar

### Mục lục

Giới thiệu

Phần này trình bày cấu trúc của một hệ thống cập nhật tin tức tự động dựa trên thư viện \`vnstock\_news\`.

## Sử dụng qua Dòng Lệnh (CLI)

Sau khi hoàn tất cài đặt cấu hình thư viện, bạn có thể khởi chạy chương trình theo dõi tin tức trực tiếp từ dòng lệnh Terminal nhằm kiểm thử quá trình trích xuất và lưu trữ dữ liệu:

Shell

```bash
vnstock-news-crawler
```

Bởi vì `vnstock_news` sở hữu danh mục tính năng đa dạng, bạn có thể giao phó quy trình kiến trúc mã nguồn (coding) cho AI để có thể tập trung vào các logic nghiệp vụ thay vì kỹ thuật. Tải tài liệu theo liên kết **Agent Guide** bên dưới và mở trong các chương trình chuyên biệt như Google Antigravity, Claude Code đẻ tác nhân AI sử dụng kỹ năng được Vnstock chỉ dẫn và tiến hành xây dựng kịch bản chuyên sâu theo mức độ tùy chỉnh cao.

[Truy cập tài liệu Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)

![Khởi động chương trình Vnstock News từ Terminal của macOS](https://vnstocks.com/images/khoi-dong-vnstock-news-che-do-dong-lenh.png)Khởi động chương trình Vnstock News từ Terminal của macOS

Khi khởi chạy, chương trình quản lý luồng điều phối (Orchestrator) tự động kết nối nguồn tin công khai của các báo được thiết kế cho bot truy cập, thực hiện trích xuất đồng lịch sử tin tức theo điều kiện thời gian bạn yêu cầu và biên dịch tập tin dưới dạng CSV, lưu trữ tại thư mục định danh `output`.

![Nội dung dữ liệu tin tức được chuẩn hoá từ Vnstock News](https://vnstocks.com/images/bang-tinh-noi-dung-tin-tuc-chuan-hoa-vnstock-news.png)Nội dung dữ liệu tin tức được chuẩn hoá từ Vnstock News

Khung báo cáo sau thống kê sẽ xuất về tệp tĩnh mang thuật ngữ `news_summary.txt`:

Shell

```bash
News Monitor Report - 2024-xx-xx
==================================================

STATISTICS
--------------------------------------------------
Total articles collected: 580

TRENDING TOPICS
--------------------------------------------------
1. chứng khoán: 107 mentions
2. thị trường: 76 mentions
...
```

Giao diện vận hành thực tế minh họa trên Google Colab.
![Tóm tắt kết quả chương trình khi kết nối và phân tích tin tức trên Google Colab](https://vnstocks.com/images/tom-tat-ket-qua-thuc-thi-vnstock-news.png)Tóm tắt kết quả chương trình khi kết nối và phân tích tin tức trên Google Colab

## Tham khảo hệ thống giám sát bằng kịch bản Python

Với mục đích tham khảo cấu trúc, đoạn mã Python theo tiêu chuẩn dưới đây triển khai khai thác nguồn tin nóng (RSS) cũng như cào lưu trữ tuần tự (Sitemap) từ các nhà cung cấp tin. Trong quá trình tạo dự án, bạn hoàn toàn có thể yêu cầu AI Agent xây dựng hệ thống thay vì tự vận hành mã thủ công:

Python

```python
from vnstock_news import Crawler, BatchCrawler
import pandas as pd
from datetime import datetime

def automated_news_harvester():
    print("Khởi động quy trình thu thập nội dung cấu trúc hóa...")

    # 1. Trích xuất RSS
    print("\\n[1] Lấy danh mục tin xuất bản gần nhất qua RSS của VnExpress")
    rss_crawler = Crawler(site_name="vnexpress")
    feed_data = rss_crawler.get_articles_from_feed(limit_per_feed=20)

    if feed_data:
        df_feed = pd.DataFrame(feed_data)
        print(f"Trích xuất {len(df_feed)} văn bản từ hệ thống máy chủ RSS.")

    # 2. Xây dựng tài nguyên trên dữ liệu tồn kho bằng Sitemap
    print("\\n[2] Xử lý số lượng lớn phiên bản lưu trữ thông qua Sitemap của CafeF")
    # Định tuyến thời gian phân luồng (request_delay) theo chuẩn đạo đức phân tích web
    batch_executor = BatchCrawler(site_name="cafef", request_delay=1.0)
    historical_corpus = batch_executor.fetch_articles(limit=50)

    if not historical_corpus.empty:
        print(f"Trích xuất {len(historical_corpus)} văn bản từ hệ thống máy chủ Sitemap.")

        # 3. Kết xuất CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"cafef_audit_{timestamp}.csv"
        historical_corpus.to_csv(filename, index=False)
        print(f"\\nHoàn thành kết xuất dữ liệu cấu trúc về đường dẫn: {filename}")

if __name__ == "__main__":
    automated_news_harvester()
```

Những lệnh truyền dẫn qua class `BatchCrawler` mang lại độ kiểm soát bảo trì đáng kể thay vì vận động thao tác mã ngẫu nhiên trên các thư viện HTTP Requests ở cấp độ mạng.

### Thảo luận

Đang tải bình luận...

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập