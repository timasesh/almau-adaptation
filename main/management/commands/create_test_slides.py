from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io
from main.models import Lesson, LessonSlide


class Command(BaseCommand):
    help = 'Создает тестовые слайды для уроков'

    def add_arguments(self, parser):
        parser.add_argument(
            '--lesson-id',
            type=int,
            help='ID урока для создания слайдов (если не указан, создаются для всех уроков)',
        )

    def handle(self, *args, **options):
        lesson_id = options.get('lesson_id')
        
        if lesson_id:
            lessons = Lesson.objects.filter(id=lesson_id)
        else:
            lessons = Lesson.objects.filter(is_active=True)
        
        if not lessons.exists():
            self.stdout.write(
                self.style.WARNING('Уроки не найдены')
            )
            return
        
        for lesson in lessons:
            self.create_slides_for_lesson(lesson)
        
        self.stdout.write(
            self.style.SUCCESS(f'Успешно созданы слайды для {lessons.count()} уроков')
        )

    def create_slides_for_lesson(self, lesson):
        """Создает тестовые слайды для урока"""
        # Удаляем существующие слайды
        lesson.slides.all().delete()
        
        # Создаем 5 тестовых слайдов
        slide_titles = [
            f"Введение в {lesson.title}",
            "Основные концепции",
            "Практические примеры",
            "Важные моменты",
            "Заключение"
        ]
        
        slide_descriptions = [
            f"Добро пожаловать в урок '{lesson.title}'. В этом уроке мы изучим основные принципы и методы.",
            "Рассмотрим ключевые концепции и их взаимосвязи. Это поможет лучше понять материал.",
            "Посмотрим на практические примеры применения изученных концепций в реальных ситуациях.",
            "Обратим внимание на важные моменты, которые нужно запомнить и применить на практике.",
            "Подведем итоги изученного материала и определим следующие шаги для углубления знаний."
        ]
        
        for i, (title, description) in enumerate(zip(slide_titles, slide_descriptions)):
            # Создаем тестовое изображение
            image = self.create_test_slide_image(title, description, i + 1, len(slide_titles))
            
            # Сохраняем изображение в байты
            img_io = io.BytesIO()
            image.save(img_io, format='PNG')
            img_io.seek(0)
            
            # Создаем слайд
            slide = LessonSlide.objects.create(
                lesson=lesson,
                order=i + 1,
                title=title,
                description=description
            )
            
            # Сохраняем изображение
            slide.image.save(
                f'slide_{i + 1}.png',
                ContentFile(img_io.getvalue()),
                save=True
            )
            
            self.stdout.write(
                f'Создан слайд {i + 1} для урока "{lesson.title}"'
            )

    def create_test_slide_image(self, title, description, slide_num, total_slides):
        """Создает тестовое изображение слайда"""
        # Создаем изображение
        width, height = 1200, 800
        image = Image.new('RGB', (width, height), color='#f0f0f0')
        draw = ImageDraw.Draw(image)
        
        # Добавляем градиентный фон
        for y in range(height):
            r = int(240 - (y / height) * 40)
            g = int(240 - (y / height) * 40)
            b = int(240 - (y / height) * 40)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Добавляем заголовок
        try:
            # Пытаемся использовать системный шрифт
            title_font = ImageFont.truetype("arial.ttf", 48)
            desc_font = ImageFont.truetype("arial.ttf", 24)
            small_font = ImageFont.truetype("arial.ttf", 18)
        except:
            # Если не удалось, используем стандартный
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Заголовок слайда
        draw.text((width//2, 100), title, fill='#2c3e50', font=title_font, anchor="mm")
        
        # Описание
        # Разбиваем описание на строки
        words = description.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=desc_font)
            if bbox[2] < width - 200:  # Оставляем отступы
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем строки описания
        y_offset = 200
        for line in lines:
            draw.text((width//2, y_offset), line, fill='#34495e', font=desc_font, anchor="mm")
            y_offset += 40
        
        # Добавляем номер слайда
        slide_text = f"Слайд {slide_num} из {total_slides}"
        draw.text((width - 50, height - 30), slide_text, fill='#7f8c8d', font=small_font, anchor="rb")
        
        # Добавляем декоративные элементы
        # Верхняя полоса
        draw.rectangle([0, 0, width, 10], fill='#3498db')
        
        # Левый акцент
        draw.rectangle([0, 0, 20, height], fill='#3498db')
        
        return image
