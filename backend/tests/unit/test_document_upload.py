import os
import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

UPLOAD_DIR = "uploaded_files/"  # Укажите путь для сохранения файлов

# Тесты для проверки успешной загрузки документов
@pytest.mark.parametrize("file_path, file_type", [
    ("tests/test_files/sample.pdf", "application/pdf"),
    ("tests/test_files/sample.png", "image/png"),
    ("tests/test_files/sample.jpg", "image/jpeg"),
])
def test_upload_document_success(file_path, file_type):
    with open(file_path, "rb") as file:
        response = client.post(
            "/upload",
            files={"file": (os.path.basename(file_path), file, file_type)},
        )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

# Тест для невалидного формата
def test_upload_document_invalid_format():
    with open("tests/test_files/sample.txt", "rb") as file:
        response = client.post(
            "/upload",
            files={"file": ("sample.txt", file, "text/plain")},
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file format"

# Тест для проверки авторизации при загрузке документов
def test_upload_document_unauthorized():
    with open("tests/test_files/sample.pdf", "rb") as file:
        response = client.post(
            "/upload",
            files={"file": ("sample.pdf", file, "application/pdf")},
            headers={"Authorization": "Bearer invalid_token"},
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
