from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings

_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _ROOT_DIR / ".env"


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Style Transfer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./style_transfer.db"

    # JWT
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload
    UPLOAD_DIR: str = "uploads"
    RESULT_DIR: str = "results"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".webp"}

    # CORS 配置（逗号分隔的来源白名单；"*" 表示允许全部，仅开发环境推荐）
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000"

    # Stability AI
    STABILITY_API_KEY: str = ""
    AI_TIMEOUT_SECONDS: int = 60
    USE_MOCK_AI: bool = True

    # 文件清理（TTL，单位：小时；0 表示不清理）
    FILE_TTL_HOURS: int = 72

    # 图片处理
    MAX_IMAGE_DIMENSION: int = 2048  # 最大边长（像素），超过将等比缩放
    JPEG_QUALITY: int = 85  # JPEG 保存质量

    # 风格转换强度（仅真实 API 模式使用，0=保留原图，1=完全新图）
    STYLE_STRENGTH: float = 0.7

    model_config = {
        "env_file": str(_ENV_FILE),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES", mode="before")
    @classmethod
    def ensure_int(cls, v):
        try:
            return int(v)
        except (ValueError, TypeError):
            return 30

    @property
    def cors_origins_list(self) -> List[str]:
        """解析 CORS_ORIGINS 为列表"""
        if not self.CORS_ORIGINS or self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def stability_api_base_url(self) -> str:
        """Stability AI v2beta 图生图端点"""
        return "https://api.stability.ai/v2beta/stable-image/generate/sd3"


settings = Settings()
