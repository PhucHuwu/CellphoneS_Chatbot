# CellphoneS Chatbot

<p align="center">
    <img src="CellphoneSChatbot.png" alt="CellphoneS Chatbot" width="350">
</p>

## Mục tiêu dự án

-   Xây dựng hệ thống chatbot AI hỗ trợ khách hàng CellphoneS tra cứu thông tin sản phẩm, chính sách, và giải đáp thắc mắc nhanh chóng, chính xác.
-   Ứng dụng công nghệ LLM kết hợp RAG để tăng độ tin cậy và tính thực tiễn của câu trả lời.
-   Tối ưu trải nghiệm người dùng với giao diện web hiện đại, dễ sử dụng trên mọi thiết bị.

## Công nghệ sử dụng

-   **Python 3.10+**: Ngôn ngữ lập trình chính.
-   **Flask**: Xây dựng REST API backend.
-   **Sentence Transformers**: Sinh embedding cho dữ liệu đa ngôn ngữ.
-   **FAISS**: Lưu trữ và tìm kiếm embedding hiệu quả, tốc độ cao.
-   **Groq API (Meta Llama-4 Scout 17B)**: Large Language Model cho sinh câu trả lời tự động.
-   **Selenium**: Cào dữ liệu sản phẩm, chính sách, FAQ từ website CellphoneS.
-   **HTML/CSS/JS**: Xây dựng giao diện web responsive, hỗ trợ markdown, quick actions.
-   **scikit-learn**: Chuẩn hóa embedding.
-   **pickle**: Lưu trữ metadata và dữ liệu embedding.
-   **CORS**: Hỗ trợ frontend giao tiếp với backend.

## Kiến trúc hệ thống

```
+-------------------+      +-------------------+      +-------------------+
|   Frontend (Web)  | <--> |   Flask Backend   | <--> |   LLM + FAISS RAG |
+-------------------+      +-------------------+      +-------------------+
```

-   **Frontend**: Giao diện chat trực quan, hiển thị lịch sử hội thoại, quick actions, markdown formatting, trạng thái bot, và hỗ trợ đa nền tảng.
-   **Backend**: Nhận câu hỏi từ người dùng, truy vấn dữ liệu liên quan, sinh câu trả lời qua LLM, trả về kết quả cho frontend.
-   **RAG Pipeline**: Tìm kiếm thông tin liên quan từ dữ liệu cào, cung cấp cho LLM để sinh câu trả lời chính xác, có dẫn nguồn.

## Các module chính

-   `app.py`: Khởi tạo Flask server, định nghĩa các endpoint API.
-   `rag_pipeline.py`: Pipeline RAG, gồm các bước tìm kiếm, sinh câu trả lời, và quản lý chỉ mục FAISS.
-   `utils/chunking.py`: Xử lý dữ liệu đầu vào, chia nhỏ thành các đoạn thông tin dễ truy vấn.
-   `utils/embedding.py`: Sinh embedding cho văn bản sử dụng Sentence Transformers.
-   `data_crawler/`: Chứa các script Selenium để cào dữ liệu từ website CellphoneS.
-   `embeddings/`: Lưu trữ FAISS index và metadata cho truy vấn nhanh.
-   `frontend/`: Giao diện web, gồm HTML, CSS, JS.

## Quy trình cào dữ liệu

-   Sử dụng **Selenium** để tự động thu thập dữ liệu sản phẩm, chính sách, FAQ từ website CellphoneS.
-   Dữ liệu được lưu dưới dạng JSON: `product_details.json`, `policy_dataset.json`, `faq.json`.
-   Các module chunking xử lý dữ liệu thành các đoạn nhỏ, dễ truy vấn và sinh embedding.

## Pipeline RAG

1.  **Tiền xử lý dữ liệu**: Cào và chuẩn hóa dữ liệu, chunk thành các đoạn ngắn.
2.  **Embedding**: Sử dụng Sentence Transformers để chuyển đổi văn bản thành vector embedding.
3.  **Lập chỉ mục FAISS**: Lưu trữ embedding, hỗ trợ tìm kiếm nhanh.
4.  **Truy vấn**: Khi người dùng gửi câu hỏi, hệ thống tìm kiếm các đoạn thông tin liên quan nhất.
5.  **Sinh câu trả lời**: LLM (Meta Llama-4 Scout 17B qua Groq API) nhận thông tin liên quan và sinh câu trả lời tiếng Việt, rõ ràng, có dẫn nguồn.

## Hướng dẫn cài đặt

### 1. Chuẩn bị môi trường

Khuyến nghị sử dụng môi trường ảo (conda):

```bash
conda create -n cps-chatbot python=3.10.16
conda activate cps-chatbot
```

### 2. Cài đặt phụ thuộc

```bash
pip install -r requirements.txt
```

### 3. Cào dữ liệu (tuỳ chọn)

Chạy script Selenium để cào dữ liệu sản phẩm, chính sách, FAQ từ website CellphoneS. (Xem hướng dẫn trong thư mục `data_crawler/`)

### 4. Khởi tạo chỉ mục FAISS

Chạy server lần đầu sẽ tự động build FAISS index từ dữ liệu đã cào.

### 5. Chạy server

```bash
python app.py
```

Server sẽ chạy tại `http://localhost:8000`.

### 6. Truy cập giao diện web

Mở file `frontend/index.html` bằng trình duyệt để sử dụng chatbot.

## Hướng dẫn sử dụng API

-   `POST /chat`
    -   **Body:** `{ "query": "Câu hỏi của bạn" }`
    -   **Trả về:** `{ "query": "...", "contexts": [...], "answer": "..." }`
-   `GET /ping`
    -   Kiểm tra trạng thái server.

## Bảo mật & lưu ý triển khai

-   **API Key Groq**: Đảm bảo bảo mật file `apikey.py`, không public lên repository.
-   **CORS**: Đã cấu hình cho phép frontend truy cập backend.
-   **Dữ liệu cào**: Chỉ sử dụng cho mục đích demo/học tập, không dùng cho sản phẩm thương mại.
-   **Kiểm thử**: Đã kiểm thử với các trường hợp phổ biến, khuyến nghị kiểm thử thêm khi mở rộng dữ liệu.

## Kiểm thử & gỡ lỗi

-   Kiểm tra log server khi gặp lỗi sinh câu trả lời hoặc truy vấn dữ liệu.
-   Đảm bảo các file dữ liệu JSON và embedding đã được tạo đúng định dạng.
-   Sử dụng endpoint `/ping` để xác nhận server hoạt động.

## Tài liệu tham khảo

-   [Sentence Transformers](https://www.sbert.net/)
-   [FAISS](https://github.com/facebookresearch/faiss)
-   [Groq API](https://groq.com/)
-   [Selenium](https://www.selenium.dev/)
-   [CellphoneS](https://cellphones.com.vn/)

## Đóng góp & phát triển

-   Tuân thủ PEP 8, code rõ ràng, có docstring và comment đầy đủ.
-   Quản lý phụ thuộc qua `requirements.txt`.
-   Mọi đóng góp vui lòng tạo pull request hoặc liên hệ qua email.

## Liên hệ

-   **Trần Hữu Phúc**
-   Email: phuctranhuu37@gmail.com

---

> Dự án này chỉ phục vụ mục đích demo nội bộ, không dùng cho sản phẩm thương mại.
