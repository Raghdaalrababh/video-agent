from __future__ import annotations
import httpx
from typing import Any
from .config import settings

class VideoIndexer:
    """
    Minimal client for Azure AI Video Indexer.
    Flow:
      1) Get an access token using the subscription key (Ocp-Apim-Subscription-Key).
      2) Use the bearer token for subsequent API calls (upload, insights, etc.).
    """

    def __init__(self, account_id: str | None = None, location: str | None = None, api_key: str | None = None):
        self.account_id = account_id or settings.vi_account_id
        self.location = (location or settings.vi_location or "trial").lower()
        self.api_key = api_key or settings.vi_api_key
        if not (self.account_id and self.location and self.api_key):
            raise ValueError("Missing VI_* configuration")
        self.base = f"https://api.videoindexer.ai/{self.location}/Accounts/{self.account_id}"
        self._token: str | None = None

    async def _get_access_token(self, allow_edit: bool = True) -> str:
        params = {"allowEdit": str(allow_edit).lower()}
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        url = f"https://api.videoindexer.ai/auth/{self.location}/Accounts/{self.account_id}/AccessToken"
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.get(url, params=params, headers=headers)
            r.raise_for_status()
            token = r.text.strip('"')  # API returns a JSON string e.g. "eyJhbGciOi..."
            self._token = token
            return token

    async def _auth_headers(self) -> dict[str, str]:
        if not self._token:
            await self._get_access_token()
        return {"Authorization": f"Bearer {self._token}"}

    async def upload_video(self, name: str, video_url: str) -> dict[str, Any]:
        """
        Start indexing a remote video by URL.
        Returns the API response containing the video id.
        """
        params = {"name": name, "privacy": "Private", "videoUrl": video_url}
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{self.base}/Videos", params=params, headers=await self._auth_headers())
            r.raise_for_status()
            return r.json()

    async def get_insights(self, video_id: str) -> dict[str, Any]:
        """
        Fetch insights (includes transcript and key moments) for a given video id.
        """
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.get(f"{self.base}/Videos/{video_id}/Index", headers=await self._auth_headers())
            r.raise_for_status()
            return r.json()
