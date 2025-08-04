from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Teacher
from django.db import transaction

class Command(BaseCommand):
    help = 'Создает тестового преподавателя для входа в систему'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                email = 'teacher@almau.edu.kz'
                password = 'teacher123'
                full_name = 'Иванов Иван Иванович'
                department = 'Кафедра информационных технологий'
                position = 'Доцент'

                # Проверяем, существует ли пользователь с таким email
                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.WARNING(f'Преподаватель с email {email} уже существует!')
                    )
                    return

                # Создаем пользователя
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                # Создаем преподавателя
                teacher = Teacher.objects.create(
                    user=user,
                    full_name=full_name,
                    department=department,
                    position=position
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Тестовый преподаватель успешно создан!\n'
                        f'Email: {email}\n'
                        f'Пароль: {password}\n'
                        f'Имя: {full_name}\n'
                        f'Кафедра: {department}\n'
                        f'Должность: {position}\n\n'
                        f'Теперь можно войти в систему используя эти данные!'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании преподавателя: {e}')
            ) 