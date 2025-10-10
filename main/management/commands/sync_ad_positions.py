import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Position, Profile
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = "Синхронизирует должности пользователей с Entra ID (Microsoft Graph API)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🔄 Начало синхронизации должностей..."))
        updated = 0

        # Используем твои ENV переменные
        token_url = f"{settings.MS_TENANT}/oauth2/v2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.MS_CLIENT_ID,
            "client_secret": settings.MS_CLIENT_SECRET,
            "scope": "https://graph.microsoft.com/.default",
        }

        # Получаем токен Microsoft Graph API
        token_resp = requests.post(token_url, data=data)
        token_data = token_resp.json()
        token = token_data.get("access_token")

        if not token:
            self.stdout.write(self.style.ERROR(f"❌ Не удалось получить токен: {token_data}"))
            return

        # Запрашиваем пользователей
        resp = requests.get(
            "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,jobTitle,userPrincipalName",
            headers={"Authorization": f"Bearer {token}"}
        )

        if resp.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Ошибка Graph API: {resp.status_code} {resp.text}"))
            return

        # Перебираем пользователей
        for u in resp.json().get("value", []):
            username = u.get("userPrincipalName", "").split("@")[0]
            job = u.get("jobTitle")

            if not username or not job:
                continue

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                continue

            pos, _ = Position.objects.get_or_create(name=job)
            profile, _ = Profile.objects.get_or_create(user=user)

            if profile.position != pos:
                profile.position = pos
                profile.save()
                updated += 1
                self.stdout.write(f"✅ {username} → {job}")

        self.stdout.write(self.style.SUCCESS(f"🎯 Обновлено {updated} пользователей."))
        self.stdout.write(self.style.SUCCESS(f"📅 Завершено: {datetime.now()}"))
