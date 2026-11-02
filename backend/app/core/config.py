from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "ComicTranslator"
    env: str = "development"
    debug: bool = True

    # Model
    model_device: str = "cpu"  # cpu | cuda
    ocr_model: str = "paddleocr"  # placeholder
    translation_model: str = "nllb"  # placeholder

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()