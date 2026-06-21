# pipeline/run_collectors.py
import os
import django
from dotenv import load_dotenv

from collectors.http_client import HttpClient
from collectors.instagram_graph import InstagramGraphCollector
from collectors.facebook_graph import FacebookPageCollector
from storage.media_store import save_image_bytes

load_dotenv()

# 1) Підняти Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # змініть на ваш settings module
django.setup()

from catalog.models import Imagess  # змініть на ваш застосунок/модель

def short_title(text: str, max_len: int = 80) -> str:
    t = (text or "").strip().replace("\n", " ")
    return t[:max_len] if t else "Соцмережі: без опису"

def run_import():
    client = HttpClient()

    ig_token = os.getenv("IG_TOKEN", "")
    ig_user_id = os.getenv("IG_USER_ID", "")
    fb_token = os.getenv("FB_TOKEN", "")
    fb_page_id = os.getenv("FB_PAGE_ID", "")

    media_root = os.getenv("MEDIA_ROOT", "media")  # або підхопіть з Django settings.MEDIA_ROOT

    posts = []

    if ig_token and ig_user_id:
        ig = InstagramGraphCollector(ig_token, ig_user_id, client=client)
        posts += ig.fetch_recent_media(limit=20)

    if fb_token and fb_page_id:
        fb = FacebookPageCollector(fb_token, fb_page_id, client=client)
        posts += fb.fetch_recent_posts(limit=20)

    for p in posts:
        if not p.media_url:
            continue

        # 2) Скачати медіа
        content = client.download_file(p.media_url)

        # 3) Зберегти файл
        rel_path = save_image_bytes(media_root=media_root, content=content, ext="jpg")

        # 4) Записати у «Сольчик»
        obj = Imagess()
        obj.title = short_title(p.text)  # у вас це поле є
        # ВАЖЛИВО: для ImageField треба присвоювати відносний шлях або File
        obj.cover.name = rel_path
        obj.save()

if __name__ == "__main__":
    run_import()
