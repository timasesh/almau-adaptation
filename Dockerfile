# 1. Базовый образ
FROM python:3.12-slim

# 2. Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# 3. Создаём директорию приложения
WORKDIR /app

# 4. Устанавливаем зависимости Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем проект
COPY . /app/

# 6. Собираем статику
RUN python manage.py collectstatic --noinput

# 7. Запуск через gunicorn
CMD ["gunicorn", "almau_adaptation.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4"]
