from authlib.integrations.starlette_client import OAuth
import config

oauth = OAuth()

# Google OAuth
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    redirect_uri=config.REDIRECT_URI + "/google",
    client_kwargs={"scope": "openid email profile"},
)

# Yandex OAuth
oauth.register(
    name="yandex",
    client_id=config.YANDEX_CLIENT_ID,
    client_secret=config.YANDEX_CLIENT_SECRET,
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    redirect_uri=config.REDIRECT_URI + "/yandex",
    client_kwargs={"scope": "login:email login:info"},
)

# SberID OAuth
oauth.register(
    name="sber",
    client_id=config.SBER_CLIENT_ID,
    client_secret=config.SBER_CLIENT_SECRET,
    authorize_url="https://sberid.sberbank.ru/authorize",
    access_token_url="https://sberid.sberbank.ru/token",
    redirect_uri=config.REDIRECT_URI + "/sber",
    client_kwargs={"scope": "openid email profile"},
)
