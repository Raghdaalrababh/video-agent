from __future__ import annotations
import os
from pydantic import BaseModel
from dotenv import load_dotenv

# تحميل القيم من ملف .env
load_dotenv()

class Settings(BaseModel):
    # Azure Storage
    storage_conn: str | None = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    # Azure OpenAI
    aoai_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    aoai_key: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    aoai_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    # Video Indexer
    vi_account_id: str | None = os.getenv("VI_ACCOUNT_ID")
    vi_location: str | None = os.getenv("VI_LOCATION")
    vi_api_key: str | None = os.getenv("VI_API_KEY")

# إنشاء نسخة من الإعدادات لاستخدامها في باقي الملفات
settings = Settings()
