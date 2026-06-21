# storage/media_store.py
import os
import uuid

def save_image_bytes(media_root: str, content: bytes, ext: str = "jpg") -> str:
    """
    Зберігає байти зображення у MEDIA_ROOT і повертає відносний шлях (для ImageField).
    """
    os.makedirs(media_root, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{ext}"
    rel_path = os.path.join("social", filename)
    abs_path = os.path.join(media_root, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    with open(abs_path, "wb") as f:
        f.write(content)

    return rel_path
