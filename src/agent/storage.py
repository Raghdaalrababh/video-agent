from __future__ import annotations
from azure.storage.blob import BlobServiceClient
from pathlib import Path
from .config import settings

class BlobClient:
    def __init__(self, conn_str: str | None = None):
        conn = conn_str or settings.storage_conn
        if not conn:
            raise ValueError("Missing AZURE_STORAGE_CONNECTION_STRING")
        self._svc = BlobServiceClient.from_connection_string(conn)

    def upload_file(self, container: str, local_path: str, blob_name: str | None = None) -> str:
        p = Path(local_path)
        name = blob_name or p.name
        self._svc.get_container_client(container).upload_blob(name, p.read_bytes(), overwrite=True)
        return f"https://{self._svc.account_name}.blob.core.windows.net/{container}/{name}"
