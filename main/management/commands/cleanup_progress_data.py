from django.core.management.base import BaseCommand
from main.models import LessonProgress
from django.db import transaction

class Command(BaseCommand):
    help = 'Очищает проблемные данные прогресса пользователей'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем очистку проблемных данных прогресса...')
        
        with transaction.atomic():
            # Получаем все записи прогресса
            progress_records = LessonProgress.objects.all()
            cleaned_count = 0
            
            for progress in progress_records:
                needs_update = False
                
                # Проверяем и очищаем video_max_progress_percent
                if hasattr(progress, 'video_max_progress_percent'):
                    try:
                        if progress.video_max_progress_percent is not None:
                            float(progress.video_max_progress_percent)
                    except (ValueError, TypeError):
                        self.stdout.write(f'Очищаем video_max_progress_percent для записи {progress.id}')
                        progress.video_max_progress_percent = 0
                        needs_update = True
                
                # Проверяем и очищаем video_current_time
                if hasattr(progress, 'video_current_time'):
                    try:
                        if progress.video_current_time is not None:
                            float(progress.video_current_time)
                    except (ValueError, TypeError):
                        self.stdout.write(f'Очищаем video_current_time для записи {progress.id}')
                        progress.video_current_time = 0
                        needs_update = True
                
                # Проверяем и очищаем video_total_time
                if hasattr(progress, 'video_total_time'):
                    try:
                        if progress.video_total_time is not None:
                            float(progress.video_total_time)
                    except (ValueError, TypeError):
                        self.stdout.write(f'Очищаем video_total_time для записи {progress.id}')
                        progress.video_total_time = 0
                        needs_update = True
                
                # Проверяем и очищаем slides_current_slide
                if hasattr(progress, 'slides_current_slide'):
                    try:
                        if progress.slides_current_slide is not None:
                            int(progress.slides_current_slide)
                    except (ValueError, TypeError):
                        self.stdout.write(f'Очищаем slides_current_slide для записи {progress.id}')
                        progress.slides_current_slide = 0
                        needs_update = True
                
                # Проверяем и очищаем slides_total_slides
                if hasattr(progress, 'slides_total_slides'):
                    try:
                        if progress.slides_total_slides is not None:
                            int(progress.slides_total_slides)
                    except (ValueError, TypeError):
                        self.stdout.write(f'Очищаем slides_total_slides для записи {progress.id}')
                        progress.slides_total_slides = 0
                        needs_update = True
                
                if needs_update:
                    progress.save()
                    cleaned_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Очистка завершена! Обработано записей: {cleaned_count}')
            )
