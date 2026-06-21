# collectors/facebook_graph.py
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from collectors.http_client import HttpClient
from collectors.schemas import SocialPost

class FacebookPageCollector:
    """
    Збір постів зі Facebook Page через Graph API.
    Потрібно: access_token + page_id.
    """

    def __init__(self, access_token: str, page_id: str, client: Optional[HttpClient] = None):
        self.token = access_token
        self.page_id = page_id
        self.client = client or HttpClient()

    def fetch_recent_posts(self, limit: int = 25) -> List[SocialPost]:
        url = f"https://graph.facebook.com/v19.0/{self.page_id}/posts"
        params = {
            "access_token": self.token,
            "fields": "id,message,created_time,permalink_url,attachments{media,type,url}",
            "limit": limit,
        }
        data = self.client.get_json(url, params=params)
        items = data.get("data", [])
        posts: List[SocialPost] = []

        for it in items:
            msg = it.get("message") or ""
            link = it.get("permalink_url") or ""
            created = it.get("created_time")
            dt = datetime.fromisoformat(created.replace("Z", "+00:00")) if created else None

            media_url = None
            attachments = (it.get("attachments") or {}).get("data") or []
            if attachments:
                att0 = attachments[0]
                media = att0.get("media") or {}
                image = media.get("image") or {}
                media_url = image.get("src")  # може бути None

            posts.append(
                SocialPost(
                    source="facebook",
                    post_id=str(it.get("id", "")),
                    permalink=link,
                    text=msg,
                    media_url=media_url,
                    created_time=dt,
                )
            )
        return posts
