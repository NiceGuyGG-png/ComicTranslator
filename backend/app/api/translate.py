from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from typing import Optional

from app.models.schemas import TranslatePanelResponse, TextResult
from app.services.pipeline import process_panel

router = APIRouter()


@router.post("/translate/panel", response_model=TranslatePanelResponse)
async def translate_panel(
    image: UploadFile = File(...),
    source_lang: str = Form("zh"),
    target_lang: str = Form("vi"),
    detect_only: bool = Form(False),
):
    """
    Nhận 1 panel/ảnh → OCR + dịch.
    Hiện tại là skeleton, sẽ gắn model thật sau.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    content = await image.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty image")

    result = await process_panel(
        image_bytes=content,
        source_lang=source_lang,
        target_lang=target_lang,
        detect_only=detect_only,
    )
    return result


@router.post("/translate/batch")
async def translate_batch():
    """Placeholder cho batch job sau này."""
    return {"message": "Batch endpoint chưa implement", "status": "todo"}