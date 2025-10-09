# Настройка Nginx для исправления ошибки 404 при загрузке PDF

## Проблема
При загрузке PDF файлов на продакшн сайте `https://adaptation.almau.edu.kz` возникает ошибка 404 Not Found от Nginx. Это происходит потому, что Nginx не настроен для раздачи медиафайлов.

## Решение

### 1. Подключение к серверу
```bash
ssh user@your-server-ip
```

### 2. Найти путь к проекту
```bash
# Найти где находится проект Django
find / -name "manage.py" -type f 2>/dev/null | grep adaptation
# или
find /home -name "manage.py" -type f 2>/dev/null
# или
find /var/www -name "manage.py" -type f 2>/dev/null
```

### 3. Запустить скрипт настройки
```bash
# Скачать скрипт на сервер
wget https://raw.githubusercontent.com/your-repo/almau-adaptation/main/deploy_nginx_config.sh

# Сделать исполняемым
chmod +x deploy_nginx_config.sh

# Отредактировать путь к проекту в скрипте
nano deploy_nginx_config.sh
# Заменить PROJECT_PATH="/path/to/your/project" на реальный путь

# Запустить с правами root
sudo bash deploy_nginx_config.sh
```

### 4. Альтернативный способ - ручная настройка

#### Создать конфигурацию Nginx:
```bash
sudo nano /etc/nginx/sites-available/adaptation
```

#### Вставить следующую конфигурацию:
```nginx
server {
    listen 80;
    server_name adaptation.almau.edu.kz;

    # Основное приложение Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Статические файлы (CSS, JS, изображения)
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Медиа файлы (загруженные пользователями: PDF, видео, изображения)
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        
        # Безопасность для загруженных файлов
        add_header X-Content-Type-Options nosniff;
        add_header X-Frame-Options DENY;
        
        # Разрешаем только определенные типы файлов
        location ~* \.(pdf|doc|docx|txt|mp4|avi|mov|wmv|jpg|jpeg|png|gif)$ {
            # Разрешаем доступ к этим типам файлов
        }
        
        # Блокируем выполнение скриптов
        location ~* \.(php|pl|py|jsp|asp|sh|cgi)$ {
            deny all;
        }
    }

    # Безопасность
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Логирование
    access_log /var/log/nginx/adaptation_access.log;
    error_log /var/log/nginx/adaptation_error.log;
}
```

#### Включить сайт:
```bash
sudo ln -s /etc/nginx/sites-available/adaptation /etc/nginx/sites-enabled/
```

#### Проверить конфигурацию:
```bash
sudo nginx -t
```

#### Перезагрузить Nginx:
```bash
sudo systemctl reload nginx
```

### 5. Проверка работы

После настройки проверьте:

1. **Статические файлы**: `https://adaptation.almau.edu.kz/static/css/style.css`
2. **Медиа файлы**: `https://adaptation.almau.edu.kz/media/instructions/pdfs/12-презентация_нов.pdf`
3. **Загрузка PDF**: Попробуйте загрузить PDF через админку

### 6. Логи для отладки

Если проблемы остаются, проверьте логи:
```bash
# Логи Nginx
sudo tail -f /var/log/nginx/adaptation_error.log
sudo tail -f /var/log/nginx/adaptation_access.log

# Логи Django (если используется systemd)
sudo journalctl -u your-django-service -f
```

### 7. Права доступа

Убедитесь, что Nginx может читать медиафайлы:
```bash
# Проверить права на папку media
ls -la /path/to/your/project/media/

# Если нужно, исправить права
sudo chown -R www-data:www-data /path/to/your/project/media/
sudo chmod -R 755 /path/to/your/project/media/
```

## Структура медиафайлов

Проект использует следующие пути для медиафайлов:
- `media/instructions/pdfs/` - PDF инструкции
- `media/instructions/videos/` - Видео инструкции  
- `media/documents/` - Документы
- `media/lessons/pdfs/` - PDF уроки
- `media/lessons/videos/` - Видео уроки
- `media/lessons/slides/` - Слайды уроков
- `media/leaders/` - Фото руководства
- `media/about/` - Изображения истории университета
- `media/campus/` - Изображения кампуса
- `media/feedback/` - Файлы обратной связи

## Безопасность

Конфигурация включает меры безопасности:
- Блокировка выполнения скриптов в медиапапке
- Заголовки безопасности
- Ограничение типов файлов
- Защита от XSS и других атак
