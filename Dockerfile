# Используем официальный образ Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Применяем миграции базы данных
RUN python manage.py migrate

# Открываем порт, который будет использоваться контейнером
EXPOSE 8080

# Команда для запуска сервера разработки Django
CMD ["python", "manage.py", "runserver", "127.0.0.1:8080"]
