# Используем официальный Python образ
FROM python:3.13

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код в контейнер (все файлы из папки backend/app)
COPY app/ ./app

# Устанавливаем переменную окружения PYTHONPATH, чтобы Python мог найти app
ENV PYTHONPATH=/app

# Запускаем FastAPI с Uvicorn
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]