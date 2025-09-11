from django.core.management.base import BaseCommand
from main.models import Leader

class Command(BaseCommand):
    help = 'Тестирование создания и отображения руководителей'

    def handle(self, *args, **options):
        self.stdout.write('=== Тестирование руководителей ===')
        
        # Проверяем существующих руководителей
        leaders = Leader.objects.all()
        self.stdout.write(f'Найдено руководителей: {leaders.count()}')
        
        for leader in leaders:
            self.stdout.write(f'- ID: {leader.id}, Имя: {leader.full_name}, Должность: {leader.get_role_display()}')
        
        # Создаем тестового руководителя
        if not Leader.objects.filter(full_name='Тестовый Ректор').exists():
            leader = Leader.objects.create(
                role='rector',
                full_name='Тестовый Ректор',
                order=1
            )
            self.stdout.write(f'Создан тестовый руководитель: {leader.full_name} (ID: {leader.id})')
        else:
            self.stdout.write('Тестовый руководитель уже существует')
        
        # Проверяем снова
        leaders = Leader.objects.all()
        self.stdout.write(f'Всего руководителей после теста: {leaders.count()}')
        
        self.stdout.write(self.style.SUCCESS('Тест завершен'))
