# Kiến trúc ComicTranslator

## Tổng quan

```
[Browser] ←→ [Extension] ←→ HTTP/WS ←→ [Backend Server] ←→ [AI Models]
                                      ↑
                               (OCR / Translate / Layout)
```

## Luồng chính

1. User mở trang truyện (manhua/manhwa).
2. Extension content script detect panels / bubbles.
3. User chọn vùng hoặc auto-detect → gửi image + metadata lên Backend.
4. Backend:
   - Preprocess image
   - OCR (detect text + bounding boxes)
   - Translate (ZH → VN)
   - (Optional) Inpainting / re-render text
5. Trả kết quả về Extension để overlay lên trang.

## Module Backend (đề xuất)

| Service              | Trách nhiệm                              | Ưu tiên |
|----------------------|------------------------------------------|---------|
| `ocr_service`        | Detect text + boxes                      | P0      |
| `translation_service`| Dịch text ZH → VN                        | P0      |
| `layout_service`     | Phân tích panel / bubble                 | P1      |
| `render_service`     | Ghép text dịch lên ảnh (optional)        | P2      |
| `job_service`        | Quản lý queue / batch job                | P2      |

## API Contract (skeleton)

```
POST /api/v1/translate/panel
  - body: multipart (image) + json (source_lang, target_lang, options)
  - response: { texts: [{box, original, translated}], image_url? }

POST /api/v1/translate/batch
GET  /api/v1/jobs/{job_id}
GET  /health
```

## Triển khai dần cho team

- **Dev A**: Extension (UI + capture)
- **Dev B**: Backend API skeleton + OCR
- **Dev C**: Translation model + pipeline
- **Dev D**: Docker, CI, monitoring

Mỗi người chỉ cần quan tâm module của mình + contract API.