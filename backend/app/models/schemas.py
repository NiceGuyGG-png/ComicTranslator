from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class TextResult(BaseModel):
    box: BoundingBox
    original: str
    translated: Optional[str] = None
    confidence: Optional[float] = None


class TranslatePanelResponse(BaseModel):
    success: bool = True
    texts: List[TextResult] = Field(default_factory=list)
    processing_time_ms: Optional[float] = None
    message: Optional[str] = None