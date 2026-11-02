# ComicTranslator

Dự án dịch truyện tranh Trung Quốc (ZH) sang Tiếng Việt (VN) sử dụng mô hình AI local, kết hợp **Browser Extension** + **Backend Server**.

## Mục tiêu

- Extension chạy trên trình duyệt để capture/trích xuất panel truyện, gửi request dịch.
- Backend chạy trên server để chạy các model AI: OCR, Translation, Layout analysis, v.v.
- Triển khai dần theo module để team dễ phát triển song song.

## Cấu trúc thư mục

```
ComicTranslator/
├── docs/                    # Tài liệu kiến trúc, API, hướng dẫn
├── extension/               # Browser Extension (Chrome/Edge/Firefox)
│   ├── public/
│   ├── src/
│   │   ├── background/      # Service worker
│   │   ├── content/         # Content scripts
│   │   ├── popup/           # UI popup
│   │   └── utils/
│   ├── manifest.json
│   └── package.json
├── backend/                 # FastAPI / Python server chạy AI models
│   ├── app/
│   │   ├── api/             # Routes
│   │   ├── core/            # Config, security
│   │   ├── models/          # Pydantic schemas
│   │   ├── services/        # Business logic + AI inference
│   │   └── utils/
│   ├── scripts/             # Download model, migrate, etc.
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
├── shared/                  # Shared constants / types (nếu cần)
├── docker-compose.yml
└── .gitignore
```

## Roadmap triển khai dần

1. **Phase 1** – Skeleton + API contract
2. **Phase 2** – Extension: capture panel + gửi request
3. **Phase 3** – Backend: OCR + Translation pipeline
4. **Phase 4** – Tối ưu model, batch, caching
5. **Phase 5** – Auth, rate limit, monitoring

## Chạy local nhanh

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Extension
cd extension
npm install
npm run build   # hoặc load unpacked trong chrome://extensions
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

Team có thể bắt đầu từ bất kỳ module nào. Hãy đọc `docs/architecture.md` trước khi code.
