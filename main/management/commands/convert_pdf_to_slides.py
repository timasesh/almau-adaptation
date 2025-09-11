from django.core.management.base import BaseCommand
from main.models import Lesson


class Command(BaseCommand):
    help = 'Конвертирует PDF файлы уроков в слайды'

    def add_arguments(self, parser):
        parser.add_argument(
            '--lesson-id',
            type=int,
            help='ID урока для конвертации (если не указан, конвертируются все уроки с PDF)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно переконвертировать существующие слайды',
        )

    def handle(self, *args, **options):
        lesson_id = options.get('lesson_id')
        force = options.get('force')
        
        if lesson_id:
            lessons = Lesson.objects.filter(id=lesson_id, pdf_file__isnull=False)
        else:
            lessons = Lesson.objects.filter(pdf_file__isnull=False)
        
        if not lessons.exists():
            self.stdout.write(
                self.style.WARNING('Уроки с PDF файлами не найдены')
            )
            return
        
        self.stdout.write(f"Найдено {lessons.count()} уроков с PDF файлами")
        
        for lesson in lessons:
            self.stdout.write(f"Обрабатываем урок: {lesson.title}")
            
            # Проверяем, есть ли уже слайды
            if lesson.slides.exists() and not force:
                self.stdout.write(f"  - У урока уже есть {lesson.slides.count()} слайдов. Пропускаем.")
                continue
            
            try:
                success = lesson.convert_pdf_to_slides()
                if success:
                    slides_count = lesson.slides.count()
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ Успешно конвертировано в {slides_count} слайдов")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"  ❌ Ошибка при конвертации")
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  ❌ Исключение при конвертации: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS('Конвертация завершена!')
        )
