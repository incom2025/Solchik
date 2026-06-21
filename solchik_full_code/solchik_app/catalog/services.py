import requests
from django.conf import settings

POSITIVE_WORDS = {'смачно', 'чудово', 'ідеально', 'ніжно', 'супер', 'красиво', 'рекомендую', 'якісно'}
NEGATIVE_WORDS = {'несмачно', 'погано', 'жахливо', 'дорого', 'сухо', 'неякісно', 'не рекомендую'}

TAG_RULES = {
    'bento': ['бенто', 'bento'],
    'cake': ['торт', 'cake'],
    'cupcake': ['капкейк', 'cupcake'],
    'macaron': ['макарон', 'macaron'],
    'wedding': ['весіль', 'wedding'],
    'chocolate': ['шокол', 'choco'],
}

def sentiment_analysis(text: str):
    text = (text or '').lower()
    score = 0
    for phrase in POSITIVE_WORDS:
        if phrase in text:
            score += 1
    for phrase in NEGATIVE_WORDS:
        if phrase in text:
            score -= 1
    label = 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'
    return label, score

def detect_tags(text: str):
    text = (text or '').lower()
    return [tag for tag, keys in TAG_RULES.items() if any(k in text for k in keys)]

def send_telegram_order(order):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
    product_title = order.product.title if order.product else 'Не вказано'
    message = (
        '🍰 Нова заявка Solchik\n'
        f'Продукт: {product_title}\n'
        f'Ім’я: {order.name}\n'
        f'Контакт: {order.phone}\n'
        f'Повідомлення: {order.message}\n'
        f'Джерело: {order.source} / {order.utm_source}\n'
        f'Сума: {order.amount} грн'
    )
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    response = requests.post(url, data={'chat_id': settings.TELEGRAM_CHAT_ID, 'text': message}, timeout=10)
    return response.ok
