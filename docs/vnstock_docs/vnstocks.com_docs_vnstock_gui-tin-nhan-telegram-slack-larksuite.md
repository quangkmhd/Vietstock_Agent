---
url: "https://vnstocks.com/docs/vnstock/gui-tin-nhan-telegram-slack-larksuite"
title: "Gửi tin nhắn Telegram, Lark, Slack | Vnstock"
---

## Mục lục

Giới thiệu

**Vnstock** cung cấp tới bạn các hàm kết nối tới [Telegram API](https://core.telegram.org/) và [Slack API](https://api.slack.com/) cho phép gửi tin nhắn, hình ảnh qua Slack channel và Telegram group. Đây là tính năng mở ra các ứng dụng gửi tin tức, cảnh báo giao dịch và các thông tin quan trọng tới bạn mà không cần đi qua bất kỳ dịch vụ trung gian nào. Các thiết dưới đây áp dụng với bản Vnstock 3.0.6

Trong vnstock, bạn sẽ sử dụng Messenger class để thực hiện việc gửi các loại tin nhắn đến nền tảng được hỗ trợ. Cấu hình class này như sau:

Python

```python
from vnstock.botbuilder.noti import Messenger
noti = Messenger(platform='telegram', channel='-1001439492355', token_key='TOKEN_CỦA_BẠN')
```

Trong đó:

- platform (str): tên của nền tảng nhắn tin bạn chọn, nhận các giá trị là `telegram`, `slack` và `lark`
- channel (str): tên hoặc mã nhận dạng của kênh trong nền tảng nhắn tin. Ví dụ `#news_update` cho tên kênh Slack, `-1001439492355` cho mã của nhóm nhận tin nhắn trong Telegram, để None nếu bạn chọn nền tảng là Lark.
- token\_key: là mã bảo mật của API sử dụng cho app nhắn tin bạn chọn theo từng nền tảng. Đối với Lark thì đây là mã id của webhook URL.

Tiếp theo, hàm `send_message` sẽ được sử dụng chung cho tất cả các nền tảng nhắn tin dù bạn gửi tin nhắn văn bản hay kèm hình ảnh.

Python

```python
noti.send_message(message='Tin nhắn của bạn', file_path='Đường dẫn file trên máy tính hoặc để None', title='Tiêu đề ảnh bạn chọn')
```

Cụ thể, thông số thiết lập gồm:
\- message (str, bắt buộc): Nội dung tin nhắn bạn muốn gửi qua bot
\- file\_path (str, tuỳ chọn): Đường dẫn file trên máy tính. Nếu sử dụng trên máy tính Windows, lưu ý đặt chữ `r` phía trước, ví dụ `r'path/to_your_image_file.png'`
\- title (str, tuỳ chọn): tiêu đề ảnh/file nếu bạn gửi tin nhắn trong Slack khi có kèm file.

Kết quả trả về dưới dạng JSON từ server phản hồi. Cụ thể việc tạo và thiết lập bot cho từng nền tảng, bạn có thể tham khảo hướng dẫn bên dưới.

## Gửi tin nhắn Telegram

Tạo Telegram bot đầu tay là một quá trình tương đối đơn giản, bạn có thể thực hiện toàn bộ các công đoạn để có thể gửi được tin nhắn trong chưa đầy 15 phút.

### 1\. Tạo bot với BotFather

1. Nếu bạn không muốn sử dụng bot chung với tài khoản Telegram hiện có vì lý do bảo mật thì cần bắt đầu tạo tài khoản mới với App Telegram trên Smartphone trước khi bắt đầu. Trong giao diện nhắn tin, tìm kiếm BotFather và thao tác như hình dưới.
2. Đăng nhập [telgram web](https://web.telegram.org/) để tạo và thiết lập bot.
3. Copy đoạn token và lưu giữ cẩn thận để bảo mật.

![Telegram botfather tạo bot](https://vnstocks.com/images/telegram_botfather_tao_bot_vnstock.png)Telegram botfather tạo bot

### 2\. Thiết lập thông tin bot

Bước này chỉ đơn giản là cập nhật ảnh đại diện và mô tả của bot để dễ phân biệt với tài khoản thông thường.

![Thông tin Telegram bot và thiết lập](https://vnstocks.com/images/thong_tin_telegram_bot_va_thiet_lap_vnstock.png)Thông tin Telegram bot và thiết lập

### 3\. Gửi tin nhắn

1. Copy ID của nhóm chat để sử dụng cho hàm gửi tin nhắn.
2. Sử dụng đoạn code do vnstock cung cấp để gửi tin nhắn
3. Tận hưởng thành quả: tin nhắn gửi từ API thành công

![Code vnstock telegram bot](https://vnstocks.com/images/code_vnstock_telegram_bot_vnstock.png)Code vnstock telegram bot![ID nhóm chat telegram](https://vnstocks.com/images/id_nhom_chat_telegram_vnstock_tin_nhan_thanh_cong_vnstock.png)ID nhóm chat telegram

## Gửi tin nhắn Lark BotBuilder

[Lark BotBuilder](https://botbuilder.larksuite.com/home) là một công cụ cho phép xây dựng các luồng tự động hoá công việc (automated workflows) trong bộ ứng dụng văn phòng [LarkSuite](https://www.larksuite.com/). Bạn có thể gửi tin nhắn vào Webhook của 1 app bất kỳ tạo ra bởi BotBuilder một cách an toàn và bảo mật. Việc cài đặt 1 luồng công việc tự động với BotBuilder cũng tương đối đơn giản và linh hoạt theo hướng dẫn dưới đây.
Ngoài việc dùng BotBuilder để gửi tin nhắn Lark, bạn còn có thể kích hoạt bot để gọi API và thực hiện nhiều luồng công việc khác nhau sử dụng các ứng dụng trong nền tảng Larksuite, bạn hãy khám phá thêm các ứng dụng thú vị cho riêng mình.

### 1\. Tạo App

Truy cập trang web [Botbuilder](https://botbuilder.larksuite.com/home) và tạo cho bạn 1 app đầu tay. Sau khi đặt tên Bot và bấm Create, bạn sẽ được đưa đến màn hình tiếp theo tại mục Flow Design, chọn Create để tiếp tục.

![Lark tạo app botbuilder](https://vnstocks.com/images/lark_tao_app_botbuilder.png)Lark tạo app botbuilder

### 2\. Chọn Trigger

Tại màn hình tiếp lập `flow`, chọn Webhook Trigger để kích hoạt luồng tác vụ tự động.

![Lark chọn webhook trigger](https://vnstocks.com/images/lark_chon_webhook_triggger.png)Lark chọn webhook trigger

### 3\. Copy URL

Copy Webhook URL để sử dụng, tách riêng phần ID của url này để sử dụng với hàm nhắn tin từ Vnstock.

![Lark copy webhook url](https://vnstocks.com/images/lark_copy_webhook_url.png)Lark copy webhook url

### 4\. Thiết lập nhắn tin

Bạn cần thiết lập hành động gửi tin nhắn tới cá nhân hoặc nhóm cụ thể trong tổ chức sau khi bot nhận được thông tin dạng JSON từ Webhook.

![Lark chọn hành động gửi tin nhắn](https://vnstocks.com/images/lark_chon_hanh_dong_gui_tin_nhan_tu_webhook.png)Lark chọn hành động gửi tin nhắn

### 5\. Định dạng

Cuối cùng, bạn thiết lập định dạng và cách thức hiển thị của tin nhắn sẽ được gửi đi khi bot được kích hoạt bằng Webhook. Sau khi hoàn tất thiết lập, bạn có thể chọn nút Enable sau đó đặt tên `flow` để kích hoạt bot.

![Lark gửi tin nhắn từ webhook](https://vnstocks.com/images/lark_gui_tin_nhan_tu_webhook.png)Lark gửi tin nhắn từ webhook

## Gửi tin nhắn Slack

Tham khảo hướng dẫn gửi tin nhắn Slack từ tài liệu API chính thức [tại đây](https://api.slack.com/messaging/sending)

#### Tags

[gửi cảnh báo](https://vnstocks.com/blog/tag/gui-canh-bao) [telegram bot](https://vnstocks.com/blog/tag/telegram-bot) [bot tín hiệu](https://vnstocks.com/blog/tag/bot-tin-hieu)

### Thảo luận

Đang tải bình luận...