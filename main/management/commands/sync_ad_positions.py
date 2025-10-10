from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Position, Profile
from django.conf import settings
from datetime import datetime
import requests


class Command(BaseCommand):
    help = "Выгружает всех сотрудников из Entra ID и синхронизирует с локальной базой Django"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🔄 Начало синхронизации сотрудников из Entra ID..."))

        # --- 1️⃣ Получение токена ---
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
            self.stdout.write(self.style.ERROR("❌ Не удалось получить токен."))
            return

        headers = {"Authorization": f"Bearer {token}"}
        graph_url = "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,jobTitle,userPrincipalName,department"

        employees = []
        next_link = graph_url

        # --- 2️⃣ Пагинация (Microsoft Graph выдаёт по 100 записей) ---
        while next_link:
            resp = requests.get(next_link, headers=headers)
            if resp.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Ошибка Graph API: {resp.text}"))
                break

            data = resp.json()
            employees.extend(data.get("value", []))
            next_link = data.get("@odata.nextLink")

        self.stdout.write(f"📥 Получено записей: {len(employees)}")

        updated = 0
        created = 0

        # --- 3️⃣ Обработка сотрудников ---
        for emp in employees:
            username = emp.get("userPrincipalName", "").split("@")[0]
            email = emp.get("mail") or f"{username}@almau.kz"
            full_name = emp.get("displayName") or username
            job_title = emp.get("jobTitle") or "Без должности"

            if not username:
                continue

            # --- Django User ---
            user, is_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": full_name.split(" ")[0],
                    "last_name": " ".join(full_name.split(" ")[1:]),
                }
            )

            if not is_created:
                user.email = email
                user.first_name = full_name.split(" ")[0]
                user.last_name = " ".join(full_name.split(" ")[1:])
                user.save()
                updated += 1
            else:
                created += 1

            # --- Position & Profile ---
            pos, _ = Position.objects.get_or_create(name=job_title)
            profile, _ = Profile.objects.get_or_create(user=user)
            if profile.position != pos:
                profile.position = pos
                profile.save()

        self.stdout.write(self.style.SUCCESS(f"✅ Создано {created}, обновлено {updated} сотрудников"))
        self.stdout.write(self.style.SUCCESS(f"📅 Завершено: {datetime.now()}"))

