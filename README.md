# ComicTranslator

Dự án dịch truyện tranh Trung Quốc (ZH) sang Tiếng Việt (VN) sử dụng mô hình AI local, kết hợp **Browser Extension** + **Backend Server**.

## Mục tiêu

- Extension chạy trên trình duyệt để capture/trích xuất panel truyện, gửi request dịch.
- Backend chạy trên server để chạy các model AI: OCR, Translation, Layout analysis, v.v.
- Triển khai dần theo module để team dễ phát triển song song.


## Roadmap triển khai dần

Phase 1: Xác định các thành phần fine-tuning
Phase 2: Fine-tuning 
## Chạy local nhanh
```

## Tech stack đề xuất

| Component     | Công nghệ                          |
|---------------|------------------------------------|
| Extension     | Manifest V3, TypeScript, Vite      |
| Backend       | FastAPI, Python 3.11+              |
| AI Models     | LLM local for translate and OCR    |
| Container     | Docker + docker-compose            |
| Queue (sau)   | Redis + Celery / RQ (nếu cần batch)|

---
