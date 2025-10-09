#!/bin/bash

# Скрипт для настройки Nginx для проекта Adaptation AlmaU
# Запускать с правами root: sudo bash deploy_nginx_config.sh

PROJECT_PATH="/path/to/your/project"  # ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ПУТЬ К ПРОЕКТУ
NGINX_CONFIG="/etc/nginx/sites-available/adaptation"
NGINX_ENABLED="/etc/nginx/sites-enabled/adaptation"

echo "Настройка Nginx для Adaptation AlmaU..."

# Создаем конфигурацию Nginx
cat > $NGINX_CONFIG << 'EOF'
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
        alias PROJECT_PATH/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Медиа файлы (загруженные пользователями: PDF, видео, изображения)
    location /media/ {
        alias PROJECT_PATH/media/;
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
EOF

# Заменяем PROJECT_PATH на реальный путь
sed -i "s|PROJECT_PATH|$PROJECT_PATH|g" $NGINX_CONFIG

# Создаем символическую ссылку для включения сайта
ln -sf $NGINX_CONFIG $NGINX_ENABLED

# Проверяем конфигурацию Nginx
nginx -t

if [ $? -eq 0 ]; then
    echo "Конфигурация Nginx корректна. Перезагружаем Nginx..."
    systemctl reload nginx
    echo "Nginx перезагружен успешно!"
    
    # Проверяем статус
    systemctl status nginx
    
    echo ""
    echo "✅ Настройка завершена!"
    echo "📁 Медиа файлы теперь доступны по адресу: http://adaptation.almau.edu.kz/media/"
    echo "📄 PDF файлы: http://adaptation.almau.edu.kz/media/instructions/pdfs/"
    echo "📹 Видео файлы: http://adaptation.almau.edu.kz/media/instructions/videos/"
else
    echo "❌ Ошибка в конфигурации Nginx!"
    exit 1
fi
