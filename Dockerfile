# Используем базовый образ с Python
FROM python:3.12-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл требований
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт
EXPOSE 8080

# Выполняем команду запуска
CMD ["sh", "-c", "until pg_isready -h db -p 5432; do echo 'Waiting for postgres...'; sleep 1; done; python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8080"]
