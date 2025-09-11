from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Teacher, Document, DocumentCategory, Instruction, Process, Feedback, FAQ, FAQCategory, History, Mission, Values, Leader, ContactInfo, Lesson, LessonCompletion, LessonProgress, LessonCategory, LessonSlide

class TeacherInline(admin.StackedInline):
    """Inline для отображения информации о преподавателе в админке пользователя"""
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Информация о преподавателе'
    fields = ('full_name', 'department', 'position', 'phone', 'office', 'is_active')

class UserAdmin(BaseUserAdmin):
    """Расширенная админка пользователя с информацией о преподавателе"""
    inlines = (TeacherInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Админка для модели преподавателя"""
    list_display = ('full_name', 'get_email', 'department', 'position', 'is_active', 'created_at')
    list_filter = ('department', 'position', 'is_active', 'created_at')
    search_fields = ('full_name', 'user__email', 'department', 'position')
    list_editable = ('is_active',)
    ordering = ('full_name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'full_name', 'is_active')
        }),
        ('Профессиональная информация', {
            'fields': ('department', 'position', 'office')
        }),
        ('Контактная информация', {
            'fields': ('phone',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

# Перерегистрируем стандартную админку пользователя
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class AboutUniversityAdmin(admin.ModelAdmin):
    """Админка для информации об университете"""
    list_display = ('title', 'is_active', 'order', 'created_at', 'updated_at')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'content', 'title_en', 'content_en', 'title_kk', 'content_kk')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Русская версия', {
            'fields': ('title', 'content')
        }),
        ('Английская версия', {
            'fields': ('title_en', 'content_en'),
            'classes': ('collapse',)
        }),
        ('Казахская версия', {
            'fields': ('title_kk', 'content_kk'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # При сохранении, если английская или казахская версия не заполнены,
        # копируем русскую версию
        if not obj.title_en:
            obj.title_en = obj.title
        if not obj.content_en:
            obj.content_en = obj.content
        if not obj.title_kk:
            obj.title_kk = obj.title
        if not obj.content_kk:
            obj.content_kk = obj.content
        super().save_model(request, obj, form, change)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Русский', {'fields': ('text',)}),
        ('English', {'fields': ('text_en',), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('text_kk',), 'classes': ('collapse',)}),
        ('Изображение', {'fields': ('image',)})
    )

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Русский', {'fields': ('text',)}),
        ('English', {'fields': ('text_en',), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('text_kk',), 'classes': ('collapse',)})
    )

@admin.register(Values)
class ValuesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Русский', {'fields': ('text',)}),
        ('English', {'fields': ('text_en',), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('text_kk',), 'classes': ('collapse',)})
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Адрес', {'fields': ('address', 'address_en', 'address_kk', 'phone')}),
        ('Кампус', {'fields': ('campus_items', 'campus_items_en', 'campus_items_kk', 'campus_image')}),
        ('3D Кампус', {'fields': ('campus_3d_enabled', 'campus_3d_url', 'campus_3d_button_text', 'campus_3d_button_text_en', 'campus_3d_button_text_kk')}),
        ('IT Поддержка', {'fields': ('it_support_enabled', 'it_support_url')})
    )

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    """Админка для категорий документов"""
    list_display = ('name', 'order_index', 'description', 'get_documents_count', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    list_editable = ('order_index',)
    list_display_links = ('name',)
    
    def get_documents_count(self, obj):
        return obj.document_set.count()
    get_documents_count.short_description = 'Количество документов'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Админка для документов"""
    list_display = ('title', 'category', 'get_file_extension', 'get_file_size', 'download_count', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'uploaded_by')
    search_fields = ('title', 'description', 'title_en', 'title_kk', 'description_en', 'description_kk')
    readonly_fields = ('uploaded_by', 'created_at', 'updated_at', 'download_count')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Русский язык', {
            'fields': ('title', 'description', 'file')
        }),
        ('English', {
            'fields': ('title_en', 'description_en', 'file_en'),
            'classes': ('collapse',)
        }),
        ('Қазақша', {
            'fields': ('title_kk', 'description_kk', 'file_kk'),
            'classes': ('collapse',)
        }),
        ('Общие настройки', {
            'fields': ('category', 'is_active')
        }),
        ('Служебная информация', {
            'fields': ('uploaded_by', 'download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если это новый объект
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_file_extension(self, obj):
        return obj.get_file_extension()
    get_file_extension.short_description = 'Тип файла'
    
    def get_file_size(self, obj):
        return obj.get_file_size()
    get_file_size.short_description = 'Размер файла'

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'title_en', 'title_kk', 'description_en', 'description_kk')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Русский', {'fields': ('title', 'description')}),
        ('English', {'fields': ('title_en', 'description_en'), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('title_kk', 'description_kk'), 'classes': ('collapse',)}),
        ('Служебное', {'fields': ('is_active', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'title_en', 'title_kk', 'description_en', 'description_kk')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Русский', {'fields': ('title', 'description')}),
        ('English', {'fields': ('title_en', 'description_en'), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('title_kk', 'description_kk'), 'classes': ('collapse',)}),
        ('Служебное', {'fields': ('is_active', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Админка для обратной связи"""
    list_display = ('subject', 'get_user_name', 'recipient', 'feedback_type', 'status', 'created_at')
    list_filter = ('recipient', 'feedback_type', 'status', 'created_at')
    search_fields = ('subject', 'message', 'email', 'user__username', 'user__first_name')
    readonly_fields = ('user', 'created_at', 'updated_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Информация об обращении', {
            'fields': ('recipient', 'feedback_type', 'subject', 'message', 'status')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone')
        }),
        ('Прикрепленный файл', {
            'fields': ('file',),
            'classes': ('collapse',)
        }),
        ('Служебная информация', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        try:
            teacher = obj.user.teacher
            return teacher.full_name
        except:
            return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'Пользователь'
    get_user_name.admin_order_field = 'user__username'
    
    def has_delete_permission(self, request, obj=None):
        # Ограничиваем удаление обращений
        return request.user.is_superuser

@admin.register(LessonCategory)
class LessonCategoryAdmin(admin.ModelAdmin):
    """Админка для категорий уроков"""
    list_display = ('name', 'order_index', 'is_active', 'get_lesson_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'name_en', 'name_kk', 'description_en', 'description_kk')
    readonly_fields = ('created_at',)
    list_editable = ('order_index', 'is_active')
    list_display_links = ('name',)
    
    fieldsets = (
        ('Русский', {'fields': ('name', 'description')}),
        ('English', {'fields': ('name_en', 'description_en'), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('name_kk', 'description_kk'), 'classes': ('collapse',)}),
        ('Статусы', {'fields': ('is_active',)}),
        ('Сортировка', {
            'fields': ('order_index',)
        }),
        ('Служебная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_lesson_count(self, obj):
        return obj.lesson_set.filter(is_active=True).count()
    get_lesson_count.short_description = 'Количество уроков'
    get_lesson_count.admin_order_field = 'lesson_count'


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    """Админка для категорий FAQ"""
    list_display = ('name', 'order_index', 'is_active', 'get_faq_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'name_en', 'name_kk', 'description_en', 'description_kk')
    readonly_fields = ('created_at',)
    list_editable = ('order_index', 'is_active')
    list_display_links = ('name',)
    
    fieldsets = (
        ('Русский', {'fields': ('name', 'description')}),
        ('English', {'fields': ('name_en', 'description_en'), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('name_kk', 'description_kk'), 'classes': ('collapse',)}),
        ('Статусы', {'fields': ('is_active',)}),
        ('Сортировка', {
            'fields': ('order_index',)
        }),
        ('Служебная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_faq_count(self, obj):
        return obj.faq_set.filter(is_active=True).count()
    get_faq_count.short_description = 'Количество вопросов'
    get_faq_count.admin_order_field = 'faq_count'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Админка для часто задаваемых вопросов"""
    list_display = ('question', 'category', 'is_active', 'is_popular', 'views_count', 'order_index', 'created_at')
    list_filter = ('category', 'is_active', 'is_popular', 'created_at')
    search_fields = ('question', 'answer', 'question_en', 'question_kk', 'answer_en', 'answer_kk')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    list_editable = ('is_active', 'is_popular', 'order_index')
    list_display_links = ('question',)
    
    fieldsets = (
        ('Русский', {'fields': ('question', 'answer')}),
        ('English', {'fields': ('question_en', 'answer_en'), 'classes': ('collapse',)}),
        ('Қазақша', {'fields': ('question_kk', 'answer_kk'), 'classes': ('collapse',)}),
        ('Категория', {'fields': ('category',)}),
        ('Настройки отображения', {
            'fields': ('is_active', 'is_popular', 'order_index')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        # Оптимизируем запросы, добавляя связанные объекты
        return super().get_queryset(request).select_related('category')
    
    actions = ['mark_as_popular', 'mark_as_not_popular', 'activate_faqs', 'deactivate_faqs']
    
    def mark_as_popular(self, request, queryset):
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'{updated} вопросов отмечено как популярные.')
    mark_as_popular.short_description = 'Отметить как популярные'
    
    def mark_as_not_popular(self, request, queryset):
        updated = queryset.update(is_popular=False)
        self.message_user(request, f'{updated} вопросов убрано из популярных.')
    mark_as_not_popular.short_description = 'Убрать из популярных'
    
    def activate_faqs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} вопросов активировано.')
    activate_faqs.short_description = 'Активировать вопросы'
    
    def deactivate_faqs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} вопросов деактивировано.')
    deactivate_faqs.short_description = 'Деактивировать вопросы'

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'order', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('full_name',)
    list_editable = ('order', 'is_active')
    ordering = ('order', 'role')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('role', 'full_name', 'photo', 'is_active')
        }),
        ('Сортировка', {
            'fields': ('order',)
        }),
    )


@admin.register(LessonSlide)
class LessonSlideAdmin(admin.ModelAdmin):
    """Админка для слайдов уроков"""
    list_display = ('lesson', 'order', 'title', 'preview_image', 'created_at')
    list_filter = ('lesson__category', 'created_at')
    search_fields = ('lesson__title', 'title', 'description')
    list_editable = ('order',)
    ordering = ('lesson', 'order')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('lesson', 'order', 'title', 'description')
        }),
        ('Изображение', {
            'fields': ('image',),
            'description': 'Загрузите изображение слайда'
        }),
        ('Служебная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'preview_image')
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "Нет изображения"
    preview_image.short_description = 'Предварительный просмотр'
    
    def save_model(self, request, obj, form, change):
        # Автоматически устанавливаем порядок, если не задан
        if not obj.order:
            last_slide = LessonSlide.objects.filter(lesson=obj.lesson).order_by('-order').first()
            obj.order = (last_slide.order + 1) if last_slide else 1
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка для уроков"""
    list_display = ('title', 'category', 'difficulty_level', 'duration', 'has_video', 'has_pdf', 'has_slides', 'is_active', 'created_at')
    list_filter = ('category', 'difficulty_level', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'category__name')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'has_video', 'has_pdf', 'has_slides')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_en', 'title_kk', 'description', 'description_en', 'description_kk', 'category', 'difficulty_level', 'duration')
        }),
        ('Медиа файлы', {
            'fields': ('video', 'pdf_file'),
            'description': 'Можно загрузить видео ИЛИ PDF, или оба файла. Слайды создаются отдельно.'
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_video(self, obj):
        return obj.has_video()
    has_video.boolean = True
    has_video.short_description = 'Видео'

    def has_pdf(self, obj):
        return obj.has_pdf()
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF'

    def has_slides(self, obj):
        return obj.has_slides()
    has_slides.boolean = True
    has_slides.short_description = 'Слайды'

    def save_model(self, request, obj, form, change):
        # При сохранении, если английская или казахская версия не заполнены,
        # копируем русскую версию
        if not obj.title_en:
            obj.title_en = obj.title
        if not obj.description_en:
            obj.description_en = obj.description
        if not obj.title_kk:
            obj.title_kk = obj.title
        if not obj.description_kk:
            obj.description_kk = obj.description
        
        super().save_model(request, obj, form, change)
        
        # Если загружен PDF, конвертируем его в слайды
        if obj.pdf_file and (change or form.files.get('pdf_file')):
            try:
                success = obj.convert_pdf_to_slides()
                if success:
                    slides_count = obj.slides.count()
                    self.message_user(request, f"PDF успешно конвертирован в {slides_count} слайдов")
                else:
                    self.message_user(request, "Ошибка при конвертации PDF в слайды", level='WARNING')
            except Exception as e:
                self.message_user(request, f"Ошибка при конвертации PDF: {str(e)}", level='ERROR')
        
        # Если есть PDF, но нет слайдов, конвертируем
        elif obj.pdf_file and not obj.slides.exists():
            try:
                success = obj.convert_pdf_to_slides()
                if success:
                    slides_count = obj.slides.count()
                    self.message_user(request, f"PDF автоматически конвертирован в {slides_count} слайдов")
                else:
                    self.message_user(request, "Ошибка при автоматической конвертации PDF", level='WARNING')
            except Exception as e:
                self.message_user(request, f"Ошибка при автоматической конвертации PDF: {str(e)}", level='ERROR')

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:lesson_id>/progress/',
                self.admin_site.admin_view(self.lesson_progress_view),
                name='lesson_progress',
            ),
        ]
        return custom_urls + urls

    def lesson_progress_view(self, request, lesson_id):
        """Просмотр прогресса по уроку"""
        from django.shortcuts import redirect
        return redirect('lesson_progress_detail', lesson_id=lesson_id)

    def changelist_view(self, request, extra_context=None):
        """Добавляем кнопку просмотра прогресса сотрудников"""
        extra_context = extra_context or {}
        extra_context['show_employee_progress_button'] = True
        return super().changelist_view(request, extra_context)


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    """Админка для завершений уроков"""
    list_display = ('lesson', 'user', 'completed_at')
    list_filter = ('completed_at', 'lesson__difficulty_level')
    search_fields = ('lesson__title', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('completed_at',)
    ordering = ('-completed_at',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """Админка для прогресса уроков"""
    list_display = ('lesson', 'user', 'video_watched', 'pdf_completed', 'is_ready_to_complete', 'updated_at')
    list_filter = ('video_watched', 'pdf_completed', 'is_ready_to_complete', 'updated_at')
    search_fields = ('lesson__title', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('lesson', 'user')
        }),
        ('Прогресс видео', {
            'fields': ('video_progress', 'video_watched')
        }),
        ('Прогресс PDF', {
            'fields': ('pdf_current_page', 'pdf_total_pages', 'pdf_completed')
        }),
        ('Статус', {
            'fields': ('is_ready_to_complete',)
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
