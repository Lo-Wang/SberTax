import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.main import app

client = TestClient(app)

# Mock ответы от Сбер и Яндекс для тестов
@pytest.fixture
def mock_sber_response():
    return {"access_token": "sber_token", "expires_in": 3600}

@pytest.fixture
def mock_yandex_response():
    return {"access_token": "yandex_token", "expires_in": 3600}

### Тесты для Сбер ID ###
@patch("app.api.auth.sber_service.exchange_code_for_token")
def test_sber_auth_url(mock_sber_token):
    response = client.get("/auth/sber")
    assert response.status_code == 200
    assert "sberbank.ru" in response.json()["url"]

def test_sber_auth_callback_success(mock_sber_response):
    with patch("app.api.auth.sber_service.exchange_code_for_token", return_value=mock_sber_response):
        response = client.get("/auth/callback/sber?code=valid_code")
    assert response.status_code == 200
    assert response.json()["access_token"] == "sber_token"

### Тесты для Яндекс ID ###
@patch("app.api.auth.yandex_service.exchange_code_for_token")
def test_yandex_auth_url(mock_yandex_token):
    response = client.get("/auth/yandex")
    assert response.status_code == 200
    assert "oauth.yandex.ru" in response.json()["url"]

def test_yandex_auth_callback_success(mock_yandex_response):
    with patch("app.api.auth.yandex_service.exchange_code_for_token", return_value=mock_yandex_response):
        response = client.get("/auth/callback/yandex?code=valid_code")
    assert response.status_code == 200
    assert response.json()["access_token"] == "yandex_token"
