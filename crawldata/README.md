# HƯỚNG DẪN CÀO DỮ LIỆU CELLPHONES

> Bộ script tự động thu thập dữ liệu sản phẩm, chính sách, FAQ từ website CellphoneS phục vụ cho chatbot.

---

## Mục đích

-   Tự động hóa việc thu thập dữ liệu sản phẩm, chính sách, câu hỏi thường gặp từ website [CellphoneS](https://cellphones.com.vn/).
-   Chuẩn hóa dữ liệu đầu vào cho hệ thống chatbot CellphoneS.

---

## Cấu trúc thư mục

```
crawldata/
├── crawl_description.py         # Cào mô tả sản phẩm
├── crawl_faq.py                 # Cào câu hỏi thường gặp (FAQ)
├── crawl_name_and_url.py        # Cào tên và đường dẫn sản phẩm
├── crawl_policy.py              # Cào chính sách bán hàng, bảo hành,...
├── crawl_spec_and_variant.py    # Cào thông số kỹ thuật và các phiên bản sản phẩm
├── README.md                    # Tài liệu hướng dẫn sử dụng bộ script
```

---

## Yêu cầu môi trường

-   **Python** >= 3.8
-   **Chrome** và **ChromeDriver** phù hợp với phiên bản Chrome
-   Khuyến nghị sử dụng môi trường ảo: `conda` hoặc `venv`

---

## Cài đặt phụ thuộc

```bash
pip install -r ../requirements.txt
```

---

## Hướng dẫn sử dụng script

Thực hiện tuần tự các bước sau để thu thập đầy đủ dữ liệu:

### 1. Cào tên và URL sản phẩm

```python
python crawl_name_and_url.py
```

> Tạo file [`product_details.json`](#product_detailsjson) chứa danh sách sản phẩm.

---

### 2. Cào thông số kỹ thuật và biến thể sản phẩm

```python
python crawl_spec_and_variant.py
```

> Cập nhật thêm thông số và biến thể vào [`product_details.json`](#product_detailsjson).

---

### 3. Cào mô tả sản phẩm

```python
python crawl_description.py
```

> Thêm trường mô tả vào [`product_details.json`](#product_detailsjson).

---

### 4. Cào các câu hỏi thường gặp (FAQ)

```python
python crawl_faq.py
```

> Tạo file [`faq.json`](#faqjson) chứa danh sách câu hỏi và trả lời.

---

### 5. Cào chính sách, điều khoản

```python
python crawl_policy.py
```

> Tạo file [`policy_dataset.json`](#policy_datasetjson) chứa các chính sách và điều khoản.

---

## Ý nghĩa các trường dữ liệu đầu ra

### `product_details.json`

| Trường        | Ý nghĩa                                                |
| ------------- | ------------------------------------------------------ |
| `id`          | Mã định danh sản phẩm (chuỗi, lấy từ URL)              |
| `name`        | Tên sản phẩm                                           |
| `url`         | Đường dẫn chi tiết sản phẩm                            |
| `specs`       | Thông số kỹ thuật, dạng dict `{tên_thông_số: giá_trị}` |
| `variants`    | Danh sách biến thể màu sắc và giá tiền                 |
| `description` | Mô tả ngắn về sản phẩm                                 |

**Ví dụ trường `variants`:**

```json
[
    { "color": "Đen", "price": "20.990.000₫" },
    { "color": "Trắng", "price": "21.990.000₫" }
]
```

---

### `faq.json`

| Trường     | Ý nghĩa                |
| ---------- | ---------------------- |
| `question` | Câu hỏi của khách hàng |
| `answer`   | Câu trả lời tương ứng  |

---

### `policy_dataset.json`

| Trường     | Ý nghĩa                                    |
| ---------- | ------------------------------------------ |
| `category` | Nhóm chính sách (VD: Bảo hành, Đổi trả...) |
| `title`    | Tiêu đề mục chính sách                     |
| `content`  | Nội dung chi tiết của mục chính sách       |

---

## Lưu ý khi sử dụng

-   Các script sử dụng Selenium, cần đảm bảo ChromeDriver đã được cài đặt và nằm trong PATH.
-   Nên chạy từng script theo thứ tự để đảm bảo dữ liệu đầu vào đầy đủ.
-   Nếu gặp lỗi, kiểm tra lại phiên bản ChromeDriver và các thư viện đã cài đặt.
-   Dữ liệu chỉ dùng cho mục đích demo/học tập, không sử dụng cho sản phẩm thương mại.

---

## Tài liệu liên quan

-   [README tổng thể dự án](../README.md)
-   [CellphoneS](https://cellphones.com.vn/)
-   [Selenium](https://www.selenium.dev/)

---

## Liên hệ

Nếu có vấn đề khi chạy script, vui lòng liên hệ nhóm phát triển để được hỗ trợ qua email: **phuctranhuu37@gmail.com**

---
