---
url: "https://vnstocks.com/docs/vnstock-news/tuy-bien-nang-cao"
title: "Tùy biến Nâng cao | Vnstock"
---

Toggle Sidebar

### Mục lục

Kỹ thuật chuyên sâu

Bộ công cụ nâng cao hỗ trợ truy xuất bộ đếm từ khóa và thiết lập cấu hình bộ đệm lưu trữ truy cập web trung gian. Bạn chỉ nên áp dụng khi có nhu cầu thu thập dữ liệu tự động - phù hợp cho các lập trình viên, chuyên viên khoa học máy tính hoặc nhà phân tích dữ liệu.

## Phân Tích Thông Tin Khái Quát (Trending Keywords)

Thư viện tích hợp mô-đun phân rã chuỗi (tokenizer) để xuất từ vựng định tính theo mức độ xuất hiện. Dưới đây là kiến trúc tham chiếu mô hình thực thi thuật toán thống kê:

Python

```python
from vnstock_news import Crawler
from collections import Counter
import re

crawler = Crawler(site_name="tuoitre")
articles = crawler.get_articles_from_feed(limit_per_feed=30) # Vận hành 30 chuỗi gần nhất

corpus = []
for article in articles:
    title = article.get('title', '')
    words = re.findall(r'\w+', title.lower())
    # Tính lọc các cấu trúc chỉ lấy chuỗi chữ cái độ dài tối thiểu 3
    corpus.extend([w for w in words if len(w) >= 3])

most_common_topics = Counter(corpus).most_common(10)
print(f"Từ Khóa Đặc Trưng Trong Dữ Liệu Hiện Tại:")
for word, count in most_common_topics:
    print(f"  {word:15s} - Tần suất: {count}")
```

## Chế Độ Triển Khai Chuyên Sâu: `EnhancedNewsCrawler`

Các mô hình được sử dụng trong khối lượng công việc thực tế yêu cầu kiến trúc của `EnhancedNewsCrawler` nhằm bổ sung tính linh hoạt:

- **Lưu trữ Cục Bộ (Cache)**: Khi chạy trong lu kỳ 2 giờ, chức năng bảo toàn phản hồi (HTTP caching) tái sử dụng khối dữ liệu của URL đã lấy trước đó mà không truy xuất API trên máy chủ nguồn, giúp ngăn lỗi từ chối dịch vụ do truy cập quá mức (Rate limits).
- **Bộ Chuyển Hóa Markdown**: Có khả năng xóa mã nguồn HTML (tham số cấu hình `clean_content=True`) để dữ liệu đầu ra làm việc dễ dàng với các mô hình LLM hiện đại.

## Tùy Biến Lớp Tham Chiếu Hệ Thống CMS Bất Kỳ (Custom Profile)

Python

```python
from vnstock_news import Crawler

custom_website_profile = {
    "site_name": "example_tech_site",
    # Mới 🚀: Khai báo sitemap có cấu trúc động (DynamicSitemapResolver)
    "sitemap": {
        "base_url": "https://example.com/sitemaps/news-",
        "pattern_type": "monthly", # Trích xuất tuần tự theo định dạng tháng
        "format": "{year}-{month}",
        "extension": "xml",
        "current_url": ""
    },
    # (Tùy chọn) Cung cấp RSS nếu muốn ưu tiên
    "rss": {
        "urls": ["https://example.com/rss/tin-moi.rss"]
    },
    "config": {
        "title_selector": {"tag": "h1", "class": "title-detail"},
        "content_selector": {"tag": "article", "class": "fck_detail"},
        "publish_time_selector": {"class": "date"}
    }
}

crawler = Crawler(custom_config=custom_website_profile)

# Hệ thống tự động phân giải liên kết Sitemap của tháng hiện tại thông qua pattern_type
recent_articles = crawler.get_latest_articles(limit=5)
for article in recent_articles:
    print(f"Tiêu đề: {article['title']}")
```

Thông qua tham chiếu `custom_config`, công cụ tiếp tục kết hợp các phương pháp chẩn đoán mạng thông minh. Nhờ module `DynamicSitemapResolver`, `vnstock_news` có thể tự động dò tìm cấu trúc đường dẫn Sitemap thay đổi theo thời gian (ví dụ: `news-2026-04.xml`) dựa trên mốc thời gian hiện tại mà không đòi hỏi khai báo thủ công từ người dùng.

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập