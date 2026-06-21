# Код програмної реалізації для дипломної роботи «Сольчик»

Архів містить два компоненти:

1. `solchik_app/` — Django вебзастосунок «Сольчик» для каталогу, CRM-заявок, аналітики, Telegram-інтеграції, аналізу тональності, трендів і dashboard.
2. `solchikcake_site/` — сайт-візитка `solchik.cake`, який показує продукцію і передає замовлення в Telegram із UTM/product-параметрами.

## Швидкий запуск Django

```bash
cd solchik_app
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Відкрити: http://127.0.0.1:8000/

## Налаштування Telegram

У `solchik_app/.env.example` вказано змінні:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Скопіюйте файл у `.env` і заповніть значення.
