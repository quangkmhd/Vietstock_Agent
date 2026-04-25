---
url: "https://vnstocks.com/docs/vnstock/google-gemini-ai-flash-phan-tich-du-lieu-vnstock"
title: "Dùng Gemini AI phân tích dữ liệu chứng khoán | Vnstock"
---

## Mục lục

Gợi ý

Thư viện [gemini\_ai](https://github.com/vnstock-hq/gemini_ai) do Vnstock phát triển cung cấp một giao diện mạnh mẽ để tương tác với mô hình AI Gemini của Google. Với `gemini_ai`, người dùng có thể cấu hình linh hoạt mô hình, quản lý phiên hội thoại, tải tệp lên và truy xuất dữ liệu phản hồi từ mô hình. Gói này được tối ưu hóa đặc biệt để hoạt động hiệu quả trên Google Colab và môi trường Jupyter Notebook.

[Demo Notebook](https://colab.research.google.com/github//vnstock-hq/gemini_ai/blob/main/docs/gemini_ai_demo_notebook.ipynb) [Xem thư viện](https://github.com/vnstock-hq/gemini_ai)

## Tính năng chính

- **Cấu hình mô hình linh hoạt**: Tùy chỉnh thông số mô hình như `temperature`, `top-p`, `top-k` và giới hạn token đầu ra để tạo ra phản hồi đa dạng.
- **Hỗ trợ tệp và media**: Cho phép tải lên các loại tệp (ảnh, âm thanh, văn bản) trong môi trường Google Colab và sử dụng API của Gemini để xử lý các nội dung này.
- **Quản lý hội thoại và phản hồi**: Cung cấp các phương thức để quản lý lịch sử hội thoại, đếm token và stream phản hồi.
- **Tối ưu hóa theo môi trường**: Tự động nhận diện môi trường Google Colab và Jupyter Notebook để tối ưu hóa trải nghiệm.

## Cài đặt

Để cài đặt gói `gemini_ai` và các thư viện phụ thuộc, bạn có thể sử dụng lệnh sau:

Shell

```bash
pip install gemini_ai
```

Lệnh này sẽ tự động cài đặt tất cả các thư viện cần thiết như `google-generativeai`, `pillow`, `ipywidgets`, và `ipython`.

## Hướng dẫn sử dụng

### 1\. Khởi tạo GeminiAI

Đầu tiên, bạn cần có API key của Google Gemini. Hãy đăng ký và lấy API key của bạn tại [Google AI Studio](https://aistudio.google.com/app/apikey). Mã Token nên được lưu vào mục Secrets của Google Colab để sử dụng thuận tiện.

Python

```python
from gemini.gemini import GeminiAI

# Khởi tạo đối tượng GeminiAI với API key của bạn
gemini = GeminiAI(api_key="YOUR_API_KEY")
```

### 2\. Cấu hình Mô Hình

Bạn có thể cấu hình mô hình với các tham số như `temperature`, `top_p`, `top_k` và `max_output_tokens` để tùy chỉnh cách mà mô hình tạo phản hồi. Bỏ qua nếu không muốn thay đổi cấu hình mặc định.

Python

```python
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
```

### 3\. Khởi Tạo Phiên Hội Thoại

Để bắt đầu một phiên hội thoại với mô hình AI, bạn cần cung cấp chỉ dẫn (instruction). Nếu đang làm việc trên Google Colab, bạn cũng có thể tải tệp lên để làm ngữ cảnh cho hội thoại.

Python

```python
gemini.start_chat(instruction="Đóng vai trò là một chuyên viên phân tích tài chính. Tôi sẽ cung cấp bảng dữ liệu dưới dạng bảng Markdown. Hãy đọc, xử lý và phân tích dữ liệu đó, cung cấp các nhận định về tình hình tài chính hoặc xu hướng dựa trên số liệu trong bảng.")
```

### 4\. Gửi Tin Nhắn và Tạo Nội Dung

Sau khi khởi tạo phiên hội thoại, bạn có thể gửi các câu hỏi cho mô hình AI và nhận phản hồi. Phương thức `send_message` phù hợp cho các phản hồi ngắn, trong khi `generate` giúp tạo ra các phản hồi chi tiết hơn với tùy chọn stream.

Trước tiên, hãy thử sử dụng dữ liệu Báo cáo kết quả kinh doanh của hàng quý của ACB làm một ví dụ

Python

```python
from vnstock import Vnstock
stock = Vnstock().stock(symbol='ACB', source='VCI')
income_df = stock.finance.income_statement(period='quarter', lang='vi')
```

Python

```python
# Gửi một câu hỏi khởi động
gemini.send_message(prompt=f'Dưới đây là Báo cáo Kết quả Kinh doanh của Ngân hàng ACB dạng văn bản. Phân tích tình hình doanh thu, lợi nhuận gộp, chi phí và lợi nhuận ròng trong các quý gần đây của ACB. Hãy nhận định về xu hướng tài chính của ngân hàng này, đánh giá hiệu quả kinh doanh và cung cấp các nhận xét về khả năng phát triển trong tương lai. Dữ liệu chi tiết: {income_df.to_string()}')

# Đặt câu hỏi tiếp theo
gemini.send_message(prompt="Dựa trên phân tích lợi nhuận ròng và chi phí qua các quý, bạn có thể đánh giá khả năng kiểm soát chi phí của ACB không?", stream=True)
```

### 5\. Quản lý Lịch Sử Hội Thoại và Đếm Token

Bạn có thể xem lại lịch sử hội thoại hoặc đếm token trong phiên hội thoại để quản lý mức sử dụng API hiệu quả hơn.

Python

```python
# Hiển thị lịch sử hội thoại
gemini.history()

# Đếm số lượng token đã sử dụng trong phiên hội thoại
gemini._token_counts()
```

## Tính Năng Riêng Cho Môi Trường

`GeminiAI` sẽ tự động tối ưu hóa các tính năng dựa trên môi trường làm việc. Cụ thể:

- **Google Colab**: Hỗ trợ tải tệp lên trực tiếp và tích hợp các tiện ích của `google.colab`.
- **Jupyter Notebook**: Hạn chế một số chức năng tải tệp, và tự động bỏ qua các tính năng không hỗ trợ.

## Tổng Quan về Các Phương Thức Chính

### class `GeminiAI`

#### `__init__(api_key: str, gemini_model: str = 'gemini-1.5-flash-latest')`

Khởi tạo đối tượng `GeminiAI` với API key và tên mô hình.

- **api\_key** (str): API key của bạn để kết nối với Gemini AI.
- **gemini\_model** (str): Phiên bản mô hình Gemini. Mặc định là `'gemini-1.5-flash-latest'`.

#### `config(temp: Optional[int] = 1, top_p: Optional[float] = 0.95, top_k: Optional[int] = 64, max_output_tokens: Optional[int] = 8192, response_mime_type: str = "text/plain", stream: bool = True, silent: bool = True)`

Cấu hình các thông số tạo phản hồi của mô hình.

#### `start_chat(instruction: [str], file_path: Optional[str] = None, meme_type: Optional[str]="text/plain")`

Bắt đầu một phiên hội thoại mới với mô hình AI, có thể bao gồm tệp ngữ cảnh (chỉ dành cho Colab).

#### `send_message(prompt: str, stream: bool = False)`

Gửi một tin nhắn đến mô hình AI và nhận phản hồi.

#### `generate(prompt: str, stream: bool = True, chunk_size: int = 80)`

Tạo nội dung từ một câu hỏi hoặc yêu cầu, có hỗ trợ stream theo từng phần.

#### `upload() -> str`

Tải tệp lên Google Colab và trả về đường dẫn. Sẽ báo lỗi nếu không chạy trên Colab.

#### `upload_to_gemini(path, mime_type=None)`

Tải tệp lên API Gemini và nhận URI.

#### `history()`

Hiển thị lịch sử hội thoại của phiên hiện tại.

#### `_token_counts()`

Đếm số token đã sử dụng trong toàn bộ lịch sử hội thoại.

## Các Loại MIME Được Hỗ Trợ

Gói này hỗ trợ các loại MIME cho tệp tải lên như sau:

- **Ảnh**: `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `image/heic`, `image/heif`
- **Âm thanh**: `audio/wav`, `audio/mp3`, `audio/aiff`, `audio/aac`, `audio/ogg`, `audio/flac`
- **Văn bản**: `text/plain`, `text/html`, `text/css`, `text/javascript`, `application/json`, `text/markdown`

#### Tags

[phân tích dữ liệu](https://vnstocks.com/blog/tag/phan-tich-du-lieu) [tích hợp AI](https://vnstocks.com/blog/tag/tich-hop-ai) [ứng dụng vnstock](https://vnstocks.com/blog/tag/ung-dung-vnstock)

### Thảo luận

Đang tải bình luận...