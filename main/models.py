from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.

class Instruction(models.Model):
    """Модель инструкции"""
    title = models.CharField(max_length=200, verbose_name="Название инструкции")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название (English)")
    title_kk = models.CharField(max_length=200, blank=True, verbose_name="Название (Қазақша)")

    description = models.TextField(verbose_name="Текст инструкции")
    description_en = models.TextField(blank=True, verbose_name="Текст (English)")
    description_kk = models.TextField(blank=True, verbose_name="Текст (Қазақша)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Инструкция"
        verbose_name_plural = "Инструкции"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_title(self, language: str = 'ru') -> str:
        if language == 'en' and self.title_en:
            return self.title_en
        if language == 'kk' and self.title_kk:
            return self.title_kk
        return self.title

    def get_description(self, language: str = 'ru') -> str:
        if language == 'en' and self.description_en:
            return self.description_en
        if language == 'kk' and self.description_kk:
            return self.description_kk
        return self.description

class Process(models.Model):
    """Модель процесса"""
    title = models.CharField(max_length=200, verbose_name="Название процесса")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название (English)")
    title_kk = models.CharField(max_length=200, blank=True, verbose_name="Название (Қазақша)")

    description = models.TextField(verbose_name="Текст процесса")
    description_en = models.TextField(blank=True, verbose_name="Текст (English)")
    description_kk = models.TextField(blank=True, verbose_name="Текст (Қазақша)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Процесс"
        verbose_name_plural = "Процессы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_title(self, language: str = 'ru') -> str:
        if language == 'en' and self.title_en:
            return self.title_en
        if language == 'kk' and self.title_kk:
            return self.title_kk
        return self.title

    def get_description(self, language: str = 'ru') -> str:
        if language == 'en' and self.description_en:
            return self.description_en
        if language == 'kk' and self.description_kk:
            return self.description_kk
        return self.description


class Teacher(models.Model):
    """Модель преподавателя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    department = models.CharField(max_length=200, blank=True, verbose_name="Кафедра")
    position = models.CharField(max_length=200, blank=True, verbose_name="Должность")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    office = models.CharField(max_length=100, blank=True, verbose_name="Кабинет")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем имя пользователя если не задано
        if not self.user.first_name and self.full_name:
            parts = self.full_name.split()
            if len(parts) >= 2:
                self.user.first_name = parts[0]
                self.user.last_name = ' '.join(parts[1:])
            else:
                self.user.first_name = self.full_name
            self.user.save()
        super().save(*args, **kwargs)

class DocumentCategory(models.Model):
    """Категории документов"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Название (English)")
    name_kk = models.CharField(max_length=100, blank=True, verbose_name="Название (Қазақша)")

    description = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание (English)")
    description_kk = models.TextField(blank=True, verbose_name="Описание (Қазақша)")
    order_index = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория документов"
        verbose_name_plural = "Категории документов"
        ordering = ['order_index', 'name']

    def __str__(self):
        return self.name

    def get_name(self, language: str = 'ru') -> str:
        if language == 'en' and self.name_en:
            return self.name_en
        if language == 'kk' and self.name_kk:
            return self.name_kk
        return self.name

class Document(models.Model):
    """Модель документов"""
    title = models.CharField(max_length=200, verbose_name="Название документа")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название (English)")
    title_kk = models.CharField(max_length=200, blank=True, verbose_name="Название (Қазақша)")
    
    description = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание (English)")
    description_kk = models.TextField(blank=True, verbose_name="Описание (Қазақша)")
    
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, verbose_name="Категория")
    
    file = models.FileField(upload_to='documents/', verbose_name="Файл (Русский)")
    file_en = models.FileField(upload_to='documents/', blank=True, verbose_name="Файл (English)")
    file_kk = models.FileField(upload_to='documents/', blank=True, verbose_name="Файл (Қазақша)")
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Загружено пользователем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Количество скачиваний")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_file_size(self):
        """Возвращает размер файла в читаемом формате"""
        if self.file:
            size = self.file.size
            if size < 1024:
                return f"{size} байт"
            elif size < 1024 * 1024:
                return f"{size // 1024} КБ"
            else:
                return f"{size // (1024 * 1024)} МБ"
        return "Неизвестно"

    def get_file_extension(self):
        """Возвращает расширение файла"""
        if self.file:
            return self.file.name.split('.')[-1].upper()
        return ""
    
    def get_title(self, language='ru'):
        """Получить название на нужном языке"""
        if language == 'en' and self.title_en:
            return self.title_en
        elif language == 'kk' and self.title_kk:
            return self.title_kk
        return self.title
    
    def get_description(self, language='ru'):
        """Получить описание на нужном языке"""
        if language == 'en' and self.description_en:
            return self.description_en
        elif language == 'kk' and self.description_kk:
            return self.description_kk
        return self.description
    
    def get_file(self, language='ru'):
        """Получить файл на нужном языке"""
        if language == 'en' and self.file_en:
            return self.file_en
        elif language == 'kk' and self.file_kk:
            return self.file_kk
        return self.file

    def increment_download_count(self):
        """Увеличивает счетчик скачиваний"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

class Feedback(models.Model):
    """Модель обратной связи"""
    RECIPIENT_CHOICES = [
        ('hr', 'HR'),
        ('it', 'IT поддержка'),
    ]
    
    TYPE_CHOICES = [
        ('suggestion', 'Предложение'),
        ('question', 'Вопрос'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    ]
    
    recipient = models.CharField(max_length=20, choices=RECIPIENT_CHOICES, verbose_name="Кому направить")
    feedback_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип обращения")
    subject = models.CharField(max_length=200, verbose_name="Тема обращения")
    message = models.TextField(verbose_name="Сообщение")
    file = models.FileField(upload_to='feedback/', blank=True, null=True, verbose_name="Прикрепленный файл")
    email = models.EmailField(verbose_name="Почта")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    
    # Служебные поля
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"

class FAQCategory(models.Model):
    """Категории для часто задаваемых вопросов"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Название (English)")
    name_kk = models.CharField(max_length=100, blank=True, verbose_name="Название (Қазақша)")

    description = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание (English)")
    description_kk = models.TextField(blank=True, verbose_name="Описание (Қазақша)")
    order_index = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория FAQ"
        verbose_name_plural = "Категории FAQ"
        ordering = ['order_index', 'name']

    def __str__(self):
        return self.name

    def get_name(self, language: str = 'ru') -> str:
        if language == 'en' and self.name_en:
            return self.name_en
        if language == 'kk' and self.name_kk:
            return self.name_kk
        return self.name

class FAQ(models.Model):
    """Модель часто задаваемых вопросов"""
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    question_en = models.CharField(max_length=300, blank=True, verbose_name="Вопрос (English)")
    question_kk = models.CharField(max_length=300, blank=True, verbose_name="Вопрос (Қазақша)")

    answer = models.TextField(verbose_name="Ответ")
    answer_en = models.TextField(blank=True, verbose_name="Ответ (English)")
    answer_kk = models.TextField(blank=True, verbose_name="Ответ (Қазақша)")
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, verbose_name="Категория")
    order_index = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    is_popular = models.BooleanField(default=False, verbose_name="Популярный вопрос")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"
        ordering = ['category__order_index', 'order_index', '-is_popular', 'question']

    def __str__(self):
        return self.question

    def get_question(self, language: str = 'ru') -> str:
        if language == 'en' and self.question_en:
            return self.question_en
        if language == 'kk' and self.question_kk:
            return self.question_kk
        return self.question

    def get_answer(self, language: str = 'ru') -> str:
        if language == 'en' and self.answer_en:
            return self.answer_en
        if language == 'kk' and self.answer_kk:
            return self.answer_kk
        return self.answer

    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class History(models.Model):
    """История университета (редактируемый текст + картинка)"""
    text = models.TextField(verbose_name="Текст истории", help_text="Простой текст истории университета")
    text_en = models.TextField(blank=True, verbose_name="Текст истории (English)", help_text="University history text in English")
    text_kk = models.TextField(blank=True, verbose_name="Текст истории (Қазақша)", help_text="Университет тарихының мәтіні қазақ тілінде")
    image = models.ImageField(upload_to='about/', blank=True, verbose_name="Картинка истории")

    class Meta:
        verbose_name = "История университета"
        verbose_name_plural = "История университета"

    def __str__(self):
        return "История AlmaU"

    def get_text(self, language: str = 'ru') -> str:
        if language == 'en' and self.text_en:
            return self.text_en
        if language == 'kk' and self.text_kk:
            return self.text_kk
        return self.text

class Mission(models.Model):
    """Миссия университета (редактируемый текст)"""
    text = models.CharField(max_length=500, verbose_name="Текст миссии")
    text_en = models.CharField(max_length=500, blank=True, verbose_name="Текст миссии (English)")
    text_kk = models.CharField(max_length=500, blank=True, verbose_name="Текст миссии (Қазақша)")

    class Meta:
        verbose_name = "Миссия университета"
        verbose_name_plural = "Миссия университета"

    def __str__(self):
        return "Миссия AlmaU"

    def get_text(self, language: str = 'ru') -> str:
        if language == 'en' and self.text_en:
            return self.text_en
        if language == 'kk' and self.text_kk:
            return self.text_kk
        return self.text

class Values(models.Model):
    """Ценности университета (редактируемый текст)"""
    text = models.CharField(max_length=500, verbose_name="Текст ценностей")
    text_en = models.CharField(max_length=500, blank=True, verbose_name="Текст ценностей (English)")
    text_kk = models.CharField(max_length=500, blank=True, verbose_name="Текст ценностей (Қазақша)")

    class Meta:
        verbose_name = "Ценности университета"
        verbose_name_plural = "Ценности университета"

    def __str__(self):
        return "Ценности AlmaU"

    def get_text(self, language: str = 'ru') -> str:
        if language == 'en' and self.text_en:
            return self.text_en
        if language == 'kk' and self.text_kk:
            return self.text_kk
        return self.text


class ContactInfo(models.Model):
    """Контент страницы Контакты и карта"""
    address = models.CharField(max_length=255, verbose_name="Адрес")
    address_en = models.CharField(max_length=255, blank=True, verbose_name="Адрес (English)")
    address_kk = models.CharField(max_length=255, blank=True, verbose_name="Адрес (Қазақша)")

    phone = models.CharField(max_length=50, verbose_name="Телефон")

    campus_items = models.TextField(help_text="Список пунктов через перевод строки", verbose_name="Кампус — пункты")
    campus_items_en = models.TextField(blank=True, verbose_name="Кампус — пункты (English)")
    campus_items_kk = models.TextField(blank=True, verbose_name="Кампус — пункты (Қазақша)")
    
    campus_image = models.ImageField(
        upload_to='campus/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение кампуса",
        help_text="Изображение отображается на странице 'Контакты и карта' в разделе 'Кампус'"
    )
    
    # 3D кнопка кампуса
    campus_3d_button_text = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Текст кнопки 3D кампуса",
        default="Изучить кампус в 3D",
        help_text="Текст, который отображается на кнопке для 3D просмотра кампуса"
    )
    campus_3d_button_text_en = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Текст кнопки 3D кампуса (English)",
        help_text="Текст кнопки на английском языке"
    )
    campus_3d_button_text_kk = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Текст кнопки 3D кампуса (Қазақша)",
        help_text="Текст кнопки на казахском языке"
    )
    
    campus_3d_url = models.URLField(
        blank=True, 
        verbose_name="Ссылка на 3D кампус",
        help_text="URL для 3D просмотра кампуса (например, виртуальный тур)"
    )
    
    campus_3d_enabled = models.BooleanField(
        default=False,
        verbose_name="Показывать кнопку 3D кампуса",
        help_text="Включить/выключить отображение кнопки 3D кампуса на сайте"
    )
    
    # IT поддержка
    it_support_url = models.URLField(
        blank=True, 
        verbose_name="Ссылка на IT поддержку",
        help_text="URL для IT поддержки (например, система helpdesk)"
    )
    it_support_enabled = models.BooleanField(
        default=True,
        verbose_name="Показывать кнопку IT поддержки",
        help_text="Включить/выключить отображение кнопки IT поддержки на странице обратной связи"
    )

    class Meta:
        verbose_name = "Контакты и карта"
        verbose_name_plural = "Контакты и карта"

    def __str__(self) -> str:
        return "Контакты AlmaU"

    def get_address(self, language: str = 'ru') -> str:
        if language == 'en' and self.address_en:
            return self.address_en
        if language == 'kk' and self.address_kk:
            return self.address_kk
        return self.address

    def get_campus_items(self, language: str = 'ru') -> list[str]:
        text = self.campus_items
        if language == 'en' and self.campus_items_en:
            text = self.campus_items_en
        elif language == 'kk' and self.campus_items_kk:
            text = self.campus_items_kk
        return [line.strip() for line in text.splitlines() if line.strip()]
    
    def get_campus_3d_button_text(self, language: str = 'ru') -> str:
        if language == 'en' and self.campus_3d_button_text_en:
            return self.campus_3d_button_text_en
        if language == 'kk' and self.campus_3d_button_text_kk:
            return self.campus_3d_button_text_kk
        return self.campus_3d_button_text or "Изучить кампус в 3D"

class Leader(models.Model):
    """Модель для руководства университета"""
    ROLE_CHOICES = [
        ('rector', 'Ректор'),
        ('prorector', 'Проректор'),
        ('other', 'Другое')
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Должность")
    full_name = models.CharField(max_length=200, verbose_name="Имя и фамилия")
    photo = models.ImageField(upload_to='leaders/', blank=True, verbose_name="Фото")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Руководитель университета"
        verbose_name_plural = "Руководство университета"
        ordering = ['order', 'role']

    def __str__(self):
        return f"{self.get_role_display()} — {self.full_name}"


class LessonCategory(models.Model):
    """Категории уроков"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Название (English)")
    name_kk = models.CharField(max_length=100, blank=True, verbose_name="Название (Қазақша)")

    description = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание (English)")
    description_kk = models.TextField(blank=True, verbose_name="Описание (Қазақша)")
    order_index = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория уроков"
        verbose_name_plural = "Категории уроков"
        ordering = ['order_index', 'name']

    def __str__(self):
        return self.name

    def get_name(self, language: str = 'ru') -> str:
        if language == 'en' and self.name_en:
            return self.name_en
        if language == 'kk' and self.name_kk:
            return self.name_kk
        return self.name

    def get_description(self, language: str = 'ru') -> str:
        if language == 'en' and self.description_en:
            return self.description_en
        if language == 'kk' and self.description_kk:
            return self.description_kk
        return self.description


class Lesson(models.Model):
    """Модель урока с поддержкой видео и PDF"""
    title = models.CharField(max_length=200, verbose_name="Название урока")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название (English)")
    title_kk = models.CharField(max_length=200, blank=True, verbose_name="Название (Қазақша)")

    description = models.TextField(verbose_name="Описание урока")
    description_en = models.TextField(blank=True, verbose_name="Описание (English)")
    description_kk = models.TextField(blank=True, verbose_name="Описание (Қазақша)")
    
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE, verbose_name="Категория", null=True, blank=True)

    # Видео файл (опционально)
    video = models.FileField(
        upload_to='lessons/videos/', 
        blank=True, 
        null=True,
        verbose_name="Видео файл",
        help_text="Поддерживаемые форматы: MP4, AVI, MOV, WMV"
    )
    
    # PDF файл (опционально)
    pdf_file = models.FileField(
        upload_to='lessons/pdfs/', 
        blank=True, 
        null=True,
        verbose_name="PDF файл",
        help_text="PDF файл будет автоматически конвертирован в слайды"
    )

    # Дополнительные поля (длительность убрана - рассчитывается автоматически)
    
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Начинающий'),
            ('intermediate', 'Средний'),
            ('advanced', 'Продвинутый')
        ],
        default='beginner',
        verbose_name="Уровень сложности"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    # Автор урока
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Автор урока",
        help_text="Редактор или администратор, создавший урок"
    )

    # Пользователи, завершившие урок
    completed_users = models.ManyToManyField(
        User, 
        through='LessonCompletion',
        related_name='completed_lessons',
        verbose_name="Завершившие пользователи"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_title(self, language: str = 'ru') -> str:
        if language == 'en' and self.title_en:
            return self.title_en
        if language == 'kk' and self.title_kk:
            return self.title_kk
        return self.title

    def get_description(self, language: str = 'ru') -> str:
        if language == 'en' and self.description_en:
            return self.description_en
        if language == 'kk' and self.description_kk:
            return self.description_kk
        return self.description

    def calculate_duration(self) -> int:
        """Автоматически рассчитывает длительность урока в минутах"""
        total_duration = 0
        
        # Расчет длительности видео (упрощенный)
        if self.video:
            # Используем фиксированную длительность для видео
            # В будущем можно добавить более точный расчет
            total_duration += 10  # 10 минут по умолчанию для видео
        
        # Расчет длительности PDF (2 слайда = 1 минута)
        if self.pdf_file:
            try:
                # Пытаемся использовать PyMuPDF, если доступен
                try:
                    import fitz  # PyMuPDF
                    pdf_path = self.pdf_file.path
                    doc = fitz.open(pdf_path)
                    slide_count = len(doc)
                    pdf_minutes = max(1, slide_count // 2)  # Минимум 1 минута
                    total_duration += pdf_minutes
                    doc.close()
                except ImportError:
                    # Если PyMuPDF не установлен, используем фиксированную длительность
                    total_duration += 5  # 5 минут по умолчанию для PDF
            except Exception as e:
                # Если произошла ошибка, используем фиксированную длительность
                total_duration += 5  # 5 минут по умолчанию для PDF
        
        return max(1, total_duration)  # Минимум 1 минута

    @property
    def duration(self) -> int:
        """Свойство для получения длительности урока"""
        return self.calculate_duration()

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматической конвертации PDF"""
        is_new = self.pk is None
        had_pdf = False
        
        # Проверяем, был ли PDF до сохранения
        if not is_new:
            try:
                old_instance = Lesson.objects.get(pk=self.pk)
                had_pdf = old_instance.pdf_file != self.pdf_file
            except Lesson.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # Конвертируем PDF в слайды если:
        # 1. Это новый урок с PDF
        # 2. PDF был изменен
        # 3. Есть PDF, но нет слайдов
        if (is_new and self.pdf_file) or had_pdf or (self.pdf_file and not self.slides.exists()):
            try:
                success = self.convert_pdf_to_slides()
                if success:
                    print(f"PDF успешно конвертирован в {self.slides.count()} слайдов для урока '{self.title}'")
                else:
                    print(f"Ошибка при конвертации PDF для урока '{self.title}'")
            except Exception as e:
                print(f"Исключение при конвертации PDF для урока '{self.title}': {e}")

    def has_video(self) -> bool:
        """Проверяет, есть ли видео у урока"""
        return bool(self.video)

    def has_pdf(self) -> bool:
        """Проверяет, есть ли PDF у урока (но он должен быть конвертирован в слайды)"""
        return bool(self.pdf_file)

    def get_primary_content_type(self):
        """Возвращает основной тип контента для отображения"""
        if self.has_video():
            return 'video'
        elif self.has_slides():
            return 'slides'
        else:
            return 'none'

    def should_show_slides(self):
        """Определяет, нужно ли показывать слайды вместо PDF"""
        return self.has_slides() or self.has_pdf()

    def get_file_extension(self) -> str:
        """Возвращает расширение файла"""
        if self.video:
            return self.video.name.split('.')[-1].lower()
        elif self.pdf_file:
            return 'pdf'
        return ''

    def has_slides(self) -> bool:
        """Проверяет, есть ли слайды у урока"""
        return self.slides.exists()

    def get_slides(self):
        """Возвращает все слайды урока в правильном порядке"""
        return self.slides.all().order_by('order')

    def get_file_size_mb(self) -> float:
        """Возвращает размер файла в МБ"""
        if self.video and self.video.storage.exists(self.video.name):
            return round(self.video.size / (1024 * 1024), 2)
        elif self.pdf_file and self.pdf_file.storage.exists(self.pdf_file.name):
            return round(self.pdf_file.size / (1024 * 1024), 2)
        return 0.0

    def is_completed_by_user(self, user) -> bool:
        """Проверяет, завершил ли пользователь этот урок"""
        return self.completed_users.filter(id=user.id).exists()

    def mark_as_completed(self, user):
        """Отмечает урок как завершенный пользователем"""
        LessonCompletion.objects.get_or_create(
            lesson=self,
            user=user
        )

    def get_or_create_progress(self, user):
        """Получает или создает прогресс для пользователя"""
        progress, created = LessonProgress.objects.get_or_create(
            lesson=self,
            user=user,
            defaults={
                'pdf_total_pages': 1  # Будет обновлено при загрузке PDF
            }
        )
        return progress

    def can_be_completed_by_user(self, user):
        """Проверяет, может ли пользователь завершить урок"""
        if self.is_completed_by_user(user):
            return False
        
        progress = self.get_or_create_progress(user)
        return progress.is_ready_to_complete

    def convert_pdf_to_slides(self):
        """Автоматически конвертирует PDF в слайды"""
        if not self.pdf_file:
            return False
        
        try:
            import fitz  # PyMuPDF
            from PIL import Image
            import io
            from django.core.files.base import ContentFile
            
            # Удаляем существующие слайды
            self.slides.all().delete()
            
            # Открываем PDF
            pdf_document = fitz.open(self.pdf_file.path)
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                
                # Рендерим страницу как изображение
                mat = fitz.Matrix(2.0, 2.0)  # Увеличиваем разрешение
                pix = page.get_pixmap(matrix=mat)
                
                # Конвертируем в PIL Image
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Создаем слайд
                slide = LessonSlide.objects.create(
                    lesson=self,
                    order=page_num + 1,
                    title=f"Страница {page_num + 1}",
                    description=f"Страница {page_num + 1} из {pdf_document.page_count}"
                )
                
                # Сохраняем изображение
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                
                slide.image.save(
                    f'slide_{page_num + 1}.png',
                    ContentFile(img_io.getvalue()),
                    save=True
                )
            
            pdf_document.close()
            return True
            
        except ImportError:
            # Если PyMuPDF не установлен, используем альтернативный метод
            return self.convert_pdf_to_slides_alternative()
        except Exception as e:
            print(f"Ошибка конвертации PDF: {e}")
            return False

    def convert_pdf_to_slides_alternative(self):
        """Альтернативный метод конвертации PDF (без PyMuPDF)"""
        if not self.pdf_file:
            return False
        
        try:
            from pdf2image import convert_from_path
            from django.core.files.base import ContentFile
            import io
            
            # Удаляем существующие слайды
            self.slides.all().delete()
            
            # Конвертируем PDF в изображения
            images = convert_from_path(self.pdf_file.path, dpi=150)
            
            for i, image in enumerate(images):
                # Создаем слайд
                slide = LessonSlide.objects.create(
                    lesson=self,
                    order=i + 1,
                    title=f"Страница {i + 1}",
                    description=f"Страница {i + 1} из {len(images)}"
                )
                
                # Сохраняем изображение
                img_io = io.BytesIO()
                image.save(img_io, format='PNG')
                img_io.seek(0)
                
                slide.image.save(
                    f'slide_{i + 1}.png',
                    ContentFile(img_io.getvalue()),
                    save=True
                )
            
            return True
            
        except ImportError:
            print("Необходимо установить PyMuPDF или pdf2image для конвертации PDF")
            return False
        except Exception as e:
            print(f"Ошибка альтернативной конвертации PDF: {e}")
            return False

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматической конвертации PDF"""
        is_new = self.pk is None
        had_pdf = False
        
        # Проверяем, был ли PDF до сохранения
        if not is_new:
            try:
                old_instance = Lesson.objects.get(pk=self.pk)
                had_pdf = old_instance.pdf_file != self.pdf_file
            except Lesson.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # Конвертируем PDF в слайды если:
        # 1. Это новый урок с PDF
        # 2. PDF был изменен
        # 3. Есть PDF, но нет слайдов
        if (is_new and self.pdf_file) or had_pdf or (self.pdf_file and not self.slides.exists()):
            try:
                success = self.convert_pdf_to_slides()
                if success:
                    print(f"PDF успешно конвертирован в {self.slides.count()} слайдов для урока '{self.title}'")
                else:
                    print(f"Ошибка при конвертации PDF для урока '{self.title}'")
            except Exception as e:
                print(f"Исключение при конвертации PDF для урока '{self.title}': {e}")

    def has_video(self) -> bool:
        """Проверяет, есть ли видео у урока"""
        return bool(self.video)

    def has_pdf(self) -> bool:
        """Проверяет, есть ли PDF у урока (но он должен быть конвертирован в слайды)"""
        return bool(self.pdf_file)

    def has_slides(self) -> bool:
        """Проверяет, есть ли слайды у урока"""
        return self.slides.exists()

    def get_primary_content_type(self):
        """Возвращает основной тип контента для отображения"""
        if self.has_video():
            return 'video'
        elif self.has_slides():
            return 'slides'
        else:
            return 'none'

    def should_show_slides(self):
        """Определяет, нужно ли показывать слайды вместо PDF"""
        return self.has_slides() or self.has_pdf()


class LessonSlide(models.Model):
    """Модель слайда урока"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='slides', verbose_name="Урок")
    image = models.ImageField(upload_to='lessons/slides/', verbose_name="Изображение слайда")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    title = models.CharField(max_length=200, blank=True, verbose_name="Название слайда")
    description = models.TextField(blank=True, verbose_name="Описание слайда")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Слайд урока"
        verbose_name_plural = "Слайды уроков"
        ordering = ['lesson', 'order']
        unique_together = ['lesson', 'order']

    def __str__(self):
        return f"Слайд {self.order} - {self.lesson.title}"


class LessonCompletion(models.Model):
    """Модель для отслеживания завершения уроков пользователями"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Урок")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата завершения")

    class Meta:
        verbose_name = "Завершение урока"
        verbose_name_plural = "Завершения уроков"
        unique_together = ['lesson', 'user']  # Пользователь может завершить урок только один раз
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} завершил {self.lesson.title}"


class LessonProgress(models.Model):
    """Прогресс пользователя по уроку"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress', verbose_name="Урок")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress', verbose_name="Пользователь")
    
    # Прогресс видео
    video_watched = models.BooleanField(default=False, verbose_name="Видео просмотрено")
    video_current_time = models.FloatField(default=0.0, verbose_name="Текущее время видео (секунды)")
    video_total_time = models.FloatField(default=0.0, verbose_name="Общее время видео (секунды)")
    video_max_progress_percent = models.FloatField(default=0.0, verbose_name="Максимальный прогресс видео (%)")
    video_last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление видео")
    
    # Прогресс PDF/слайдов
    pdf_completed = models.BooleanField(default=False, verbose_name="PDF/слайды завершены")
    pdf_current_page = models.PositiveIntegerField(default=1, verbose_name="Текущая страница PDF")
    pdf_total_pages = models.PositiveIntegerField(default=1, verbose_name="Всего страниц PDF")
    pdf_last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление PDF")
    
    # Прогресс слайдов
    slides_current_slide = models.PositiveIntegerField(default=1, verbose_name="Текущий слайд")
    slides_total_slides = models.PositiveIntegerField(default=1, verbose_name="Всего слайдов")
    slides_max_progress_percent = models.FloatField(default=0.0, verbose_name="Максимальный прогресс слайдов (%)")
    slides_completed = models.BooleanField(default=False, verbose_name="Слайды завершены")
    slides_last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление слайдов")
    
    # Общий прогресс
    is_ready_to_complete = models.BooleanField(default=False, verbose_name="Готов к завершению")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Прогресс урока"
        verbose_name_plural = "Прогресс уроков"
        unique_together = ['lesson', 'user']
        ordering = ['-last_activity']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

    def update_video_progress(self, current_time, total_time, max_progress_percent=None):
        """Обновляет прогресс видео"""
        self.video_current_time = current_time
        self.video_total_time = total_time
        
        # Обновляем максимальный прогресс
        if max_progress_percent is not None:
            self.video_max_progress_percent = max(self.video_max_progress_percent, max_progress_percent)
        
        # Видео считается просмотренным, если максимальный прогресс >= 100%
        self.video_watched = self.video_max_progress_percent >= 100
        
        self.video_last_updated = timezone.now()
        self.last_activity = timezone.now()
        self.check_completion_ready()
        self.save()

    def update_pdf_progress(self, current_page, total_pages):
        """Обновляет прогресс PDF"""
        self.pdf_current_page = current_page
        self.pdf_total_pages = total_pages
        self.pdf_completed = current_page >= total_pages
        self.pdf_last_updated = timezone.now()
        self.last_activity = timezone.now()
        self.check_completion_ready()
        self.save()

    def update_slides_progress(self, current_slide, total_slides):
        """Обновляет прогресс слайдов"""
        self.slides_current_slide = current_slide
        self.slides_total_slides = total_slides
        
        # Обновляем максимальный прогресс
        if total_slides > 0:
            current_progress_percent = (current_slide / total_slides) * 100
            self.slides_max_progress_percent = max(self.slides_max_progress_percent, current_progress_percent)
        
        # Слайды считаются завершенными, если максимальный прогресс >= 100%
        self.slides_completed = self.slides_max_progress_percent >= 100
        self.slides_last_updated = timezone.now()
        self.last_activity = timezone.now()
        self.check_completion_ready()
        self.save()

    def check_completion_ready(self):
        """Проверяет, готов ли урок к завершению"""
        lesson = self.lesson

        # Если есть только видео
        if lesson.has_video() and not lesson.has_pdf() and not lesson.has_slides():
            self.is_ready_to_complete = self.video_watched

        # Если есть только PDF
        elif lesson.has_pdf() and not lesson.has_video() and not lesson.has_slides():
            self.is_ready_to_complete = self.pdf_completed

        # Если есть только слайды
        elif lesson.has_slides() and not lesson.has_video() and not lesson.has_pdf():
            self.is_ready_to_complete = self.slides_completed

        # Если есть видео и PDF
        elif lesson.has_video() and lesson.has_pdf() and not lesson.has_slides():
            self.is_ready_to_complete = self.video_watched and self.pdf_completed

        # Если есть видео и слайды
        elif lesson.has_video() and lesson.has_slides() and not lesson.has_pdf():
            self.is_ready_to_complete = self.video_watched and self.slides_completed

        # Если есть PDF и слайды
        elif lesson.has_pdf() and lesson.has_slides() and not lesson.has_video():
            self.is_ready_to_complete = self.pdf_completed and self.slides_completed

        # Если есть все три типа контента
        elif lesson.has_video() and lesson.has_pdf() and lesson.has_slides():
            self.is_ready_to_complete = self.video_watched and self.pdf_completed and self.slides_completed

        # Если нет ни видео, ни PDF, ни слайдов
        else:
            self.is_ready_to_complete = True
        
        # Автоматически завершаем урок, если он готов к завершению и еще не завершен
        if self.is_ready_to_complete and not self.lesson.is_completed_by_user(self.user):
            self.lesson.mark_as_completed(self.user)

    def get_video_progress_percentage(self):
        """Возвращает максимальный процент прогресса видео"""
        return min(100, self.video_max_progress_percent)

    def get_pdf_progress_percentage(self):
        """Возвращает процент прогресса PDF"""
        if self.pdf_total_pages > 0:
            return min(100, (self.pdf_current_page / self.pdf_total_pages) * 100)
        return 0

    def get_slides_progress_percentage(self):
        """Возвращает максимальный процент прогресса слайдов"""
        return min(100, self.slides_max_progress_percent)

    def get_overall_progress_percentage(self):
        """Возвращает общий процент прогресса урока"""
        lesson = self.lesson
        total_progress = 0
        content_count = 0

        # Если есть видео
        if lesson.has_video():
            video_progress = self.get_video_progress_percentage()
            total_progress += video_progress
            content_count += 1
            print(f"DEBUG: Video progress: {video_progress}%")

        # Если есть PDF
        if lesson.has_pdf():
            pdf_progress = self.get_pdf_progress_percentage()
            total_progress += pdf_progress
            content_count += 1
            print(f"DEBUG: PDF progress: {pdf_progress}%")

        # Если есть слайды
        if lesson.has_slides():
            slides_progress = self.get_slides_progress_percentage()
            total_progress += slides_progress
            content_count += 1
            print(f"DEBUG: Slides progress: {slides_progress}%")

        # Если нет контента, возвращаем 0
        if content_count == 0:
            print(f"DEBUG: No content found")
            return 0

        # Возвращаем средний прогресс
        average_progress = total_progress / content_count
        print(f"DEBUG: Total progress: {total_progress}, Content count: {content_count}, Average: {average_progress}%")
        return min(100, average_progress)

    def get_formatted_video_time(self):
        """Возвращает отформатированное время видео"""
        current_minutes = int(self.video_current_time // 60)
        current_seconds = int(self.video_current_time % 60)
        total_minutes = int(self.video_total_time // 60)
        total_seconds = int(self.video_total_time % 60)
        return f"{current_minutes:02d}:{current_seconds:02d} / {total_minutes:02d}:{total_seconds:02d}"

    def get_remaining_video_time(self):
        """Возвращает оставшееся время видео в секундах"""
        return max(0, self.video_total_time - self.video_current_time)

    @property
    def is_completed(self):
        """Проверяет, завершен ли урок пользователем"""
        return self.lesson.is_completed_by_user(self.user)

class Editor(models.Model):
    """Модель редактора - пользователя, который может создавать уроки"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    email = models.EmailField(unique=True, verbose_name="Email")
    department = models.CharField(max_length=200, blank=True, verbose_name="Кафедра/Отдел")
    position = models.CharField(max_length=200, blank=True, verbose_name="Должность")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    bio = models.TextField(blank=True, verbose_name="Биография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Редактор"
        verbose_name_plural = "Редакторы"
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем имя пользователя если не задано
        if not self.user.first_name and self.full_name:
            self.user.first_name = self.full_name.split()[0] if self.full_name.split() else ''
        if not self.user.last_name and len(self.full_name.split()) > 1:
            self.user.last_name = ' '.join(self.full_name.split()[1:])
        
        # Устанавливаем email пользователя
        if self.user.email != self.email:
            self.user.email = self.email
        
        # Сохраняем пользователя
        self.user.save()
        
        super().save(*args, **kwargs)

    def get_created_lessons_count(self):
        """Возвращает количество созданных уроков"""
        return Lesson.objects.filter(created_by=self.user).count()

    def get_lessons(self):
        """Возвращает все уроки, созданные этим редактором"""
        return Lesson.objects.filter(created_by=self.user)

    @property
    def is_verified(self):
        """Проверяет, верифицирован ли редактор"""
        return self.is_active and self.user.is_active
