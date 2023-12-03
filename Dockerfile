# Используем базовый образ Python
FROM python:3.8

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev

# Создание и установка директории приложения
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt requirements.txt

# Установка зависимостей
RUN pip install -r requirements.txt

# Копирование файлов приложения в контейнер
COPY . .

# Запуск приложения
CMD ["python", "app.py"]
