from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Teacher, Document, DocumentCategory, Instruction, Process

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
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_by', 'created_at', 'updated_at', 'download_count')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'file', 'is_active')
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
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
