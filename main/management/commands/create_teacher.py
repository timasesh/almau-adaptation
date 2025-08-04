from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Teacher
from django.db import transaction

class Command(BaseCommand):
    help = 'Создает нового преподавателя'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email преподавателя')
        parser.add_argument('--password', type=str, help='Пароль преподавателя')
        parser.add_argument('--full-name', type=str, help='Полное имя преподавателя')
        parser.add_argument('--department', type=str, help='Кафедра преподавателя')
        parser.add_argument('--position', type=str, help='Должность преподавателя')
        parser.add_argument('--phone', type=str, help='Телефон преподавателя')
        parser.add_argument('--office', type=str, help='Кабинет преподавателя')

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Получаем данные от пользователя или из аргументов
                email = options['email'] or input('Email преподавателя: ')
                password = options['password'] or input('Пароль: ')
                full_name = options['full_name'] or input('Полное имя: ')
                department = options['department'] or input('Кафедра (необязательно): ')
                position = options['position'] or input('Должность (необязательно): ')
                phone = options['phone'] or input('Телефон (необязательно): ')
                office = options['office'] or input('Кабинет (необязательно): ')

                # Проверяем, существует ли пользователь с таким email
                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.ERROR(f'Пользователь с email {email} уже существует!')
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
                    position=position,
                    phone=phone,
                    office=office
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Преподаватель "{full_name}" успешно создан!\n'
                        f'Email: {email}\n'
                        f'Кафедра: {department}\n'
                        f'Должность: {position}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании преподавателя: {e}')
            ) 