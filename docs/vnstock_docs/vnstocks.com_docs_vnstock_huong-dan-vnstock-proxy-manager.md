---
url: "https://vnstocks.com/docs/vnstock/huong-dan-vnstock-proxy-manager"
title: "Sử dụng Proxy truy cập Dữ liệu bị chặn | Vnstock"
---

## Mục lục

Lưu ý quan trọng

**Mục đích sử dụng:** Hướng dẫn này dành cho mục đích nghiên cứu và cá nhân trải nghiệm Vnstock. Việc sử dụng proxy không nhằm mục đích vượt qua các biện pháp bảo vệ hợp pháp của nguồn dữ liệu. Vnstock khuyến khích sử dụng proxy một cách có trách nhiệm để tránh tạo tác động tiêu cực đến hệ thống nguồn.

Khi nào cần sử dụng Proxy

Proxy đặc biệt hữu ích trong các trường hợp:

- Truy cập từ môi trường đám mây bị chặn IP như Google Colab, Kaggle
- Mạng nội bộ hoặc VPN có hạn chế truy cập
- Cần phân tán tải truy cập để tránh rate limiting
- Thử nghiệm và phát triển ứng dụng với nhiều địa điểm

## Tổng quan về ProxyManager

ProxyManager là một tiện ích trong [proxy\_manager](https://github.com/thinh-vu/vnstock/blob/main/vnstock/core/utils/proxy_manager.py) cung cấp khả năng:

- Tự động lấy danh sách proxy miễn phí từ proxyscrape API
- Kiểm tra và xác thực proxy hoạt động
- Chuyển đổi proxy tự động cho các yêu cầu
- Tích hợp dễ dàng với các module của Vnstock
- Hỗ trợ nhiều giao thức (HTTP, HTTPS, SOCKS5)

_ProxyManager giúp giải quyết vấn đề truy cập dữ liệu từ môi trường bị chặn IP, đồng thời cung cấp các công cụ để quản lý và chuyển đổi proxy một cách tự động và hiệu quả._

## Cài đặt và Khởi tạo

_Cài đặt và khởi tạo ProxyManager là bước đầu tiên để bắt đầu sử dụng proxy trong Vnstock. Phần này hướng dẫn cách import thư viện và tạo instance với các tùy chọn cơ bản._

### Import và Khởi tạo Cơ bản

Python

```python
from vnstock.core.utils.proxy_manager import ProxyManager

# Khởi tạo với timeout mặc định 10 giây
proxy_manager = ProxyManager()

# Hoặc tùy chỉnh timeout
proxy_manager = ProxyManager(timeout=15)
```

_Import và khởi tạo ProxyManager với timeout tùy chỉnh để phù hợp với điều kiện mạng của bạn._

### Lấy Danh sách Proxy

Python

```python
# Lấy 20 proxy đầu tiên
proxies = proxy_manager.fetch_proxies(limit=20)

print(f"Đã lấy được {len(proxies)} proxy")
```

_Lấy danh sách proxy từ API proxyscrape với số lượng tùy chỉnh. Đây là bước cơ bản để có được các proxy sẵn sàng sử dụng._

**Dữ liệu mẫu:**

Shell

```bash
>>> proxies = proxy_manager.fetch_proxies(limit=5)
Đã lấy được 5 proxy

>>> proxy_manager.print_proxies()
Giao thức   IP              Port   Quốc gia         Tốc độ (ms)
------------------------------------------------------------
http       139.99.237.62   80                     0.00
http       101.109.119.24  8080                   0.00
http       108.162.192.0   80                     0.00
http       108.162.192.113 80                     0.00
http       139.162.78.109  8080                   0.00
```

## Kiểm tra và Lọc Proxy

_Sau khi lấy được danh sách proxy, việc kiểm tra và lọc ra các proxy hoạt động là rất quan trọng để đảm bảo hiệu suất và độ tin cậy khi sử dụng._

### Kiểm tra Proxy Đơn lẻ

Python

```python
from vnstock.core.utils.proxy_manager import Proxy

# Tạo proxy object
proxy = Proxy(protocol='http', ip='101.109.119.24', port=8080)

# Kiểm tra proxy
is_working = proxy_manager.test_proxy(proxy)
print(f"Proxy hoạt động: {is_working}")
```

_Kiểm tra từng proxy riêng lẻ để xác định xem nó có hoạt động tốt không, giúp lọc ra các proxy chất lượng._

### Kiểm tra Nhiều Proxy

Python

```python
# Kiểm tra tất cả proxy đã fetch
working_proxies, failed_proxies = proxy_manager.test_proxies()

print(f"Proxy hoạt động: {len(working_proxies)}")
print(f"Proxy lỗi: {len(failed_proxies)}")
```

_Kiểm tra hàng loạt proxy để phân loại thành working và failed, tiết kiệm thời gian và tăng hiệu quả._

### Lấy Proxy Tốt Nhất

Python

```python
# Lấy proxy nhanh nhất
best_proxy = proxy_manager.get_best_proxy()
if best_proxy:
    print(f"Proxy tốt nhất: {best_proxy}")
    print(f"Địa chỉ: {best_proxy.address}")
```

_Chọn proxy có tốc độ nhanh nhất từ danh sách để tối ưu hóa hiệu suất truy cập dữ liệu._

#### Tags

[proxy manager](https://vnstocks.com/blog/tag/proxy-manager) [vnstock](https://vnstocks.com/blog/tag/vnstock) [web scraping](https://vnstocks.com/blog/tag/web-scraping)

### Thảo luận

Đang tải bình luận...