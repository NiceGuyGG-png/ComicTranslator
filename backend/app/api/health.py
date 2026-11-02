from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "comic-translator-backend",
        "version": "0.1.0",
    }