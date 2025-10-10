# main/management/commands/sync_ad_positions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Position, Profile
from django.conf import settings
import requests
from datetime import datetime


class Command(BaseCommand):
    help = "Синхронизирует должности пользователей с Entra ID (Microsoft Graph API)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🔄 Начало синхронизации должностей..."))

        # --- Получение токена ---
        token_url = f"https://login.microsoftonline.com/{settings.MS_TENANT}/oauth2/v2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.MS_CLIENT_ID,
            "client_secret": settings.MS_CLIENT_SECRET,
            "scope": "https://graph.microsoft.com/.default",
        }
        token_resp = requests.post(token_url, data=data)
        if token_resp.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Ошибка токена: {token_resp.text}"))
            return

        token = token_resp.json().get("access_token")
        if not token:
            self.stdout.write(self.style.ERROR("❌ Токен не получен"))
            return

        # --- Получаем пользователей из Graph API ---
        headers = {"Authorization": f"Bearer {token}"}
        users_resp = requests.get(
            "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,jobTitle,userPrincipalName",
            headers=headers,
        )

        if users_resp.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Ошибка Graph API: {users_resp.text}"))
            return

        users_data = users_resp.json().get("value", [])
        updated = 0

        # --- Обновляем профили ---
        for u in users_data:
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
