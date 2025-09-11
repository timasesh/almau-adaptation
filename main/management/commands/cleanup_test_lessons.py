from django.core.management.base import BaseCommand
from main.models import Lesson


class Command(BaseCommand):
    help = 'Удаляет тестовые уроки из базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно удалить все тестовые уроки',
        )

    def handle(self, *args, **options):
        # Список названий тестовых уроков
        test_lesson_titles = [
            "Введение в адаптацию",
            "Работа с документами", 
            "Продвинутые техники обучения"
        ]
        
        # Находим тестовые уроки
        test_lessons = Lesson.objects.filter(title__in=test_lesson_titles)
        
        if not test_lessons.exists():
            self.stdout.write(
                self.style.WARNING('Тестовые уроки не найдены в базе данных.')
            )
            return
        
        self.stdout.write(f'Найдено {test_lessons.count()} тестовых уроков:')
        for lesson in test_lessons:
            self.stdout.write(f'  - {lesson.title} (ID: {lesson.id})')
        
        if not options['force']:
            confirm = input('\nВы уверены, что хотите удалить эти уроки? (y/N): ')
            if confirm.lower() != 'y':
                self.stdout.write(
                    self.style.WARNING('Удаление отменено.')
                )
                return
        
        # Удаляем уроки
        deleted_count = 0
        for lesson in test_lessons:
            try:
                lesson_title = lesson.title
                lesson.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Урок "{lesson_title}" успешно удален.')
                )
                deleted_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при удалении урока "{lesson.title}": {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nУдалено {deleted_count} из {test_lessons.count()} тестовых уроков.')
        )
