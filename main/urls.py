from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('documents/', views.documents_view, name='documents'),
    path('api/documents/search/', views.documents_api_search, name='documents_api_search'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
    path('logout/', views.logout_view, name='logout'),
    path('lessons/', views.lessons_view, name='lessons'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson_view, name='complete_lesson'),
    path('lessons/<int:lesson_id>/progress/', views.get_lesson_progress_view, name='get_lesson_progress'),
    path('lessons/<int:lesson_id>/progress/video/', views.update_video_progress_view, name='update_video_progress'),
    path('lessons/<int:lesson_id>/progress/pdf/', views.update_pdf_progress_view, name='update_pdf_progress'),
    path('lessons/<int:lesson_id>/slides/', views.get_lesson_slides_view, name='get_lesson_slides'),
    path('lessons/<int:lesson_id>/progress/slides/', views.update_slides_progress_view, name='update_slides_progress'),
    path('lessons/<int:lesson_id>/convert-pdf/', views.convert_pdf_to_slides_view, name='convert_pdf_to_slides'),
    path('admin-panel/employee-progress/', views.employee_progress_view, name='employee_progress'),
    path('admin-panel/lesson-progress/<int:lesson_id>/', views.lesson_progress_detail_view, name='lesson_progress_detail'),
    path('map/', views.map_view, name='map'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('faq/', views.faq_view, name='faq'),
    path('api/faq/search/', views.faq_api_search, name='faq_api_search'),
    path('api/faq/<int:faq_id>/views/', views.faq_increment_views, name='faq_increment_views'),

    path('settings/', views.settings_view, name='settings'),
    path('set-language/', views.set_language_view, name='set_language'),
    
    # Admin Panel URLs
    path('admin-panel/', views.admin_login_view, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout_view, name='admin_logout'),
    
    # Admin Panel - Content Management
    path('admin-panel/about/', views.admin_about_view, name='admin_about'),
    path('admin-panel/map/', views.admin_map_view, name='admin_map'),
    path('admin-panel/faq/', views.admin_faq_view, name='admin_faq'),
    path('admin-panel/feedback/', views.admin_feedback_view, name='admin_feedback'),
    path('admin-panel/lessons/', views.admin_lessons_view, name='admin_lessons'),
    path('admin-panel/lessons/<int:lesson_id>/data/', views.get_lesson_data, name='get_lesson_data'),

    path('admin-panel/teachers/', views.admin_teachers_view, name='admin_teachers'),
    path('admin-panel/leaders/', views.admin_leaders_view, name='admin_leaders'),
    path('admin-panel/users/', views.admin_users_view, name='admin_users'),
    path('admin-panel/users/<int:user_id>/progress/', views.admin_user_progress_view, name='admin_user_progress'),
    # Документы
    path('admin-panel/documents/', views.admin_documents_view, name='admin_documents'),
    path('admin-panel/documents/<int:document_id>/edit/', views.admin_document_edit_view, name='edit_document'),
    path('admin-panel/documents/<int:document_id>/delete/', views.admin_document_delete_view, name='delete_document'),
    path('admin-panel/document-categories/add/', views.admin_document_category_add_view, name='admin_document_category_add'),
    
    # FAQ
    path('admin-panel/faq/<int:faq_id>/edit/', views.admin_faq_edit_view, name='edit_faq'),
    path('admin-panel/faq/<int:faq_id>/delete/', views.admin_faq_delete_view, name='delete_faq'),
    
    # Настройки темы
    path('set-theme/', views.set_theme_view, name='set_theme'),
    
    # Test theme page
    path('test-theme/', views.test_theme_view, name='test_theme'),
    
    # Simple test theme page
    path('test-simple/', views.test_simple_view, name='test_simple'),
    
    # Удаляем тестовые URL для входа в админ панель
    
    # Editor URLs
    path('editor/', views.editor_login_view, name='editor_login'),
    path('editor/logout/', views.editor_logout_view, name='editor_logout'),
    path('editor/dashboard/', views.editor_dashboard_view, name='editor_dashboard'),
    path('editor/lessons/', views.editor_lessons_view, name='editor_lessons'),
    path('editor/lessons/create/', views.editor_create_lesson_view, name='editor_create_lesson'),
    path('editor/lessons/<int:lesson_id>/edit/', views.editor_edit_lesson_view, name='editor_edit_lesson'),
    path('editor/documents/', views.editor_documents_view, name='editor_documents'),
    path('editor/documents/create/', views.editor_create_document_view, name='editor_create_document'),
    path('editor/documents/<int:document_id>/edit/', views.editor_edit_document_view, name='editor_edit_document'),
    path('editor/feedback/', views.editor_feedback_view, name='editor_feedback'),
    path('editor/progress/', views.editor_progress_view, name='editor_progress'),
    path('editor/progress/lesson/<int:lesson_id>/', views.editor_lesson_progress_detail_view, name='editor_lesson_progress_detail'),
    
    # Admin Panel - Editors Management
    path('admin-panel/editors/', views.admin_editors_view, name='admin_editors'),
    
]
