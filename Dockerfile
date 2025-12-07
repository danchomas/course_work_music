# Dockerfile

FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
# Назовем её /src или /app (не путать с папкой app на хосте)
WORKDIR /src

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 1. Копируем requirements.txt
# Если он лежит ВНУТРИ папки app:
COPY app/requirements.txt .
# Если он лежит В КОРНЕ (рядом с Dockerfile), то: COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 2. Копируем содержимое папки app внутрь рабочей директории контейнера (/src)
# То есть /src/main.py, /src/core, /src/routers и т.д.
COPY app .

# 3. Запускаем
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
