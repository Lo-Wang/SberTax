# main.py
from fastapi import FastAPI, Request, Depends
from starlette.responses import RedirectResponse, JSONResponse
from auth.oauth import oauth

app = FastAPI()

@app.get("/")
async def homepage():
    return {"message": "Выберите сервис для авторизации"}

# Маршрут для авторизации через Google
@app.get("/auth/google")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(request, config.REDIRECT_URI + "/google")

# Callback для Google
@app.get("/auth/callback/google")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return JSONResponse({"user_info": user_info})

# Маршрут для авторизации через Яндекс
@app.get("/auth/yandex")
async def auth_yandex(request: Request):
    return await oauth.yandex.authorize_redirect(request, config.REDIRECT_URI + "/yandex")

# Callback для Яндекс
@app.get("/auth/callback/yandex")
async def auth_yandex_callback(request: Request):
    token = await oauth.yandex.authorize_access_token(request)
    resp = await oauth.yandex.get("https://login.yandex.ru/info", token=token)
    return JSONResponse({"user_info": resp.json()})

# Маршрут для авторизации через SberID
@app.get("/auth/sber")
async def auth_sber(request: Request):
    return await oauth.sber.authorize_redirect(request, config.REDIRECT_URI + "/sber")

# Callback для SberID
@app.get("/auth/callback/sber")
async def auth_sber_callback(request: Request):
    token = await oauth.sber.authorize_access_token(request)
    user_info = token["userinfo"]
    return JSONResponse({"user_info": user_info})
