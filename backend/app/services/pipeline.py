"""
Pipeline xử lý panel: preprocess → OCR → translate.
Hiện tại trả mock data để team có thể test end-to-end sớm.
"""

import time
from typing import Optional

from app.models.schemas import TranslatePanelResponse, TextResult, BoundingBox


async def process_panel(
    image_bytes: bytes,
    source_lang: str = "zh",
    target_lang: str = "vi",
    detect_only: bool = False,
) -> TranslatePanelResponse:
    start = time.perf_counter()

    # TODO: thay bằng OCR thật (PaddleOCR / EasyOCR / ...)
    mock_texts = [
        TextResult(
            box=BoundingBox(x1=10, y1=20, x2=200, y2=60),
            original="你好，世界",
            translated=None if detect_only else "Xin chào, thế giới",
            confidence=0.95,
        ),
        TextResult(
            box=BoundingBox(x1=30, y1=80, x2=180, y2=120),
            original="这是漫画翻译项目",
            translated=None if detect_only else "Đây là dự án dịch truyện tranh",
            confidence=0.92,
        ),
    ]

    elapsed = (time.perf_counter() - start) * 1000

    return TranslatePanelResponse(
        success=True,
        texts=mock_texts,
        processing_time_ms=round(elapsed, 2),
        message="Mock response – thay bằng model thật ở phase sau",
    )