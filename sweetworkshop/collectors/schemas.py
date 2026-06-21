# collectors/schemas.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SocialPost:
    source: str                  # "instagram" | "facebook"
    post_id: str
    permalink: str
    text: str
    media_url: Optional[str]
    created_time: Optional[datetime]
    author: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
