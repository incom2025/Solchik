# collectors/instagram_graph.py
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from collectors.http_client import HttpClient
from collectors.schemas import SocialPost

class InstagramGraphCollector:
    """
    Збір медіа з Instagram Business/Creator через Graph API.
    Потрібно: access_token + ig_user_id (Instagram User ID).
    """

    def __init__(self, access_token: str, ig_user_id: str, client: Optional[HttpClient] = None):
        self.token = access_token
        self.ig_user_id = ig_user_id
        self.client = client or HttpClient()

    def fetch_recent_media(self, limit: int = 25) -> List[SocialPost]:
        url = f"https://graph.facebook.com/v19.0/{self.ig_user_id}/media"
        params = {
            "access_token": self.token,
            "fields": "id,caption,media_url,permalink,timestamp,media_type,username",
            "limit": limit,
        }
        data = self.client.get_json(url, params=params)
        items = data.get("data", [])
        posts: List[SocialPost] = []

        for it in items:
            # фільтрація: беремо фото (IMAGE) або thumbnail для відео
            media_type = it.get("media_type")
            media_url = it.get("media_url")
            if media_type not in ("IMAGE", "CAROUSEL_ALBUM", "VIDEO"):
                continue

            ts = it.get("timestamp")
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None

            posts.append(
                SocialPost(
                    source="instagram",
                    post_id=str(it.get("id", "")),
                    permalink=it.get("permalink") or "",
                    text=it.get("caption") or "",
                    media_url=media_url,
                    created_time=dt,
                    author=it.get("username"),
                )
            )
        return posts
