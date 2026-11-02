# ComicTranslator

Dự án dịch truyện tranh Trung Quốc (ZH) sang Tiếng Việt (VN) sử dụng mô hình AI local, kết hợp **Browser Extension** + **Backend Server**.

## Mục tiêu

- Extension chạy trên trình duyệt để capture/trích xuất panel truyện, gửi request dịch.
- Backend chạy trên server để chạy các model AI: OCR, Translation, Layout analysis, v.v.
- Triển khai dần theo module để team dễ phát triển song song.


## Roadmap triển khai dần

Phase 1: Xác định các thành phần fine-tuning
Phase 2: Fine-tuning 


## KIẾN TRÚC HỆ THỐNG TỔNG THỂ (PIPELINE)

Hệ thống của bạn được vận hành tự động theo mô hình 2 tầng tối ưu:
text
[Trình duyệt máy bạn] --(Gửi văn bản cần dịch qua SSH Tunnel/API)--> [Hệ thống điều phối]
                                                                             |
   +-------------------------------------------------------------------------+
   |
   v (TẦNG 1: PHÂN TÍCH NGỮ CẢNH DÀI)
[Google Colab TPU v5e + 47GB RAM] (Mô hình Qwen2.5-7B hoặc Gemini Pro API)
   |---> Đọc tài liệu lớn, trích xuất sơ đồ nhân vật, tự động sinh Instruction & Glossary.
   |
   v (TẦNG 2: DỊCH THUẬT HARDCORE LOCAL)
[VPS Linux + Card GTX 1650 4GB VRAM] (Mô hình Index-Translate-2B dạng GGUF)
   |---> Nhận văn bản + Bộ hướng dẫn vừa sinh -> Khạc ra bản dịch chuẩn xác -> Trả về trình duyệt.
Hãy thận trọng khi sử dụng mã.

## Tech stack đề xuất

| Component     | Công nghệ                          |
|---------------|------------------------------------|
| Extension     | Manifest V3, TypeScript, Vite      |
| Backend       | Rust		                     |
| AI Models     | LLM local for translate and OCR    |
| Container     | Docker + docker-compose            |
| Queue (sau)   | Redis + Celery / RQ (nếu cần batch)|
 

## 🌐 SSH TUNNEL & EXTENSION

1. Đục đường ống bảo mật
ssh -L 8080:127.0.0.1:8080 user@ip_vps_cua_ban
Hãy thận trọng khi sử dụng mã.
2. Cấu hình trên Extension trình duyệt (Immersive Translate):
	• API URL: http://127.0.9:8387
	• Model: Index-Translate-2B.
	• 

 Logic xac minh ext

1. User bấm nút Login trên Extension -> Mở trang Web Login (HTTPS).
2. Web Login xác thực xong -> Trả Token về cho Extension Background Script.
3. Background Script lưu Token và đảm nhận mọi thao tác fetch() về Backend.
4. Backend luôn luôn phải validate Token và phân quyền (Authorization) chặt chẽ. Đừng bao giờ tin tưởng tuyệt đối vào dữ liệu gửi lên từ client.
















