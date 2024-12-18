# Используем образ Python 3.11 как базовый
FROM python:3.11-slim

# Установка рабочей директории в /app
WORKDIR /app

# Копирование файла с зависимостями
COPY requirements.txt .

# Установка зависимостей из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Установка PostgreSQL клиента
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

# Копирование кода приложения в контейнер
COPY . .

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка команды для запуска приложения
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]