from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Instruction(models.Model):
    """Модель инструкции"""
    title = models.CharField(max_length=200, verbose_name="Название инструкции")
    description = models.TextField(verbose_name="Текст инструкции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Инструкция"
        verbose_name_plural = "Инструкции"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Process(models.Model):
    """Модель процесса"""
    title = models.CharField(max_length=200, verbose_name="Название процесса")
    description = models.TextField(verbose_name="Текст процесса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Процесс"
        verbose_name_plural = "Процессы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


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
    description = models.TextField(blank=True, verbose_name="Описание")
    order_index = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория документов"
        verbose_name_plural = "Категории документов"
        ordering = ['order_index', 'name']

    def __str__(self):
        return self.name

class Document(models.Model):
    """Модель документов"""
    title = models.CharField(max_length=200, verbose_name="Название документа")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, verbose_name="Категория")
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
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

    def increment_download_count(self):
        """Увеличивает счетчик скачиваний"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
