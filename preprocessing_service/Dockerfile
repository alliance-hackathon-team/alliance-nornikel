# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    libreoffice-core \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    libreoffice-common \
    fonts-dejavu \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Устанавливаем зависимости Python
WORKDIR /app
COPY requirements_preprocessing.txt /app/
RUN pip install --no-cache-dir -r requirements_preprocessing.txt

# Копируем файлы приложения
COPY . /app

# Указываем рабочую директорию и точку входа
WORKDIR /app
CMD ["python", "file_to_pdf_converter.py"]