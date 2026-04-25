---
url: "https://vnstocks.com/docs/vnstock/bieu-dien-du-lieu"
title: "Biểu diễn dữ liệu trực quan | Vnstock"
---

Toggle Sidebar

### Mục lục

Giới thiệu

Vnstock cung cấp khả năng biểu diễn dữ liệu trực quan giúp bạn khám phá nhanh đặc tính của dữ liệu cho bất kỳ DataFrame, Series được trả về. Các loại đồ thị được giới thiệu trong gói thư viện [vnstock\_ezchart](https://github.com/vnstock-hq/vnstock_ezchart) nay được tích hợp trực tiếp vào Vnstock giúp bạn sử dụng thuận tiện chỉ với 1 câu lệnh đơn giản vẫn cho ra biểu đồ đẹp mắt và sẵn sàng để chia sẻ.

## Sử dụng đơn giản

### Notebook minh hoạ

Bạn có thể truy cập ngay Notebook minh hoạ tính năng tại đây.

[Notebook minh hoạ](https://colab.research.google.com/github/thinh-vu/vnstock/blob/main/docs/5_visualization_data_exploration_vnstock.ipynb)

### Truy cập tính năng

Từ DataFrame, Series trả về bởi Vnstock3, bạn có thể truy cập lớp (class) hàm biểu diễn dữ liệu dưới dạng thuộc tính `.viz.gọi_tên_hàm()`. Ví dụ, cú pháp vẽ đồ thị `timeseries` cho cột `close` trong DataFrame có tên `df` như sau:

Python

```python
df.viz.timeseries()
```

Kết quả trả về như hình bên dưới. Bạn có thể tinh chỉnh biểu đồ với các tham số được cung cấp để nhanh chóng tạo ra biểu đồ vừa đơn giản nhưng cũng đầy chuyên nghiệp để có thể chia sẻ dễ dàng.:

![Blog image](https://vnstocks.com/images/timeseries_vnstock_ezchart.png)

### Xem trợ giúp nhanh chóng

Gợi ý

Bạn có thể xem hướng dẫn cho từng loại biểu đồ một cách chi tiết bằng cách gọi hàm `help()` theo sau lớp hàm `.viz`. Ví dụ, từ DataFrame, Series bất kỳ, ví dụ gọi hàm `df.viz.help('timeseries')` trên DataFrame có tên `df` sẽ trả về hướng dẫn chi tiết sử dụng hàm biểu diễn dữ liệu `timeseries`.

**Hướng dẫn hàm timeseries**

```
Biểu diễn dữ liệu theo thời gian (timeseries). Dữ liệu cần có cột index là kiểu dữ liệu datetime.

Tham số:
  - data (pd.DataFrame hoặc pd.Series): Dữ liệu đầu vào dạng DataFrame hoặc Series.
  - title (str): Tiêu đề của biểu đồ.
  - title_fontsize (int): Cỡ chữ cho tiêu đề.
  - xlabel (str): Nhãn cho trục X.
  - ylabel (str): Nhãn cho trục Y.
  - color_palette (str): Tên của bảng màu đã được định trước hoặc danh sách các màu tùy chỉnh. Mặc định là 'vnstock'. Các bảng màu có sẵn: 'percentage', 'amount', 'category', 'trend', 'flatui', 'vnstock', 'learn_anything'. Có thể liệt kê tất cả bảng màu với Utils.brand_palettes.keys().
  - palette_shuffle (bool): Xáo trộn thứ tự màu sắc trong bảng màu, cho phép chọn màu ngẫu nhiên trong bảng màu để biểu diễn cho đến khi bạn ưng ý. Mặc định là False.
  - grid (bool): Hiển thị lưới. Nhận True để hiện thị hoặc False để ẩn lưới.
  - data_labels (bool): Hiển thị nhãn dữ liệu trên biểu đồ.
  - data_label_format (str): Định dạng cho nhãn dữ liệu. Nhận các giá trị rút gọn như 1K, 1M, 1B, 1T tương ứng với 1 ngàn, 1 triệu, 1 tỷ, 1 nghìn tỷ.
  - label_fontsize (int): Cỡ chữ cho nhãn trục X và Y.
  - legend_title (str): Tiêu đề cho chú giải.
  - show_legend (bool): Hiển thị chú giải. Nhận True để hiển thị hoặc False để ẩn chú giải.
  - series_names (list): Danh sách tên cho các dải (series) dữ liệu trong biểu đồ. Nhận giá trị là 1 danh sách (list).
  - font_name (str): Tên của font chữ muốn áp dụng.
  - figsize (tuple): Kích thước của biểu đồ, ví dụ (10, 6).
  - show_xaxis (bool): Hiển thị trục X. Nhận True để hiển thị hoặc False để ẩn trục X.
  - show_yaxis (bool): Hiển thị trục Y. Nhận True để hiển thị hoặc False để ẩn trục Y.
  - tick_labelsize (int): Cỡ chữ cho các nhãn trục.
  - xtick_format (str): Định dạng cho nhãn trục X. Ví dụ định dạng số thập phân '{:.0f}'.
  - ytick_format (str): Định dạng cho nhãn trục Y. Ví dụ định dạng phần trăm '{:.0%}'.
  - tick_rotation (int): Góc quay cho các nhãn trục.
  - xlim (tuple): Giới hạn cho trục X, ví dụ (0, 100).
  - ylim (tuple): Giới hạn cho trục Y, ví dụ (0, 100).
  - background_color (str): Màu nền cho biểu đồ.
  - bar_edge_color (str): Màu viền cho các cột (bar) trong biểu đồ.
```

## Biểu diễn xu hướng

### Timeseries

Python

```python
df['close'].viz.timeseries(figsize=(10, 6),
		title='Giá đóng cửa - Hợp đồng tương lai VN30F1M',
		ylabel='Giá',
		xlabel='Thời gian',
		color_palette='vnstock',
		palette_shuffle=True)
```

Trong đó là `df` là DataFrame dữ liệu mẫu giá cổ phiếu được gọi từ mục [Thống kê giá lịch sử](https://vnstocks.com/docs/vnstock/thong-ke-gia-lich-su).

![Blog image](https://vnstocks.com/images/gia-dong-cua-hop-dong-tuong-lai-vn30-timeseries_vnstock_ezchart.png)

### Combo chart

Python

```python
df.viz.combo(bar_data='volume',
             line_data='close',
             title='Giá đóng cửa và khối lượng giao dịch - Hợp đồng tương lai VN30F1M',
             left_ylabel='Volume (M)', right_ylabel='Price (K)',
             figsize=(10, 6),
             color_palette='stock',
             palette_shuffle=True)
```

![Blog image](https://vnstocks.com/images/combo_chart_gia_khoi_luong_vnstock_ezchart.png)

## Biểu diễn số lượng

### Barplot

Python

```python
income_df[['LN trước thuế', 'Lợi nhuận thuần']].div(1000_000_000)\
    .viz.bar(figsize=(10, 6),
             title='VCI - Lợi nhuận trước thuế & lợi nhuận thuần (tỷ đồng)',
             ylabel='Lợi nhuận (tỷ đồng)',
             xlabel='Năm',
             color_palette='stock',
             data_labels=True, # Hiển thị giá trị trên cột
             show_legend=True,
             rot=45) # Xoay nhãn trục x 45 độ
```

![Blog image](https://vnstocks.com/images/barplot_visualize_amount_vnstock_ezchart.png)

### Heatmap

Python

```python
import pandas as pd
return_pivot = pd.pivot_table(df, index=df.index.year, columns=df.index.month, values='returns', aggfunc='mean')
cmap = df.viz.create_cmap('percentage') # Tạo colormap bằng 1 bảng màu có trong vnstock_ezchart
return_pivot.viz.heatmap(figsize=(10, 6),
                         title='VN30F1M - Thống kê lợi nhuận trung bình theo ngày qua các tháng trong năm (%)',
                         annot=True,
                         cmap=cmap)
```

![Blog image](https://vnstocks.com/images/returns_heatmap_vnstock_ezchart.png)

### Table

Trong nhiều trường hợp, bạn cần trình bày dữ liệu chi tiết dứoi dạng bảng bằng để có thể tiện copy và chia sẻ hoặc chèn hình ảnh thương hiệu cá nhân, loại biểu diễn dữ liệu này dành cho bạn.

Python

```python
df.reset_index().iloc[:10, :5]\
    .viz.table(figsize=(10, 10),
               title='10 dòng đầu tiên của dữ liệu',
               title_loc='center')
```

![Blog image](https://vnstocks.com/images/table_bang_du_lieu_vnstock_ezchart.png)

## Biểu diễn phân phối

### Histogram

Python

```python
df['returns'].viz.hist(bins=20,
                       figsize=(10, 6),
                       title='VN30F1M - Phân phối lợi nhuận ngày (%)',
                       xlabel='Lợi nhuận (%)',
                       ylabel='Tần suất',
                       color_palette='stock')
```

![Blog image](https://vnstocks.com/images/Pasted%20image%2020240603004429.png)

### Boxplot

Python

```python
# Mở help cho biểu đồ boxplot để xem tất cả các tuỳ chọn
df.volume.div(1000_000)\
    .viz.boxplot(
        title='Phân phối khối lượng giao dịch của VN30F1M',
        xlabel='',
        ylabel='KLGD (Triệu CP)',
        color_palette='stock',
        palette_shuffle=True,
        figsize=(10, 6))
```

![Blog image](https://vnstocks.com/images/boxplot_vnstock_chart.png)

### Word Cloud

Python

```python
profile_df.viz.wordcloud(figsize=(10, 6),
                         title='VCB - Mô tả công ty',
                         max_words=50,
                         color_palette='stock')
```

![Blog image](https://vnstocks.com/images/wordcloud_vnstock_ezchart.png)

## Biểu diễn tỉ lệ

### Pie

Python

```python
shareholders_df.viz.pie(title='Cổ đông lớn VNM',
                                             labels='share_holder',
                                             values='share_own_percent',
                                             figsize=(10, 6),
                                             ylabel='',
                                             color_palette='stock')
```

![Blog image](https://vnstocks.com/images/Pasted%20image%2020240603004946.png)

### Treemap

Python

```python
shareholders_df.viz.treemap(title='Cổ đông lớn VNM',
                            labels='share_holder',
                            values='share_own_percent',
                            figsize=(10, 6),
                            color_palette='stock')
```

![Blog image](https://vnstocks.com/images/Pasted%20image%2020240603005015.png)

## Biểu diễn tương quan

### Scatter plot

Python

```python
df.viz.scatter(x='close', y='volume',
               title='VN30F1M - Tương quan giá đóng cửa và khối lượng giao dịch',
               xlabel='Giá đóng cửa',
               ylabel='Khối lượng giao dịch',
               figsize=(10, 6),
               color_palette='stock')
```

![Blog image](https://vnstocks.com/images/Pasted%20image%2020240603005228.png)

### Pairplot

Python

```python
df.viz.pairplot()
```

![Blog image](https://vnstocks.com/images/Pasted%20image%2020240603005309.png)

#### Tags

[biểu diễn dữ liệu](https://vnstocks.com/blog/tag/bieu-dien-du-lieu) [dữ liệu trực quan](https://vnstocks.com/blog/tag/du-lieu-truc-quan) [vẽ chart](https://vnstocks.com/blog/tag/ve-chart)

### Thảo luận

Chưa có bình luận. Hãy là người đầu tiên!

Vui lòng đăng nhập bằng Google để thảo luận.

Đăng nhập