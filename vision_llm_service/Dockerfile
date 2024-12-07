# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    poppler-utils \
    curl && \
    curl -fsSL https://ollama.com/install.sh | bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python зависимости
COPY requirements_vllm.txt .
RUN pip install --no-cache-dir -r requirements_vllm.txt

# Копируем все файлы проекта
COPY . .

# Указываем порт, который будет слушать приложение
EXPOSE 8001

# Команда для запуска Ollama и FastAPI
CMD ["sh", "-c", "ollama serve & ollama pull llama3.1:8b-instruct-q8_0 && uvicorn vllm_fastapi:app --host 0.0.0.0 --port 8001"]