from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, translate

app = FastAPI(
    title="ComicTranslator API",
    description="Backend cho dịch truyện tranh ZH → VN bằng AI local",
    version="0.1.0",
)

# CORS cho extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Siết lại khi production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(translate.router, prefix="/api/v1", tags=["translate"])


@app.get("/")
async def root():
    return {"message": "ComicTranslator Backend is running"}