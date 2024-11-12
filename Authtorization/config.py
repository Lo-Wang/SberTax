from dotenv import load_dotenv
import os

load_dotenv()

# Параметры для наших сервисов
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
YANDEX_CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
SBER_CLIENT_ID = os.getenv("SBER_CLIENT_ID")
SBER_CLIENT_SECRET = os.getenv("SBER_CLIENT_SECRET")

REDIRECT_URI = os.getenv("REDIRECT_URI")  # общий редирект URI для всех сервисов
