# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл требований
COPY requirements_backend.txt .

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y poppler-utils && \
    pip install --no-cache-dir -r requirements_backend.txt

# Копируем все файлы проекта
COPY . .

# Указываем порт, который будет слушать приложение
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]