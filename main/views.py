from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _, activate
from django.utils import timezone
from django.template.loader import render_to_string
from django.db.models import Q

# Import models
from .models import (
    History, Mission, Values, ContactInfo, 
    FAQCategory, FAQ, Process, Instruction, 
    Teacher, Feedback, Document, DocumentCategory, Leader, Lesson, LessonCompletion, LessonProgress, LessonCategory, Editor
)

# Import forms
from .forms import EditorLoginForm

# Простые переводы для тестирования
TRANSLATIONS = {
    'en': {
        'Главная': 'Home',
        'Об университете': 'About the university',
        'Документация': 'Documentation',
        'Уроки': 'Lessons',
        'Контакты и карта': 'Contacts and map',
        'Обратная связь': 'Feedback',
        'Часто задаваемые вопросы': 'Frequently asked questions',
        'Настройки': 'Settings',
        'Выход': 'Exit',
        'Доброе утро': 'Good morning',
        'Добрый день': 'Good afternoon',
        'Добрый вечер': 'Good evening',
        'Логин': 'Login',
        'Пароль': 'Password',
        'Забыли пароль?': 'Forgot password?',
        'Продолжить': 'Continue',
        'Язык успешно изменен': 'Language successfully changed',
        'Пользователь': 'User',
        '1. Кому направить?': '1. Who to address?',
        '2. Тип обращения': '2. Type of request',
        '3. Тема обращения': '3. Subject',
        'Введите тему своего обращения': 'Enter the subject of your request',
        '4. Сообщение': '4. Message',
        'Опишите ваше обращение как можно подробнее...': 'Describe your request in as much detail as possible...',
        '5. Прикрепите файл': '5. Attach file',
        'Загрузить файл': 'Upload file',
        '6. Ваши контакты': '6. Your contacts',
        'Почта': 'Email',
        'Номер телефона': 'Phone number',
        'Отправить': 'Send',
        'Процесс': 'Process',
        'Инструкция': 'Instruction',
        'Ничего не найдено': 'Nothing found',
        'Попробуйте изменить критерии поиска или выбрать другую категорию.': 'Try changing your search criteria or selecting a different category.',
        'В данный момент уроки отсутствуют': 'No lessons are currently available',
        'Если у вас есть предложения, замечания по работе сайта или вопросы — отправьте их через форму ниже. Мы ответим как можно быстрее.': 'If you have suggestions, comments about the site or questions - send them through the form below. We will respond as quickly as possible.',
        'Изучайте материалы в удобном формате': 'Study materials in a convenient format',
        'Начать поиск': 'Start search',
        'Начинающий': 'Beginner',
        'Средний': 'Intermediate',
        'Продвинутый': 'Advanced',
        'Скачать PDF': 'Download PDF',
        'Документы не найдены': 'No documents found',
        'Попробуйте изменить критерии поиска': 'Try changing your search criteria',
        'Уроки не найдены': 'No lessons found',
        'Попробуйте изменить критерии поиска или выбрать другой уровень сложности.': 'Try changing your search criteria or selecting a different difficulty level.',
        'Открыть': 'Open',
        'Скрыть': 'Hide',
        'Видео урока': 'Lesson Video',
        'Презентация урока': 'Lesson Presentation',
        'Ваш браузер не поддерживает видео': 'Your browser does not support video',
        'Ваш браузер не поддерживает PDF': 'Your browser does not support PDF',
        'В данный момент документы отсутствуют': 'No documents are currently available',
        'Завершить урок': 'Complete Lesson',
        'Завершен': 'Completed',
        'Изучите материал для завершения': 'Study the material to complete',
        'Задайте свой вопрос': 'Ask your question',
        'Поиск по вопросам': 'Search questions',
        'Категории': 'Categories',
        'HR': 'HR',
        'IT поддержка': 'IT Support',
        'Предложение': 'Suggestion',
        'Жалоба': 'Complaint',
        'Вопрос': 'Question',
        'Проблема с сайтом': 'Website Issue',
        'Пожалуйста, заполните все обязательные поля.': 'Please fill in all required fields.',
        'Ваше обращение успешно отправлено! Мы ответим как можно быстрее.': 'Your request has been sent successfully! We will respond as soon as possible.',
    },
    'kk': {
        'Главная': 'Басты бет',
        'Об университете': 'Университет туралы',
        'Документация': 'Құжаттама',
        'Уроки': 'Сабақтар',
        'Контакты и карта': 'Карта және контактілер',
        'Обратная связь': 'Кері байланыс',
        'Часто задаваемые вопросы': 'Жиі қойылатын сұрақтар',
        'Настройки': 'Настройки',
        'Выход': 'Шығу',
        'Доброе утро': 'Қайырлы таң',
        'Добрый день': 'Қайырлы күн',
        'Добрый вечер': 'Қайырлы кеш',
        'Логин': 'Логин',
        'Пароль': 'Құпия сөз',
        'Забыли пароль?': 'Құпия сөзді ұмыттыңыз ба?',
        'Продолжить': 'Жалғастыру',
        'Язык успешно изменен': 'Тіл сәтті өзгертілді',
        'Пользователь': 'Пайдаланушы',
        '1. Кому направить?': '1. Кімге жіберу керек?',
        '2. Тип обращения': '2. Өтініш түрі',
        '3. Тема обращения': '3. Тақырыбы',
        'Введите тему своего обращения': 'Өтінішіңіздің тақырыбын енгізіңіз',
        '4. Сообщение': '4. Хабарлама',
        'Опишите ваше обращение как можно подробнее...': 'Өтінішіңізді мүмкіндігінше толық сипаттаңыз...',
        '5. Прикрепите файл': '5. Файл тіркеңіз',
        'Загрузить файл': 'Файл жүктеу',
        '6. Ваши контакты': '6. Сіздің байланыстарыңыз',
        'Почта': 'Электрондық пошта',
        'Номер телефона': 'Телефон нөірі',
        'Отправить': 'Жіберу',
        'Процесс': 'Процесс',
        'Инструкция': 'Нұсқаулық',
        'Ничего не найдено': 'Ештеңе табылмады',
        'Попробуйте изменить критерии поиска или выбрать другую категорию.': 'Іздеу критерийлерін өзгертіп көріңіз немесе басқа санатты таңдаңыз.',
        'В данный момент уроки отсутствуют': 'Қазіргі уақытта сабақтар жоқ',
        'Если у вас есть предложения, замечания по работе сайта или вопросы — отправьте их через форму ниже. Мы ответим как можно быстрее.': 'Егер сіздің ұсыныстарыңыз, сайттың жұмысы туралы ескертпелеріңіз немесе сұрақтарыңыз болса - оларды төмендегі форма арқылы жіберіңіз. Біз барынша тез жауап береміз.',
        'Изучайте материалы в удобном формате': 'Материалдарды ыңғайлы форматта оқыңыз',
        'Начать поиск': 'Іздеуді бастау',
        'Начинающий': 'Бастаушы',
        'Средний': 'Орташа',
        'Продвинутый': 'Жоғары',
        'Скачать PDF': 'PDF жүктеу',
        'Документы не найдены': 'Құжаттар табылмады',
        'Попробуйте изменить критерии поиска': 'Іздеу критерийлерін өзгертіп көріңіз',
        'Уроки не найдены': 'Сабақтар табылмады',
        'Попробуйте изменить критерии поиска или выбрать другой уровень сложности.': 'Іздеу критерийлерін өзгертіп көріңіз немесе басқа қиындық деңгейін таңдаңыз.',
        'Открыть': 'Ашу',
        'Скрыть': 'Жасыру',
        'Видео урока': 'Сабақтың бейнесі',
        'Презентация урока': 'Сабақтың презентациясы',
        'Ваш браузер не поддерживает видео': 'Сіздің браузеріңіз бейнені қолдамайды',
        'Ваш браузер не поддерживает PDF': 'Сіздің браузеріңіз PDF қолдамайды',
        'В данный момент документы отсутствуют': 'Қазіргі уақытта құжаттар жоқ',
        'Завершить урок': 'Сабақты аяқтау',
        'Завершен': 'Аяқталды',
        'Изучите материал для завершения': 'Аяқтау үшін материалды зерттеңіз',
        'Задайте свой вопрос': 'Сұрағыңызды қойыңыз',
        'Поиск по вопросам': 'Сұрақтарды іздеу',
        'Категории': 'Санаттар',
        'HR': 'HR',
        'IT поддержка': 'IT қолдауы',
        'Предложение': 'Ұсыныс',
        'Жалоба': 'Шағым',
        'Вопрос': 'Сұрақ',
        'Проблема с сайтом': 'Сайт мәселесі',
        'Пожалуйста, заполните все обязательные поля.': 'Барлық міндетті өрістерді толтырыңыз.',
        'Ваше обращение успешно отправлено! Мы ответим как можно быстрее.': 'Сіздің өтінішіңіз сәтті жіберілді! Біз барынша тез жауап береміз.',
    }
}

def get_translation(text, language='ru'):
    """Простая функция перевода"""
    if language == 'ru' or language not in TRANSLATIONS:
        return text
    return TRANSLATIONS.get(language, {}).get(text, text)
from .models import Instruction, Process, Feedback, FAQ, FAQCategory

def login_view(request):
    """Login page view"""
    if request.user.is_authenticated:
        return redirect('main:dashboard')
    return render(request, 'main/login.html')

@login_required
def dashboard_view(request):
    """Main dashboard view"""
    # Проверяем, является ли пользователь преподавателем
    teacher = None
    try:
        from .models import Teacher
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        pass
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('_language') or request.session.get('django_language', 'ru')
    
    # Определяем приветствие в зависимости от времени
    now = timezone.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        greeting = get_translation("Доброе утро", current_language)
    elif 12 <= hour < 18:
        greeting = get_translation("Добрый день", current_language)
    else:
        greeting = get_translation("Добрый вечер", current_language)
    
    user_name = teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else get_translation('Пользователь', current_language))
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': user_name,
        'greeting': greeting,
        'current_page': 'dashboard'
    }
    return render(request, 'main/dashboard.html', context)

@login_required
def lessons_view(request):
    """Вкладка Уроки с современным дизайном"""
    # Получаем уроки из базы данных
    lessons = list(Lesson.objects.filter(is_active=True).order_by('-created_at'))
    
    # Получаем все активные категории
    categories = LessonCategory.objects.filter(is_active=True).order_by('order_index', 'name')
    
    # Получаем параметры поиска и фильтрации
    search_query = request.GET.get('search', '')
    difficulty_filter = request.GET.get('difficulty', 'all')
    category_filter = request.GET.get('category', '')
    
    # Фильтруем по категории
    if category_filter:
        lessons = [l for l in lessons if l.category and str(l.category.id) == category_filter]
    
    # Фильтруем по уровню сложности
    if difficulty_filter != 'all':
        lessons = [l for l in lessons if l.difficulty_level == difficulty_filter]
    
    if search_query:
        # Поиск без учета регистра для латиницы и кириллицы
        search_query = search_query.lower()
        
        # Фильтруем уроки
        lessons = [l for l in lessons if 
                  search_query in l.title.lower() or 
                  search_query in getattr(l, 'title_en', '').lower() or 
                  search_query in getattr(l, 'title_kk', '').lower() or 
                  search_query in l.description.lower() or 
                  search_query in getattr(l, 'description_en', '').lower() or 
                  search_query in getattr(l, 'description_kk', '').lower()]
    
    # Если уроков нет, просто показываем пустой список
    # Тестовые уроки теперь создаются в admin_lessons_view
    
    # Добавляем информацию о завершении уроков и прогрессе для каждого урока
    # Получаем прогресс для всех уроков
    lesson_progress = {}
    for lesson in lessons:
        # Убеждаемся, что урок сохранен в базе данных
        if lesson.pk is None:
            lesson.save()
        
        lesson.is_completed = lesson.is_completed_by_user(request.user)
        lesson.can_complete = lesson.can_be_completed_by_user(request.user)
        lesson_progress[lesson.id] = lesson.get_or_create_progress(request.user)
    
    return render(request, 'main/lessons.html', {
        'lessons': lessons,
        'lesson_progress': lesson_progress,
        'categories': categories,
        'search_query': search_query,
        'difficulty_filter': difficulty_filter,
        'category_filter': category_filter,
        'current_language': request.session.get('django_language', 'ru'),
        'current_page': 'lessons'
    })


@login_required
def complete_lesson_view(request, lesson_id):
    """API endpoint для завершения урока"""
    if request.method == 'POST':
        try:
            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            lesson.mark_as_completed(request.user)
            return JsonResponse({
                'success': True,
                'message': 'Урок успешно завершен!'
            })
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при завершении урока'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)


@login_required
def update_video_progress_view(request, lesson_id):
    """API endpoint для обновления прогресса видео"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            current_time = data.get('current_time', 0)
            total_duration = data.get('total_duration', 0)

            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            progress = lesson.get_or_create_progress(request.user)

            # Обновляем прогресс видео
            max_progress_percent = data.get('max_progress_percent', None)
            progress.update_video_progress(current_time, total_duration, max_progress_percent)

            return JsonResponse({
                'success': True,
                'video_watched': progress.video_watched,
                'is_ready_to_complete': progress.is_ready_to_complete
            })
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при обновлении прогресса'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)

@login_required
def update_pdf_progress_view(request, lesson_id):
    """API endpoint для обновления прогресса PDF"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            current_page = data.get('current_page', 1)
            total_pages = data.get('total_pages', 1)

            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            progress = lesson.get_or_create_progress(request.user)

            # Обновляем прогресс PDF
            progress.update_pdf_progress(current_page, total_pages)

            return JsonResponse({
                'success': True,
                'pdf_completed': progress.pdf_completed,
                'is_ready_to_complete': progress.is_ready_to_complete
            })
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при обновлении прогресса'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)

@login_required
def update_slides_progress_view(request, lesson_id):
    """API endpoint для обновления прогресса слайдов"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            current_slide = data.get('current_slide', 1)
            total_slides = data.get('total_slides', 1)

            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            progress = lesson.get_or_create_progress(request.user)

            # Обновляем прогресс слайдов
            progress.update_slides_progress(current_slide, total_slides)

            return JsonResponse({
                'success': True,
                'slides_completed': progress.slides_completed,
                'is_ready_to_complete': progress.is_ready_to_complete
            })
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при обновлении прогресса'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)

@login_required
def get_lesson_progress_view(request, lesson_id):
    """API endpoint для получения прогресса урока"""
    if request.method == 'GET':
        try:
            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            progress = lesson.get_or_create_progress(request.user)

            return JsonResponse({
                'success': True,
                'video_progress': {
                    'current_time': progress.video_current_time,
                    'total_time': progress.video_total_time,
                    'max_progress_percent': progress.video_max_progress_percent,
                    'watched': progress.video_watched
                },
                'slides_progress': {
                    'current_slide': progress.slides_current_slide,
                    'total_slides': progress.slides_total_slides,
                    'max_progress_percent': progress.slides_max_progress_percent,
                    'completed': progress.slides_completed
                },
                'pdf_progress': {
                    'current_page': progress.pdf_current_page,
                    'total_pages': progress.pdf_total_pages,
                    'completed': progress.pdf_completed,
                    'progress_percent': progress.get_pdf_progress_percentage()
                },
                'is_ready_to_complete': progress.is_ready_to_complete,
                'is_completed': lesson.is_completed_by_user(request.user)
            })
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при получении прогресса'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)

@login_required
def get_lesson_slides_view(request, lesson_id):
    """API endpoint для получения слайдов урока"""
    if request.method == 'GET':
        try:
            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            slides = lesson.get_slides()

            # Если есть слайды, возвращаем их
            if slides.exists():
                slides_data = []
                for slide in slides:
                    slides_data.append({
                        'id': slide.id,
                        'order': slide.order,
                        'title': slide.title,
                        'description': slide.description,
                        'image': request.build_absolute_uri(slide.image.url) if slide.image else None
                    })

                return JsonResponse({
                    'success': True,
                    'slides': slides_data
                })
            # Если нет слайдов, но есть PDF, сообщаем о необходимости конвертации
            elif lesson.has_pdf():
                return JsonResponse({
                    'success': True,
                    'needs_conversion': True,
                    'message': 'PDF нужно конвертировать в слайды'
                })
            # Если нет ни слайдов, ни PDF
            else:
                return JsonResponse({
                    'success': True,
                    'slides': []
                })
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при получении слайдов'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)

@login_required
def convert_pdf_to_slides_view(request, lesson_id):
    """API endpoint для конвертации PDF в слайды"""
    if request.method == 'POST':
        try:
            lesson = Lesson.objects.get(id=lesson_id, is_active=True)
            
            if not lesson.pdf_file:
                return JsonResponse({
                    'success': False,
                    'message': 'У урока нет PDF файла'
                }, status=400)
            
            # Конвертируем PDF в слайды
            success = lesson.convert_pdf_to_slides()
            
            if success:
                slides_count = lesson.slides.count()
                return JsonResponse({
                    'success': True,
                    'message': f'PDF успешно конвертирован в {slides_count} слайдов',
                    'slides_count': slides_count
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Ошибка при конвертации PDF'
                }, status=500)
                
        except Lesson.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Урок не найден'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Произошла ошибка при конвертации: {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    }, status=405)

@login_required
def employee_progress_view(request):
    """Страница для просмотра прогресса сотрудников - новая версия"""
    if not request.user.is_staff:
        return redirect('dashboard')
    
    # Получаем все уроки
    lessons = Lesson.objects.filter(is_active=True).order_by('title')
    
    # Получаем всех пользователей (кроме админов)
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    
    # Собираем статистику по пользователям
    user_stats = []
    total_users = 0
    total_lessons = lessons.count()
    
    for user in users:
        total_users += 1
        
        # Подсчитываем прогресс пользователя
        user_completed = 0
        user_in_progress = 0
        user_not_started = 0
        
        for lesson in lessons:
            try:
                progress = LessonProgress.objects.get(user=user, lesson=lesson)
                
                # Безопасно получаем значения прогресса
                video_progress = 0
                slides_progress = 0
                
                if hasattr(progress, 'video_max_progress_percent'):
                    try:
                        video_progress = float(progress.video_max_progress_percent or 0)
                    except (ValueError, TypeError):
                        video_progress = 0
                
                # Вычисляем максимальный процент прогресса слайдов
                if hasattr(progress, 'slides_max_progress_percent'):
                    try:
                        slides_progress = float(progress.slides_max_progress_percent or 0)
                    except (ValueError, TypeError):
                        slides_progress = 0
                elif hasattr(progress, 'slides_current_slide') and hasattr(progress, 'slides_total_slides'):
                    try:
                        slides_current = int(progress.slides_current_slide or 0)
                        slides_total = int(progress.slides_total_slides or 0)
                        if slides_total > 0:
                            slides_progress = (slides_current / slides_total) * 100
                    except (ValueError, TypeError):
                        slides_progress = 0
                else:
                    slides_progress = 0
                
                # Определяем общий прогресс урока
                lesson_progress = 0
                if lesson.video and lesson.pdf:
                    lesson_progress = (video_progress + slides_progress) / 2
                elif lesson.video:
                    lesson_progress = video_progress
                elif lesson.pdf:
                    lesson_progress = slides_progress
                
                # Определяем статус урока
                if lesson_progress >= 100:
                    user_completed += 1
                elif lesson_progress > 0:
                    user_in_progress += 1
                else:
                    user_not_started += 1
                    
            except LessonProgress.DoesNotExist:
                user_not_started += 1
        
        # Вычисляем общий процент завершения
        total_user_lessons = user_completed + user_in_progress + user_not_started
        completion_percentage = 0
        if total_user_lessons > 0:
            completion_percentage = (user_completed / total_user_lessons) * 100
        
        user_stats.append({
            'user': user,
            'completed': user_completed,
            'in_progress': user_in_progress,
            'not_started': user_not_started,
            'completion_percentage': completion_percentage,
            'total_lessons': total_user_lessons
        })
    
    # Сортируем пользователей по проценту завершения (убывание)
    user_stats.sort(key=lambda x: x['completion_percentage'], reverse=True)
    
    # Общая статистика
    total_completed = sum(stat['completed'] for stat in user_stats)
    total_in_progress = sum(stat['in_progress'] for stat in user_stats)
    total_not_started = sum(stat['not_started'] for stat in user_stats)
    
    context = {
        'user_stats': user_stats,
        'total_users': total_users,
        'total_lessons': total_lessons,
        'total_completed': total_completed,
        'total_in_progress': total_in_progress,
        'total_not_started': total_not_started,
    }
    
    return render(request, 'main/admin/employee_progress.html', context)

@login_required
def lesson_progress_detail_view(request, lesson_id):
    """Детальная страница прогресса по конкретному уроку"""
    if not request.user.is_staff:
        return redirect('dashboard')
    
    try:
        lesson = Lesson.objects.get(id=lesson_id, is_active=True)
    except Lesson.DoesNotExist:
        messages.error(request, 'Урок не найден')
        return redirect('employee_progress')
    
    # Получаем всех пользователей
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    
    # Получаем прогресс для этого урока
    progress_list = []
    for user in users:
        progress, created = LessonProgress.objects.get_or_create(
            lesson=lesson,
            user=user,
            defaults={
                'video_total_time': 0,
                'pdf_total_pages': 1,
                'slides_total_slides': 1
            }
        )
        progress_list.append(progress)
    
    # Статистика по уроку
    total_users = users.count()
    completed_users = lesson.completed_users.count()
    active_users = LessonProgress.objects.filter(
        lesson=lesson,
        last_activity__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()
    
    context = {
        'lesson': lesson,
        'progress_list': progress_list,
        'total_users': total_users,
        'completed_users': completed_users,
        'active_users': active_users,
    }
    
    return render(request, 'main/admin/lesson_progress_detail.html', context)


# ===== EDITOR PROGRESS VIEWS =====
@login_required
def editor_progress_view(request):
    """Страница прогресса пользователей для редактора (чтение только)"""
    # Проверяем права редактора
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')

    lessons = Lesson.objects.filter(is_active=True).order_by('title')
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')

    user_stats = []
    total_users = 0
    total_lessons = lessons.count()

    for user in users:
        total_users += 1
        user_completed = 0
        user_in_progress = 0
        user_not_started = 0

        for lesson in lessons:
            try:
                progress = LessonProgress.objects.get(user=user, lesson=lesson)
                video_progress = float(getattr(progress, 'video_max_progress_percent', 0) or 0)
                slides_progress = float(getattr(progress, 'slides_max_progress_percent', 0) or 0)
                if not slides_progress and getattr(progress, 'slides_total_slides', 0):
                    slides_current = int(getattr(progress, 'slides_current_slide', 0) or 0)
                    slides_total = int(getattr(progress, 'slides_total_slides', 0) or 0)
                    if slides_total > 0:
                        slides_progress = (slides_current / slides_total) * 100

                if lesson.video and lesson.pdf:
                    lesson_progress = (video_progress + slides_progress) / 2
                elif lesson.video:
                    lesson_progress = video_progress
                elif lesson.pdf:
                    lesson_progress = slides_progress
                else:
                    lesson_progress = 0

                if lesson_progress >= 100:
                    user_completed += 1
                elif lesson_progress > 0:
                    user_in_progress += 1
                else:
                    user_not_started += 1
            except LessonProgress.DoesNotExist:
                user_not_started += 1

        total_user_lessons = user_completed + user_in_progress + user_not_started
        completion_percentage = (user_completed / total_user_lessons) * 100 if total_user_lessons else 0
        user_stats.append({
            'user': user,
            'completed': user_completed,
            'in_progress': user_in_progress,
            'not_started': user_not_started,
            'completion_percentage': completion_percentage,
            'total_lessons': total_user_lessons
        })

    user_stats.sort(key=lambda x: x['completion_percentage'], reverse=True)

    total_completed = sum(stat['completed'] for stat in user_stats)
    total_in_progress = sum(stat['in_progress'] for stat in user_stats)
    total_not_started = sum(stat['not_started'] for stat in user_stats)

    context = {
        'editor': editor,
        'user_stats': user_stats,
        'total_users': total_users,
        'total_lessons': total_lessons,
        'total_completed': total_completed,
        'total_in_progress': total_in_progress,
        'total_not_started': total_not_started,
    }

    return render(request, 'main/editor/employee_progress.html', context)


@login_required
def editor_lesson_progress_detail_view(request, lesson_id):
    """Детальная страница прогресса по уроку для редактора (чтение только)"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')

    try:
        lesson = Lesson.objects.get(id=lesson_id, is_active=True)
    except Lesson.DoesNotExist:
        messages.error(request, 'Урок не найден')
        return redirect('main:editor_progress')

    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    progress_list = []
    for user in users:
        progress, _ = LessonProgress.objects.get_or_create(
            lesson=lesson,
            user=user,
            defaults={'video_total_time': 0, 'pdf_total_pages': 1, 'slides_total_slides': 1}
        )
        progress_list.append(progress)

    total_users = users.count()
    completed_users = lesson.completed_users.count()
    active_users = LessonProgress.objects.filter(
        lesson=lesson,
        last_activity__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()

    context = {
        'editor': editor,
        'lesson': lesson,
        'progress_list': progress_list,
        'total_users': total_users,
        'completed_users': completed_users,
        'active_users': active_users,
    }

    return render(request, 'main/editor/lesson_progress_detail.html', context)

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('main:login')

@login_required
def about_view(request):
    """About university page view"""
    # Проверяем, является ли пользователь преподавателем
    teacher = None
    try:
        from .models import Teacher
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        pass
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Получаем объекты для страницы "Об университете"
    try:
        from .models import History, Mission, Values, Leader
        history_obj = History.objects.first()
        mission_obj = Mission.objects.first()
        values_obj = Values.objects.first()
        leaders = Leader.objects.filter(is_active=True).order_by('order', 'role')
    except Exception:
        history_obj = None
        mission_obj = None
        values_obj = None
        leaders = []
    
    # Подготавливаем текст на нужном языке
    history_text = history_obj.get_text(current_language) if history_obj else None
    mission_text = mission_obj.get_text(current_language) if mission_obj else None
    values_text = values_obj.get_text(current_language) if values_obj else None
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь'),
        'current_page': 'about',
        'current_language': current_language,
        'history_obj': history_obj,
        'mission_obj': mission_obj,
        'values_obj': values_obj,
        'history_text': history_text,
        'mission_text': mission_text,
        'values_text': values_text,
        'leaders': leaders,
    }
    return render(request, 'main/about.html', context)
    
@login_required
def map_view(request):
    """Contacts and map page view"""
    # Проверяем, является ли пользователь преподавателем
    teacher = None
    try:
        from .models import Teacher
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        pass
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Получаем переводимые данные контактов (первый объект)
    try:
        from .models import ContactInfo
        contact_info = ContactInfo.objects.first()
    except Exception:
        contact_info = None

    # Подготавливаем текст на нужном языке
    address_text = contact_info.get_address(current_language) if contact_info else None
    campus_items_list = contact_info.get_campus_items(current_language) if contact_info else []
    campus_3d_button_text = contact_info.get_campus_3d_button_text(current_language) if contact_info else "Изучить кампус в 3D"
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь'),
        'current_language': current_language,
        'contact_info': contact_info,
        'address_text': address_text,
        'campus_items_list': campus_items_list,
        'campus_3d_button_text': campus_3d_button_text,
        'current_page': 'map'
    }
    return render(request, 'main/map.html', context)

@login_required
def documents_view(request):
    """Documents page view with search and filtering"""
    from .models import Document, DocumentCategory
    from django.db.models import Q
    
    # Получаем параметры из запроса
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Базовый queryset только активных документов
    documents = Document.objects.filter(is_active=True)
    
    # Применяем фильтр по категории сначала (для оптимизации)
    if category_filter:
        # поддержка фильтра по id
        if category_filter.isdigit():
            documents = documents.filter(category_id=int(category_filter))
        else:
            # обратная совместимость по имени
            documents = documents.filter(category__name=category_filter)
    
    # Применяем поиск (нечувствительный к регистру)
    # Используем Python поиск из-за проблем SQLite с кириллицей в icontains
    if search_query:
        search_query = search_query.strip().lower()
        if search_query:
            # Получаем все документы сначала, потом фильтруем в Python
            all_documents = list(documents)
            filtered_documents = []
            
            for doc in all_documents:
                # Получаем переведенные названия и описания
                title = doc.get_title(current_language)
                description = doc.get_description(current_language)
                
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in title.lower()
                desc_match = search_query in description.lower()
                category_match = (
                    search_query in doc.category.name.lower() or
                    search_query in getattr(doc.category, 'name_en', '').lower() or
                    search_query in getattr(doc.category, 'name_kk', '').lower()
                )
                
                if title_match or desc_match or category_match:
                    filtered_documents.append(doc.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_documents:
                documents = documents.filter(id__in=filtered_documents)
            else:
                documents = documents.none()
    
    # Получаем все категории для фильтров
    categories = DocumentCategory.objects.all()
    
    # Проверяем, является ли пользователь преподавателем
    teacher = None
    try:
        from .models import Teacher
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        pass
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь'),
        'documents': documents,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_filter,
        'current_language': current_language,
        'current_page': 'documents'
    }
    return render(request, 'main/documents.html', context)

@login_required
def download_document(request, document_id):
    """Download document and increment counter"""
    from .models import Document
    from django.http import Http404, HttpResponse, FileResponse
    import os
    
    try:
        document = Document.objects.get(id=document_id, is_active=True)
    except Document.DoesNotExist:
        raise Http404("Документ не найден")
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Получаем файл на нужном языке
    file_to_download = document.get_file(current_language)
    
    if not file_to_download:
        raise Http404("Файл не найден для выбранного языка")
    
    # Увеличиваем счетчик скачиваний
    document.increment_download_count()
    
    # Возвращаем файл для скачивания
    if file_to_download and os.path.exists(file_to_download.path):
        response = FileResponse(
            open(file_to_download.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_to_download.name)
        )
        return response
    else:
        raise Http404("Файл не найден")

@login_required
def documents_api_search(request):
    """API endpoint для поиска документов без перезагрузки страницы"""
    from .models import Document, DocumentCategory
    from django.db.models import Q
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    
    # Получаем параметры из запроса
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Базовый queryset только активных документов
    documents = Document.objects.filter(is_active=True)
    
    # Применяем фильтр по категории сначала (для оптимизации)
    if category_filter:
        try:
            # Фильтруем по ID категории, а не по имени
            category_id = int(category_filter)
            documents = documents.filter(category_id=category_id)
        except (ValueError, TypeError):
            # Если category_filter не является числом, игнорируем фильтр
            pass
    
    # Применяем поиск (нечувствительный к регистру)
    # Используем Python поиск из-за проблем SQLite с кириллицей в icontains
    if search_query:
        search_query = search_query.strip().lower()
        if search_query:
            # Получаем все документы сначала, потом фильтруем в Python
            all_documents = list(documents)
            filtered_documents = []
            
            for doc in all_documents:
                # Получаем переведенные названия и описания
                title = doc.get_title(current_language)
                description = doc.get_description(current_language)
                
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in title.lower()
                desc_match = search_query in description.lower()
                category_match = search_query in doc.category.name.lower()
                
                if title_match or desc_match or category_match:
                    filtered_documents.append(doc.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_documents:
                documents = documents.filter(id__in=filtered_documents)
            else:
                documents = documents.none()
    
    # Рендерим только список документов
    documents_html = render_to_string('main/documents_list_partial.html', {
        'documents': documents,
        'search_query': search_query,
        'current_category': category_filter,
        'current_language': current_language
    })
    
    return JsonResponse({
        'success': True,
        'html': documents_html,
        'count': documents.count()
    })



@login_required
def feedback_view(request):
    """Страница обратной связи"""
    if request.method == 'POST':
        # Получаем данные из формы
        feedback_type = request.POST.get('feedback_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        file = request.FILES.get('file')
        
        # Получаем текущий язык из сессии для сообщений
        current_language = request.session.get('django_language', 'ru')
        
        # Валидация обязательных полей (recipient автоматически становится 'hr')
        if not all([feedback_type, subject, message, email]):
            error_message = get_translation('Пожалуйста, заполните все обязательные поля.', current_language)
            messages.error(request, error_message)
        else:
            try:
                # Создаем новое обращение (все обращения идут в HR)
                feedback = Feedback.objects.create(
                    user=request.user,
                    recipient='hr',  # Все обращения автоматически направляются в HR
                    feedback_type=feedback_type,
                    subject=subject,
                    message=message,
                    email=email,
                    phone=phone,
                    file=file
                )
                
                success_message = get_translation('Ваше обращение успешно отправлено! Мы ответим как можно быстрее.', current_language)
                messages.success(request, success_message)
                return redirect('main:feedback')
                
            except Exception as e:
                messages.error(request, f'Произошла ошибка при отправке обращения: {str(e)}')
    
    # Получаем информацию о пользователе
    teacher = None
    try:
        from .models import Teacher
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        pass
    
    # Предзаполняем email пользователя
    user_email = request.user.email if request.user.email else ''
    if teacher and not user_email:
        user_email = getattr(teacher, 'email', '')
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Создаем переведенные choices
    recipient_choices = []
    for value, label in Feedback.RECIPIENT_CHOICES:
        translated_label = get_translation(label, current_language)
        recipient_choices.append((value, translated_label))
    
    type_choices = []
    for value, label in Feedback.TYPE_CHOICES:
        translated_label = get_translation(label, current_language)
        type_choices.append((value, translated_label))
    
    # Получаем информацию для кнопки IT поддержки
    contact_info = None
    try:
        contact_info = ContactInfo.objects.first()
    except ContactInfo.DoesNotExist:
        pass
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else get_translation('Пользователь', current_language)),
        'user_email': user_email,
        'recipient_choices': recipient_choices,
        'type_choices': type_choices,
        'contact_info': contact_info,
        'current_language': current_language,
        'current_page': 'feedback'
    }
    
    return render(request, 'main/feedback.html', context)

@login_required
def faq_view(request):
    """Страница часто задаваемых вопросов с поиском и фильтрацией"""
    from django.db.models import Q
    
    # Получаем параметры из запроса
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Базовый queryset только активных FAQ
    faqs = FAQ.objects.filter(is_active=True)
    
    # Применяем фильтр по категории сначала (для оптимизации)
    if category_filter:
        if category_filter.isdigit():
            faqs = faqs.filter(category_id=int(category_filter))
        else:
            faqs = faqs.filter(category__name=category_filter)
    
    # Применяем поиск (нечувствительный к регистру)
    if search_query:
        search_query = search_query.strip().lower()
        if search_query:
            # Получаем все FAQ сначала, потом фильтруем в Python
            all_faqs = list(faqs)
            filtered_faq_ids = []
            
            for faq in all_faqs:
                # Проверяем вхождение поискового запроса в разные поля
                question_match = (
                    search_query in faq.question.lower() or
                    search_query in getattr(faq, 'question_en', '').lower() or
                    search_query in getattr(faq, 'question_kk', '').lower()
                )
                answer_match = (
                    search_query in faq.answer.lower() or
                    search_query in getattr(faq, 'answer_en', '').lower() or
                    search_query in getattr(faq, 'answer_kk', '').lower()
                )
                category_name = getattr(faq.category, 'name', '')
                category_match = (
                    search_query in category_name.lower() or
                    search_query in getattr(faq.category, 'name_en', '').lower() or
                    search_query in getattr(faq.category, 'name_kk', '').lower()
                )
                
                if question_match or answer_match or category_match:
                    filtered_faq_ids.append(faq.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_faq_ids:
                faqs = faqs.filter(id__in=filtered_faq_ids)
            else:
                faqs = faqs.none()
    
    # Получаем все активные категории для фильтров
    categories = FAQCategory.objects.filter(is_active=True)
    
    # Получаем информацию о пользователе
    teacher = None
    try:
        from .models import Teacher
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        pass
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Подготавливаем FAQ с текстом на нужном языке
    faqs_with_translations = []
    for faq in faqs:
        faq_data = {
            'id': faq.id,
            'question': faq.get_question(current_language),
            'answer': faq.get_answer(current_language),
            'category': faq.category,
            'views_count': faq.views_count,
            'is_popular': faq.is_popular,
            'order_index': faq.order_index,
        }
        faqs_with_translations.append(faq_data)
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь'),
        'faqs': faqs_with_translations,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_filter,
        'current_language': current_language,
        'current_page': 'faq'
    }
    
    return render(request, 'main/faq.html', context)

@login_required
def faq_api_search(request):
    """API endpoint для поиска FAQ без перезагрузки страницы"""
    from django.template.loader import render_to_string
    from django.db.models import Q
    
    # Получаем параметры из запроса
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Базовый queryset только активных FAQ
    faqs = FAQ.objects.filter(is_active=True)
    
    # Применяем фильтр по категории сначала (для оптимизации)
    if category_filter:
        try:
            category_id = int(category_filter)
            faqs = faqs.filter(category_id=category_id)
        except (ValueError, TypeError):
            # Если category_filter не является числом, игнорируем фильтр
            pass
    
    # Применяем поиск (нечувствительный к регистру)
    if search_query:
        search_query = search_query.strip().lower()
        if search_query:
            # Получаем все FAQ сначала, потом фильтруем в Python
            all_faqs = list(faqs)
            filtered_faq_ids = []
            
            for faq in all_faqs:
                # Проверяем вхождение поискового запроса в разные поля
                question_match = search_query in faq.question.lower()
                answer_match = search_query in faq.answer.lower()
                category_match = search_query in faq.category.name.lower()
                
                if question_match or answer_match or category_match:
                    filtered_faq_ids.append(faq.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_faq_ids:
                faqs = faqs.filter(id__in=filtered_faq_ids)
            else:
                faqs = faqs.none()
    
    # Получаем текущий язык из сессии
    current_language = request.session.get('django_language', 'ru')
    
    # Подготавливаем FAQ с текстом на нужном языке
    faqs_with_translations = []
    for faq in faqs:
        faq_data = {
            'id': faq.id,
            'question': faq.get_question(current_language),
            'answer': faq.get_answer(current_language),
            'category': faq.category,
            'views_count': faq.views_count,
            'is_popular': faq.is_popular,
            'order_index': faq.order_index,
        }
        faqs_with_translations.append(faq_data)
    
    # Рендерим только список FAQ
    faq_html = render_to_string('main/faq_list_partial.html', {
        'faqs': faqs_with_translations,
        'search_query': search_query,
        'current_category': category_filter
    })
    
    return JsonResponse({
        'success': True,
        'html': faq_html,
        'count': faqs.count()
    })

@login_required
def faq_increment_views(request, faq_id):
    """API endpoint для увеличения счетчика просмотров FAQ"""
    try:
        faq = FAQ.objects.get(id=faq_id, is_active=True)
        faq.increment_views()
        return JsonResponse({'success': True})
    except FAQ.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'FAQ не найден'})


@login_required
def processes_instructions_api_search(request):
    """API для поиска процессов и инструкций"""
    search_query = request.GET.get('search', '').strip()
    tab = request.GET.get('tab', 'all')
    
    # Получаем все процессы и инструкции (используем тестовые данные)
    processes = [
        Process(title="Как пользоваться Career AlmaU?", description="Подробная инструкция по использованию Career AlmaU для поиска работы и стажировок."),
        Process(title="Как подать заявку на мероприятие в Документологе?", description="Пошаговое руководство по подаче заявки на мероприятие через систему Документолог."),
        Process(title="Куда писать за помощью?", description="Контактная информация и способы получения помощи по различным вопросам.")
    ]
    
    instructions = [
        Instruction(title="Инструкция по регистрации в системе", description="Подробная инструкция по регистрации нового пользователя в системе."),
        Instruction(title="Как изменить пароль", description="Пошаговое руководство по смене пароля в личном кабинете."),
        Instruction(title="Настройка уведомлений", description="Инструкция по настройке email и push уведомлений.")
    ]
    
    # Фильтрация по типу
    if tab == 'processes':
        instructions = []
    elif tab == 'instructions':
        processes = []
    
    # Поиск
    if search_query:
        search_query_lower = search_query.lower()
        processes = [p for p in processes if 
                    search_query_lower in p.title.lower() or 
                    search_query_lower in p.description.lower()]
        
        instructions = [i for i in instructions if 
                       search_query_lower in i.title.lower() or 
                       search_query_lower in i.description.lower()]
    
    # Подготавливаем контекст для шаблона
    context = {
        'filtered_processes': processes,
        'filtered_instructions': instructions,
        'search_query': search_query,
        'current_tab': tab
    }
    
    # Рендерим частичный шаблон
    html = render_to_string('main/processes_instructions_list_partial.html', context, request=request)
    
    return JsonResponse({
        'success': True,
        'html': html,
        'count': len(processes) + len(instructions)
    })


@login_required
def settings_view(request):
    """Страница настроек"""
    from django.utils import translation
    
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in ['ru', 'en', 'kk']:
            # Активируем язык для текущего запроса
            translation.activate(language)
            # Сохраняем в сессии (используем стандартный ключ Django)
            request.session['django_language'] = language
            request.session['_language'] = language  # Стандартный ключ Django для языка
            success_message = get_translation('Язык успешно изменен', language)
            messages.success(request, success_message)
            return redirect('main:settings')
    
    current_language = request.session.get('_language') or request.session.get('django_language', 'ru')
    current_theme = request.session.get('selected_theme', 'light')
    
    context = {
        'current_language': current_language,
        'current_theme': current_theme,
        'languages': [
            ('ru', 'Русский'),
            ('en', 'English'),
            ('kk', 'Қазақша'),
        ],
        'current_page': 'settings'
    }
    return render(request, 'main/settings.html', context)


def set_language_view(request):
    """Переключение языка"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in ['ru', 'en', 'kk']:
            # Сохраняем в сессии
            request.session['django_language'] = language
            request.session['_language'] = language  # Стандартный ключ Django для языка
            
            # Определяем куда перенаправить
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
            return redirect(next_url)
    
    # Если что-то пошло не так, перенаправляем на главную
    return redirect('main:dashboard')


# ===== ADMIN PANEL VIEWS =====

# Удаляем тестовые view для входа в админ панель

def admin_login_view(request):
    """Страница логина для администраторов"""
    # Если пользователь уже авторизован и является суперпользователем
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('main:admin_about')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:  # Проверяем что пользователь суперпользователь
                    login(request, user)
                    return redirect('main:admin_about')
                else:
                    messages.error(request, 'У вас нет прав администратора для доступа к этой панели.')
            else:
                messages.error(request, 'Неверные учетные данные.')
        else:
                messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'main/admin_login.html')


def admin_logout_view(request):
    """Выход из панели администратора"""
    logout(request)
    return redirect('main:admin_login')

@login_required
def admin_about_view(request):
    """Админка для страницы 'Об университете'"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем или создаем объекты
    history_obj, created = History.objects.get_or_create(pk=1, defaults={'text': 'История университета'})
    mission_obj, created = Mission.objects.get_or_create(pk=1, defaults={'text': 'Миссия университета'})
    values_obj, created = Values.objects.get_or_create(pk=1, defaults={'text': 'Ценности университета'})
    
    if request.method == 'POST':
        # Отладочная информация для всех POST запросов
        print(f"DEBUG: POST request received")
        print(f"DEBUG: POST data: {request.POST}")
        print(f"DEBUG: FILES data: {request.FILES}")
        
        # Обработка формы истории
        if 'history' in request.POST:
            history_obj.text = request.POST.get('history_text', '')
            history_obj.text_en = request.POST.get('history_text_en', '')
            history_obj.text_kk = request.POST.get('history_text_kk', '')
            if 'history_image' in request.FILES:
                history_obj.image = request.FILES['history_image']
            history_obj.save()
            messages.success(request, 'История успешно обновлена!')
        
        # Обработка формы миссии
        if 'mission' in request.POST:
            mission_obj.text = request.POST.get('mission_text', '')
            mission_obj.text_en = request.POST.get('mission_text_en', '')
            mission_obj.text_kk = request.POST.get('mission_text_kk', '')
            mission_obj.save()
            messages.success(request, 'Миссия успешно обновлена!')
        
        # Обработка формы ценностей
        if 'values' in request.POST:
            values_obj.text = request.POST.get('values_text', '')
            values_obj.text_en = request.POST.get('values_text_en', '')
            values_obj.text_kk = request.POST.get('values_text_kk', '')
            values_obj.save()
            messages.success(request, 'Ценности успешно обновлены!')
            
        # Обработка руководителей перенесена в отдельный раздел admin_leaders_view
        
        return redirect('main:admin_about')
    
    context = {
        'current_page': 'admin_about',
        'active_tab': 'about',
        'history_obj': history_obj,
        'mission_obj': mission_obj,
        'values_obj': values_obj,
    }
    return render(request, 'main/admin/about.html', context)

@login_required
def admin_map_view(request):
    """Админка для страницы 'Контакты и карта'"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем или создаем объект контактной информации
    contact_info, created = ContactInfo.objects.get_or_create(
        pk=1, 
        defaults={
            'address': 'Адрес университета',
            'phone': '+7 (727) XXX-XX-XX',
            'campus_items': 'Учебные корпуса\nБиблиотека\nСпортивные залы\nСтоловая'
        }
    )
    
    if request.method == 'POST':
        contact_info.address = request.POST.get('address', '')
        contact_info.address_en = request.POST.get('address_en', '')
        contact_info.address_kk = request.POST.get('address_kk', '')
        contact_info.phone = request.POST.get('phone', '')
        contact_info.campus_items = request.POST.get('campus_items', '')
        contact_info.campus_items_en = request.POST.get('campus_items_en', '')
        contact_info.campus_items_kk = request.POST.get('campus_items_kk', '')
        
        # Обработка 3D кампуса
        contact_info.campus_3d_enabled = 'campus_3d_enabled' in request.POST
        contact_info.campus_3d_url = request.POST.get('campus_3d_url', '')
        contact_info.campus_3d_button_text = request.POST.get('campus_3d_button_text', 'Изучить кампус в 3D')
        contact_info.campus_3d_button_text_en = request.POST.get('campus_3d_button_text_en', '')
        contact_info.campus_3d_button_text_kk = request.POST.get('campus_3d_button_text_kk', '')
        
        # Обработка IT поддержки
        contact_info.it_support_enabled = 'it_support_enabled' in request.POST
        contact_info.it_support_url = request.POST.get('it_support_url', '')
        
        # Обработка загруженного изображения
        if 'campus_image' in request.FILES:
            contact_info.campus_image = request.FILES['campus_image']
        
        contact_info.save()
        messages.success(request, 'Контактная информация успешно обновлена!')
        return redirect('main:admin_map')
    
    context = {
        'current_page': 'admin_map',
        'active_tab': 'map',
        'contact_info': contact_info,
    }
    return render(request, 'main/admin/map.html', context)

@login_required
def admin_faq_view(request):
    """Админка для страницы 'Часто задаваемые вопросы'"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем все категории и вопросы
    categories = FAQCategory.objects.filter(is_active=True).order_by('order_index')
    faqs = FAQ.objects.filter(is_active=True).order_by('category__order_index', 'order_index')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_category':
            name = request.POST.get('name', '')
            name_en = request.POST.get('name_en', '')
            name_kk = request.POST.get('name_kk', '')
            description = request.POST.get('description', '')
            description_en = request.POST.get('description_en', '')
            description_kk = request.POST.get('description_kk', '')
            order_index = request.POST.get('order_index', 0)
            
            FAQCategory.objects.create(
                name=name,
                name_en=name_en,
                name_kk=name_kk,
                description=description,
                description_en=description_en,
                description_kk=description_kk,
                order_index=order_index
            )
            messages.success(request, 'Категория успешно добавлена!')
            
        elif action == 'add_faq':
            question = request.POST.get('question', '')
            question_en = request.POST.get('question_en', '')
            question_kk = request.POST.get('question_kk', '')
            answer = request.POST.get('answer', '')
            answer_en = request.POST.get('answer_en', '')
            answer_kk = request.POST.get('answer_kk', '')
            category_id = request.POST.get('category')
            order_index = request.POST.get('order_index', 0)
            is_popular = 'is_popular' in request.POST
            
            try:
                category = FAQCategory.objects.get(pk=category_id)
                FAQ.objects.create(
                    question=question,
                    question_en=question_en,
                    question_kk=question_kk,
                    answer=answer,
                    answer_en=answer_en,
                    answer_kk=answer_kk,
                    category=category,
                    order_index=order_index,
                    is_popular=is_popular
                )
                messages.success(request, 'Вопрос успешно добавлен!')
            except FAQCategory.DoesNotExist:
                messages.error(request, 'Категория не найдена!')
        
        return redirect('main:admin_faq')
    
    context = {
        'current_page': 'admin_faq',
        'active_tab': 'faq',
        'categories': categories,
        'faqs': faqs,
    }
    return render(request, 'main/admin/faq.html', context)

@login_required
def admin_feedback_view(request):
    """Админка для страницы 'Обратная связь'"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем все обращения
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        new_status = request.POST.get('status')
        
        # Отладочная информация
        print(f"DEBUG: feedback_id = {feedback_id}, new_status = {new_status}")
        print(f"DEBUG: POST data = {request.POST}")
        
        if feedback_id and new_status and new_status.strip():
            try:
                feedback = Feedback.objects.get(pk=feedback_id)
                # Проверяем, что статус валидный
                valid_statuses = ['new', 'in_progress', 'resolved', 'closed']
                if new_status in valid_statuses:
                    old_status = feedback.status
                    feedback.status = new_status
                    feedback.save()
                    messages.success(request, f'Статус обращения #{feedback_id} изменен с "{feedback.get_status_display()}" на "{new_status}"!')
                else:
                    messages.error(request, f'Неверный статус: {new_status}. Допустимые значения: {", ".join(valid_statuses)}')
            except Feedback.DoesNotExist:
                messages.error(request, f'Обращение с ID {feedback_id} не найдено!')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении статуса: {str(e)}')
                print(f"ERROR: {str(e)}")
        else:
            if not feedback_id:
                messages.error(request, 'ID обращения не указан!')
            elif not new_status:
                messages.error(request, 'Новый статус не указан!')
            else:
                messages.error(request, 'Неверные данные для обновления статуса!')
        
        return redirect('main:admin_feedback')
    
    context = {
        'current_page': 'admin_feedback',
        'active_tab': 'feedback',
        'feedbacks': feedbacks,
    }
    return render(request, 'main/admin/feedback.html', context)

@login_required
def admin_lessons_view(request):
    """Админка для страницы 'Уроки'"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем все уроки
    lessons = Lesson.objects.filter(is_active=True).order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_lesson':
            title = request.POST.get('title', '')
            title_en = request.POST.get('title_en', '')
            title_kk = request.POST.get('title_kk', '')
            description = request.POST.get('description', '')
            description_en = request.POST.get('description_en', '')
            description_kk = request.POST.get('description_kk', '')
            difficulty_level = request.POST.get('difficulty_level', 'beginner')
            video = request.FILES.get('video')
            pdf_file = request.FILES.get('pdf_file')
            
            # Проверяем, не существует ли уже урок с таким названием
            if Lesson.objects.filter(title=title).exists():
                messages.error(request, f'Урок с названием "{title}" уже существует!')
            else:
                # Создаем урок
                lesson = Lesson.objects.create(
                    title=title,
                    title_en=title_en,
                    title_kk=title_kk,
                    description=description,
                    description_en=description_en,
                    description_kk=description_kk,
                    difficulty_level=difficulty_level,
                    video=video,
                    pdf_file=pdf_file
                )
                messages.success(request, f'Урок "{title}" успешно добавлен!')
        
        elif action == 'edit_lesson':
            lesson_id = request.POST.get('lesson_id')
            try:
                lesson = Lesson.objects.get(pk=lesson_id)
                lesson.title = request.POST.get('title', lesson.title)
                lesson.title_en = request.POST.get('title_en', lesson.title_en)
                lesson.title_kk = request.POST.get('title_kk', lesson.title_kk)
                lesson.description = request.POST.get('description', lesson.description)
                lesson.description_en = request.POST.get('description_en', lesson.description_en)
                lesson.description_kk = request.POST.get('description_kk', lesson.description_kk)
                lesson.difficulty_level = request.POST.get('difficulty_level', lesson.difficulty_level)
                
                if 'video' in request.FILES:
                    lesson.video = request.FILES['video']
                if 'pdf_file' in request.FILES:
                    lesson.pdf_file = request.FILES['pdf_file']
                
                lesson.save()  # Длительность будет пересчитана автоматически
                messages.success(request, f'Урок "{lesson.title}" успешно обновлен!')
            except Lesson.DoesNotExist:
                messages.error(request, 'Урок не найден!')
        
        elif action == 'restore_test_lessons':
            # Сбрасываем флаг удаления тестовых уроков
            request.session['test_lessons_deleted'] = False
            messages.success(request, 'Флаг удаления тестовых уроков сброшен. Тестовые уроки будут созданы при следующем обновлении страницы.')
        
        elif action == 'delete_lesson':
            lesson_id = request.POST.get('lesson_id')
            try:
                lesson = Lesson.objects.get(pk=lesson_id)
                lesson_title = lesson.title
                
                # Проверяем, является ли это тестовым уроком
                is_test_lesson = lesson_title in ["Введение в адаптацию", "Работа с документами", "Продвинутые техники обучения"]
                
                # Проверяем связанные данные перед удалением
                related_data = []
                if lesson.completed_users.exists():
                    related_data.append(f"завершили урок ({lesson.completed_users.count()} пользователей)")
                if lesson.slides.exists():
                    related_data.append(f"слайды ({lesson.slides.count()} шт.)")
                if lesson.user_progress.exists():
                    related_data.append(f"прогресс пользователей ({lesson.user_progress.count()} записей)")
                
                if related_data:
                    # Если есть связанные данные, удаляем их сначала
                    lesson.completed_users.clear()
                    lesson.slides.all().delete()
                    lesson.user_progress.all().delete()
                    messages.warning(request, f'Урок "{lesson_title}" удален вместе со связанными данными: {", ".join(related_data)}')
                else:
                    messages.success(request, f'Урок "{lesson_title}" успешно удален!')
                
                lesson.delete()
                
                # Если удалили тестовый урок, устанавливаем флаг
                if is_test_lesson:
                    request.session['test_lessons_deleted'] = True
                    messages.info(request, 'Тестовые уроки удалены. Они не будут автоматически воссоздаваться.')
                
            except Lesson.DoesNotExist:
                messages.error(request, 'Урок не найден!')
            except Exception as e:
                messages.error(request, f'Ошибка при удалении урока: {str(e)}')
                print(f"DEBUG: Ошибка удаления урока {lesson_id}: {str(e)}")
        
        return redirect('main:admin_lessons')
    
    # После обработки POST-запросов получаем обновленный список уроков
    lessons = Lesson.objects.filter(is_active=True).order_by('-created_at')
    
    # Создаем тестовые уроки только если их нет И если пользователь не удалял их намеренно
    if not lessons and not request.session.get('test_lessons_deleted', False):
        # Проверяем, есть ли уже тестовые уроки в базе данных
        existing_test_lessons = Lesson.objects.filter(
            title__in=["Введение в адаптацию", "Работа с документами", "Продвинутые техники обучения"]
        )
        
        if not existing_test_lessons.exists():
            # Создаем и сохраняем тестовые уроки только если их нет
            test_lessons = [
                Lesson(
                    title="Введение в адаптацию",
                    description="Базовый урок по адаптации к университетской жизни",
                    difficulty_level='beginner'
                ),
                Lesson(
                    title="Работа с документами",
                    description="Как правильно оформлять и подавать документы",
                    difficulty_level='intermediate'
                ),
                Lesson(
                    title="Продвинутые техники обучения",
                    description="Эффективные методы изучения материала",
                    difficulty_level='advanced'
                )
            ]
            
            # Сохраняем уроки в базе данных
            for lesson in test_lessons:
                lesson.save()
            
            lessons = test_lessons
        else:
            # Если тестовые уроки уже есть, используем их
            lessons = list(existing_test_lessons)
    else:
        # Если уроки есть, просто обновляем список
        lessons = list(lessons)
    
    context = {
        'current_page': 'admin_lessons',
        'lessons': lessons,
        'test_lessons_deleted': request.session.get('test_lessons_deleted', False),
    }
    return render(request, 'main/admin/lessons.html', context)

@login_required
def get_lesson_data(request, lesson_id):
    """Получение данных урока для редактирования по AJAX"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
        data = {
            'id': lesson.id,
            'title': lesson.title,
            'title_en': lesson.title_en or '',
            'title_kk': lesson.title_kk or '',
            'description': lesson.description,
            'description_en': lesson.description_en or '',
            'description_kk': lesson.description_kk or '',
            'difficulty_level': lesson.difficulty_level,
            'duration': lesson.duration,  # Теперь это свойство
            'has_video': bool(lesson.video),
            'has_pdf': bool(lesson.pdf_file),
            'video_url': lesson.video.url if lesson.video else None,
            'pdf_url': lesson.pdf_file.url if lesson.pdf_file else None,
        }
        print(f"DEBUG: Возвращаем данные для урока {lesson_id}: {data}")  # Отладочная информация
        return JsonResponse(data)
    except Lesson.DoesNotExist:
        print(f"DEBUG: Урок {lesson_id} не найден")  # Отладочная информация
        return JsonResponse({'error': 'Урок не найден'}, status=404)
    except Exception as e:
        print(f"DEBUG: Ошибка при получении данных урока {lesson_id}: {str(e)}")  # Отладочная информация
        return JsonResponse({'error': f'Ошибка сервера: {str(e)}'}, status=500)

@login_required
def admin_teachers_view(request):
    """Админка для управления преподавателями"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем всех преподавателей
    teachers = Teacher.objects.filter(is_active=True).order_by('full_name')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_teacher':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            full_name = request.POST.get('full_name', '')
            department = request.POST.get('department', '')
            position = request.POST.get('position', '')
            phone = request.POST.get('phone', '')
            office = request.POST.get('office', '')
            
            # Создаем пользователя
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=full_name.split()[0] if full_name else '',
                    last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                )
                
                # Создаем преподавателя
                Teacher.objects.create(
                    user=user,
                    full_name=full_name,
                    department=department,
                    position=position,
                    phone=phone,
                    office=office
                )
                messages.success(request, f'Преподаватель {full_name} успешно добавлен!')
            except Exception as e:
                messages.error(request, f'Ошибка при создании преподавателя: {str(e)}')
        
        return redirect('main:admin_teachers')
    
    context = {
        'current_page': 'admin_teachers',
        'active_tab': 'teachers',
        'teachers': teachers,
    }
    return render(request, 'main/admin/teachers.html', context)

@login_required
def admin_documents_view(request):
    """Админка для управления документами"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем все документы и категории
    documents = Document.objects.filter(is_active=True).order_by('-created_at')
    categories = DocumentCategory.objects.filter(is_active=True).order_by('order_index')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_document':
            title = request.POST.get('title', '')
            title_en = request.POST.get('title_en', '')
            title_kk = request.POST.get('title_kk', '')
            description = request.POST.get('description', '')
            description_en = request.POST.get('description_en', '')
            description_kk = request.POST.get('description_kk', '')
            category_id = request.POST.get('category')
            
            if category_id:
                try:
                    category = DocumentCategory.objects.get(id=category_id)
                    
                    # Создаем документ
                    document = Document.objects.create(
                        title=title,
                        title_en=title_en,
                        title_kk=title_kk,
                        description=description,
                        description_en=description_en,
                        description_kk=description_kk,
                        category=category,
                        uploaded_by=request.user
                    )
                    
                    # Обрабатываем файлы
                    if 'file' in request.FILES:
                        document.file = request.FILES['file']
                    if 'file_en' in request.FILES:
                        document.file_en = request.FILES['file_en']
                    if 'file_kk' in request.FILES:
                        document.file_kk = request.FILES['file_kk']
                    
                    document.save()
                    messages.success(request, 'Документ успешно добавлен!')
                except DocumentCategory.DoesNotExist:
                    messages.error(request, 'Категория не найдена!')
            else:
                messages.error(request, 'Выберите категорию!')
        
        elif action == 'delete_document':
            document_id = request.POST.get('document_id')
            try:
                document = Document.objects.get(id=document_id)
                document.is_active = False
                document.save()
                messages.success(request, 'Документ успешно удален!')
            except Document.DoesNotExist:
                messages.error(request, 'Документ не найден!')
        
        elif action == 'add_category':
            name = request.POST.get('name', '')
            name_en = request.POST.get('name_en', '')
            name_kk = request.POST.get('name_kk', '')
            description = request.POST.get('description', '')
            description_en = request.POST.get('description_en', '')
            description_kk = request.POST.get('description_kk', '')
            order_index = request.POST.get('order_index', 0)
            
            if name:
                DocumentCategory.objects.create(
                    name=name,
                    name_en=name_en,
                    name_kk=name_kk,
                    description=description,
                    description_en=description_en,
                    description_kk=description_kk,
                    order_index=order_index or 0
                )
                messages.success(request, 'Категория успешно добавлена!')
            else:
                messages.error(request, 'Название категории обязательно!')
        
        return redirect('main:admin_documents')
    
    context = {
        'current_page': 'admin_documents',
        'active_tab': 'documents',
        'documents': documents,
        'categories': categories,
    }
    return render(request, 'main/admin/documents.html', context)

@login_required
def admin_document_category_add_view(request):
    """Админка для добавления категорий документов"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        name_en = request.POST.get('name_en', '')
        name_kk = request.POST.get('name_kk', '')
        description = request.POST.get('description', '')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        order_index = request.POST.get('order_index', 0)
        
        if name:
            DocumentCategory.objects.create(
                name=name,
                name_en=name_en,
                name_kk=name_kk,
                description=description,
                description_en=description_en,
                description_kk=description_kk,
                order_index=order_index or 0
            )
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('main:admin_documents')
        else:
            messages.error(request, 'Название категории обязательно!')
    
    context = {
        'current_page': 'admin_document_category_add',
        'active_tab': 'categories',
    }
    return render(request, 'main/admin/document_category_add.html', context)

@login_required
def admin_leaders_view(request):
    """Админка для управления руководством университета"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем всех руководителей
    leaders = Leader.objects.all().order_by('order', 'role')
    
    # Отладочная информация
    print(f"DEBUG: Found {leaders.count()} leaders in admin_leaders_view")
    for leader in leaders:
        print(f"DEBUG: Leader - ID: {leader.id}, Name: {leader.full_name}, Role: {leader.role}")
    
    if request.method == 'POST':
        # Отладочная информация для всех POST запросов
        print(f"DEBUG: POST request received in admin_leaders_view")
        print(f"DEBUG: POST data: {request.POST}")
        print(f"DEBUG: FILES data: {request.FILES}")
        
        action = request.POST.get('action')
        
        if action == 'add_leader':
            # Добавление нового руководителя
            role = request.POST.get('role', '')
            full_name = request.POST.get('full_name', '')
            photo = request.FILES.get('photo')
            order = int(request.POST.get('order', 1))
            
            # Отладочная информация
            print(f"DEBUG: Adding leader - role={role}, full_name={full_name}, photo={photo}, order={order}")
            
            if role and full_name:
                try:
                    leader = Leader.objects.create(
                        role=role,
                        full_name=full_name,
                        photo=photo,
                        order=order
                    )
                    messages.success(request, f'Руководитель {full_name} успешно добавлен!')
                    print(f"DEBUG: Leader created successfully with ID {leader.id}")
                except Exception as e:
                    messages.error(request, f'Ошибка при создании руководителя: {str(e)}')
                    print(f"DEBUG: Error creating leader: {e}")
            else:
                messages.error(request, 'Роль и ФИО обязательны для заполнения!')
                print(f"DEBUG: Missing required fields - role: {bool(role)}, full_name: {bool(full_name)}")
                
        elif action == 'update_leader':
            # Обновление руководителя
            leader_id = request.POST.get('leader_id')
            print(f"DEBUG: Updating leader with ID: {leader_id}")
            
            try:
                leader = Leader.objects.get(pk=leader_id)
                leader.role = request.POST.get('role', leader.role)
                leader.full_name = request.POST.get('full_name', leader.full_name)
                
                if 'photo' in request.FILES:
                    leader.photo = request.FILES['photo']
                
                leader.order = int(request.POST.get('order', leader.order))
                leader.is_active = request.POST.get('is_active') == 'on'
                leader.save()
                
                messages.success(request, f'Руководитель {leader.full_name} успешно обновлен!')
                print(f"DEBUG: Leader updated successfully")
            except Leader.DoesNotExist:
                messages.error(request, 'Руководитель не найден!')
                print(f"DEBUG: Leader not found with ID: {leader_id}")
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении руководителя: {str(e)}')
                print(f"DEBUG: Error updating leader: {e}")
                
        elif action == 'delete_leader':
            # Удаление руководителя
            leader_id = request.POST.get('leader_id')
            print(f"DEBUG: Deleting leader with ID: {leader_id}")
            
            try:
                leader = Leader.objects.get(pk=leader_id)
                leader_name = leader.full_name
                leader.delete()
                messages.success(request, f'Руководитель {leader_name} успешно удален!')
                print(f"DEBUG: Leader deleted successfully")
            except Leader.DoesNotExist:
                messages.error(request, 'Руководитель не найден!')
                print(f"DEBUG: Leader not found with ID: {leader_id}")
            except Exception as e:
                messages.error(request, f'Ошибка при удалении руководителя: {str(e)}')
                print(f"DEBUG: Error deleting leader: {e}")
        
        return redirect('main:admin_leaders')
    
    context = {
        'current_page': 'admin_leaders',
        'active_tab': 'leaders',
        'leaders': leaders,
    }
    return render(request, 'main/admin/leaders.html', context)

@login_required
def admin_process_add_view(request):
    """Добавление нового процесса"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    if request.method == 'POST':
        title = request.POST.get('title', '')
        title_en = request.POST.get('title_en', '')
        title_kk = request.POST.get('title_kk', '')
        description = request.POST.get('description', '')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        
        Process.objects.create(
            title=title,
            title_en=title_en,
            title_kk=title_kk,
            description=description,
            description_en=description_en,
            description_kk=description_kk
        )
        messages.success(request, 'Процесс успешно добавлен!')
        return redirect('main:admin_processes')
    
    context = {
        'current_page': 'admin_processes',
        'active_tab': 'processes',
        'form_type': 'process',
    }
    return render(request, 'main/admin/process_form.html', context)

@login_required
def admin_process_edit_view(request, process_id):
    """Редактирование процесса"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        process = Process.objects.get(id=process_id, is_active=True)
    except Process.DoesNotExist:
        messages.error(request, 'Процесс не найден!')
        return redirect('main:admin_processes')
    
    if request.method == 'POST':
        process.title = request.POST.get('title', '')
        process.title_en = request.POST.get('title_en', '')
        process.title_kk = request.POST.get('title_kk', '')
        process.description = request.POST.get('description', '')
        process.description_en = request.POST.get('description_en', '')
        process.description_kk = request.POST.get('description_kk', '')
        process.save()
        
        messages.success(request, 'Процесс успешно обновлен!')
        return redirect('main:admin_processes')
    
    context = {
        'current_page': 'admin_processes',
        'active_tab': 'processes',
        'form_type': 'process',
        'process': process,
    }
    return render(request, 'main/admin/process_form.html', context)

@login_required
def admin_process_delete_view(request, process_id):
    """Удаление процесса"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        process = Process.objects.get(id=process_id, is_active=True)
        process.is_active = False
        process.save()
        messages.success(request, 'Процесс успешно удален!')
    except Process.DoesNotExist:
        messages.error(request, 'Процесс не найден!')
    
    return redirect('main:admin_processes')

@login_required
def admin_instruction_add_view(request):
    """Добавление новой инструкции"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    if request.method == 'POST':
        title = request.POST.get('title', '')
        title_en = request.POST.get('title_en', '')
        title_kk = request.POST.get('title_kk', '')
        description = request.POST.get('description', '')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        
        Instruction.objects.create(
            title=title,
            title_en=title_en,
            title_kk=title_kk,
            description=description,
            description_en=description_en,
            description_kk=description_kk
        )
        messages.success(request, 'Инструкция успешно добавлена!')
        return redirect('main:admin_processes')
    
    context = {
        'current_page': 'admin_processes',
        'active_tab': 'processes',
        'form_type': 'instruction',
    }
    return render(request, 'main/admin/process_form.html', context)

@login_required
def admin_instruction_edit_view(request, instruction_id):
    """Редактирование инструкции"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        instruction = Instruction.objects.get(id=instruction_id, is_active=True)
    except Instruction.DoesNotExist:
        messages.error(request, 'Инструкция не найдена!')
        return redirect('main:admin_processes')
    
    if request.method == 'POST':
        instruction.title = request.POST.get('title', '')
        instruction.title_en = request.POST.get('title_en', '')
        instruction.title_kk = request.POST.get('title_kk', '')
        instruction.description = request.POST.get('description', '')
        instruction.description_en = request.POST.get('description_en', '')
        instruction.description_kk = request.POST.get('description_kk', '')
        instruction.save()
        
        messages.success(request, 'Инструкция успешно обновлена!')
        return redirect('main:admin_processes')
    
    context = {
        'current_page': 'admin_processes',
        'active_tab': 'processes',
        'form_type': 'instruction',
        'instruction': instruction,
    }
    return render(request, 'main/admin/process_form.html', context)

@login_required
def admin_instruction_delete_view(request, instruction_id):
    """Удаление инструкции"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        instruction = Instruction.objects.get(id=instruction_id, is_active=True)
        instruction.is_active = False
        instruction.save()
        messages.success(request, 'Инструкция успешно удалена!')
    except Instruction.DoesNotExist:
        messages.error(request, 'Инструкция не найдена!')
    
    return redirect('main:admin_processes')

@login_required
def admin_users_view(request):
    """Админка для управления пользователями"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    # Получаем всех пользователей, кроме администраторов
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('date_joined')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if action == 'create_user':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            is_active = request.POST.get('is_active') == 'on'
            
            # Валидация
            if not username or not email or not password1:
                messages.error(request, 'Пожалуйста, заполните все обязательные поля!')
            elif password1 != password2:
                messages.error(request, 'Пароли не совпадают!')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует!')
            else:
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1,
                        first_name=first_name,
                        last_name=last_name,
                        is_active=is_active
                    )
                    messages.success(request, f'Пользователь {username} успешно создан!')
                except Exception as e:
                    messages.error(request, f'Ошибка при создании пользователя: {str(e)}')
        
        elif action == 'deactivate_user' and user_id:
            try:
                user = User.objects.get(id=user_id, is_staff=False, is_superuser=False)
                user.is_active = False
                user.save()
                messages.success(request, f'Пользователь {user.username} деактивирован!')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь не найден!')
        
        elif action == 'activate_user' and user_id:
            try:
                user = User.objects.get(id=user_id, is_staff=False, is_superuser=False)
                user.is_active = True
                user.save()
                messages.success(request, f'Пользователь {user.username} активирован!')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь не найден!')
        
        elif action == 'delete_user' and user_id:
            try:
                user = User.objects.get(id=user_id, is_staff=False, is_superuser=False)
                username = user.username
                user.delete()
                messages.success(request, f'Пользователь {username} удален!')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь не найден!')
        
        return redirect('main:admin_users')
    
    context = {
        'current_page': 'admin_users',
        'active_tab': 'users',
        'users': users,
    }
    return render(request, 'main/admin/users.html', context)

@login_required
def admin_user_progress_view(request, user_id):
    """Просмотр прогресса пользователя по урокам - новая версия"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        user = User.objects.get(id=user_id, is_staff=False, is_superuser=False)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден!')
        return redirect('main:admin_users')
    
    try:
        # Получаем все активные уроки
        lessons = Lesson.objects.filter(is_active=True).order_by('id')
        
        # Собираем данные о прогрессе
        progress_data = []
        total_lessons = 0
        completed_lessons = 0
        in_progress_lessons = 0
        not_started_lessons = 0
        
        for lesson in lessons:
            total_lessons += 1
            
            # Получаем прогресс пользователя для этого урока
            try:
                progress = LessonProgress.objects.get(user=user, lesson=lesson)
                
                # Безопасно получаем значения прогресса
                video_progress = 0
                slides_progress = 0
                slides_current = 0
                slides_total = 0
                video_current_time = 0
                video_total_time = 0
                
                # Обрабатываем прогресс видео
                if hasattr(progress, 'video_max_progress_percent'):
                    try:
                        raw_value = progress.video_max_progress_percent
                        if raw_value is not None:
                            video_progress = float(raw_value)
                        else:
                            video_progress = 0
                    except (ValueError, TypeError):
                        video_progress = 0
                
                if hasattr(progress, 'video_current_time'):
                    try:
                        raw_value = progress.video_current_time
                        if raw_value is not None:
                            video_current_time = float(raw_value)
                        else:
                            video_current_time = 0
                    except (ValueError, TypeError):
                        video_current_time = 0
                        
                if hasattr(progress, 'video_total_time'):
                    try:
                        raw_value = progress.video_total_time
                        if raw_value is not None:
                            video_total_time = float(raw_value)
                        else:
                            video_total_time = 0
                    except (ValueError, TypeError):
                        video_total_time = 0
                
                # Обрабатываем прогресс слайдов
                if hasattr(progress, 'slides_current_slide'):
                    try:
                        raw_value = progress.slides_current_slide
                        if raw_value is not None:
                            slides_current = int(raw_value)
                        else:
                            slides_current = 0
                    except (ValueError, TypeError):
                        slides_current = 0
                        
                if hasattr(progress, 'slides_total_slides'):
                    try:
                        raw_value = progress.slides_total_slides
                        if raw_value is not None:
                            slides_total = int(raw_value)
                        else:
                            slides_total = 0
                    except (ValueError, TypeError):
                        slides_total = 0
                
                # Вычисляем максимальный процент прогресса слайдов
                if hasattr(progress, 'slides_max_progress_percent'):
                    try:
                        slides_progress = float(progress.slides_max_progress_percent or 0)
                    except (ValueError, TypeError):
                        slides_progress = 0
                else:
                    # Fallback к старому способу расчета
                    if slides_total > 0:
                        slides_progress = (slides_current / slides_total) * 100
                    else:
                        slides_progress = 0
                
                # Определяем общий прогресс урока
                lesson_progress = 0
                if lesson.video and lesson.pdf_file:
                    # Если есть и видео и PDF, берем среднее
                    lesson_progress = (video_progress + slides_progress) / 2
                elif lesson.video:
                    lesson_progress = video_progress
                elif lesson.pdf_file:
                    lesson_progress = slides_progress
                
                # Определяем статус урока - сначала проверяем LessonCompletion
                if lesson.is_completed_by_user(user):
                    status = 'completed'
                    completed_lessons += 1
                elif lesson_progress >= 100:
                    status = 'completed'
                    completed_lessons += 1
                elif lesson_progress > 0:
                    status = 'in_progress'
                    in_progress_lessons += 1
                else:
                    status = 'not_started'
                    not_started_lessons += 1
                
                # Вычисляем максимальный слайд на основе максимального прогресса
                max_slides_current = 0
                if slides_total > 0 and slides_progress > 0:
                    max_slides_current = int((slides_progress / 100) * slides_total)
                
                progress_data.append({
                    'lesson': lesson,
                    'progress': progress,
                    'video_progress': video_progress,
                    'slides_progress': slides_progress,
                    'slides_current': max_slides_current,  # Используем максимальный слайд
                    'slides_total': slides_total,
                    'video_current_time': video_current_time,
                    'video_total_time': video_total_time,
                    'lesson_progress': lesson_progress,
                    'status': status,
                    'has_progress': True
                })
                
            except LessonProgress.DoesNotExist:
                # Прогресса нет - урок не начат
                progress_data.append({
                    'lesson': lesson,
                    'progress': None,
                    'video_progress': 0,
                    'slides_progress': 0,
                    'slides_current': 0,
                    'slides_total': 0,
                    'video_current_time': 0,
                    'video_total_time': 0,
                    'lesson_progress': 0,
                    'status': 'not_started',
                    'has_progress': False
                })
                print(f"DEBUG: Добавлен урок без прогресса {lesson.id}: статус=not_started")
                not_started_lessons += 1
            except Exception as e:
                # Пропускаем проблемный урок
                continue
        
        context = {
            'current_page': 'admin_users',
            'active_tab': 'users',
            'user': user,
            'progress_data': progress_data,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'in_progress_lessons': in_progress_lessons,
            'not_started_lessons': not_started_lessons,
        }
        
        return render(request, 'main/admin/user_progress.html', context)
        
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке прогресса: {str(e)}')
        return redirect('main:admin_users')

@login_required
def admin_document_edit_view(request, document_id):
    """Редактирование документа в админке"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        document = Document.objects.get(id=document_id, is_active=True)
    except Document.DoesNotExist:
        messages.error(request, 'Документ не найден!')
        return redirect('main:admin_documents')
    
    categories = DocumentCategory.objects.filter(is_active=True).order_by('order_index')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_document':
            # Обновляем основные поля
            document.title = request.POST.get('title', '')
            document.title_en = request.POST.get('title_en', '')
            document.title_kk = request.POST.get('title_kk', '')
            document.description = request.POST.get('description', '')
            document.description_en = request.POST.get('description_en', '')
            document.description_kk = request.POST.get('description_kk', '')
            
            # Обновляем категорию
            category_id = request.POST.get('category')
            if category_id:
                try:
                    category = DocumentCategory.objects.get(id=category_id)
                    document.category = category
                except DocumentCategory.DoesNotExist:
                    messages.error(request, 'Категория не найдена!')
                    return redirect('main:admin_document_edit', document_id=document_id)
            
            # Обрабатываем новые файлы
            if 'file' in request.FILES and request.FILES['file']:
                document.file = request.FILES['file']
            if 'file_en' in request.FILES and request.FILES['file_en']:
                document.file_en = request.FILES['file_en']
            if 'file_kk' in request.FILES and request.FILES['file_kk']:
                document.file_kk = request.FILES['file_kk']
            
            document.save()
            messages.success(request, 'Документ успешно обновлен!')
            return redirect('main:admin_documents')
    
    context = {
        'current_page': 'admin_documents',
        'active_tab': 'documents',
        'document': document,
        'categories': categories,
    }
    return render(request, 'main/admin/document_edit.html', context)

@login_required
def admin_document_delete_view(request, document_id):
    """Удаление документа в админке"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        document = Document.objects.get(id=document_id, is_active=True)
        document.is_active = False
        document.save()
        messages.success(request, 'Документ успешно удален!')
    except Document.DoesNotExist:
        messages.error(request, 'Документ не найден!')
    
    return redirect('main:admin_documents')

@login_required
def admin_faq_edit_view(request, faq_id):
    """Редактирование FAQ в админке"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        faq = FAQ.objects.get(id=faq_id, is_active=True)
    except FAQ.DoesNotExist:
        messages.error(request, 'FAQ не найден!')
        return redirect('main:admin_faq')
    
    categories = FAQCategory.objects.filter(is_active=True).order_by('order_index')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_faq':
            # Обновляем основные поля
            faq.question = request.POST.get('question', '')
            faq.question_en = request.POST.get('question_en', '')
            faq.question_kk = request.POST.get('question_kk', '')
            faq.answer = request.POST.get('answer', '')
            faq.answer_en = request.POST.get('answer_en', '')
            faq.answer_kk = request.POST.get('answer_kk', '')
            
            # Обновляем категорию
            category_id = request.POST.get('category')
            if category_id:
                try:
                    category = FAQCategory.objects.get(id=category_id)
                    faq.category = category
                except FAQCategory.DoesNotExist:
                    messages.error(request, 'Категория не найдена!')
                    return redirect('main:admin_faq_edit', faq_id=faq_id)
            
            faq.save()
            messages.success(request, 'FAQ успешно обновлен!')
            return redirect('main:admin_faq')
    
    context = {
        'current_page': 'admin_faq',
        'active_tab': 'faq',
        'faq': faq,
        'categories': categories,
    }
    return render(request, 'main/admin/faq_edit.html', context)

@login_required
def admin_faq_delete_view(request, faq_id):
    """Удаление FAQ в админке"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    try:
        faq = FAQ.objects.get(id=faq_id, is_active=True)
        faq.is_active = False
        faq.save()
        messages.success(request, 'FAQ успешно удален!')
    except FAQ.DoesNotExist:
        messages.error(request, 'FAQ не найден!')
    
    return redirect('main:admin_faq')

@login_required
def set_theme_view(request):
    """Установка темы интерфейса"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            theme = data.get('theme', 'light')
            
            # Сохраняем тему в сессии
            request.session['selected_theme'] = theme
            
            return JsonResponse({
                'success': True,
                'theme': theme
            })
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({
                'success': False,
                'error': 'Неверные данные'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Метод не поддерживается'
    })

@login_required
def test_theme_view(request):
    """Тестовая страница для проверки темной темы"""
    return render(request, 'main/test_theme.html')

@login_required
def test_simple_view(request):
    """Простая тестовая страница для проверки темной темы"""
    return render(request, 'main/test_simple.html')

# ===== EDITOR VIEWS =====

def editor_login_view(request):
    """Страница логина для редакторов"""
    # Если пользователь уже авторизован и является редактором
    if request.user.is_authenticated:
        try:
            editor = Editor.objects.get(user=request.user)
            if editor.is_verified:
                return redirect('main:editor_dashboard')
        except Editor.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = EditorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Находим пользователя по email (может быть несколько с одинаковым email)
                user = User.objects.filter(email=email).first()
                if user:
                    user = authenticate(request, username=user.username, password=password)
                else:
                    user = None
                
                if user is not None:
                    try:
                        editor = Editor.objects.get(user=user)
                        if editor.is_verified:
                            login(request, user)
                            return redirect('main:editor_dashboard')
                        else:
                            messages.error(request, 'Ваш аккаунт редактора неактивен. Обратитесь к администратору.')
                    except Editor.DoesNotExist:
                        messages.error(request, 'У вас нет прав редактора.')
                else:
                    messages.error(request, 'Неверные учетные данные.')
            except Exception as e:
                messages.error(request, 'Произошла ошибка при входе в систему.')
    else:
        form = EditorLoginForm()
    
    return render(request, 'main/editor_login.html', {'form': form})


def editor_logout_view(request):
    """Выход редактора из системы"""
    logout(request)
    return redirect('main:editor_login')


@login_required
def editor_dashboard_view(request):
    """Дашборд редактора"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    # Получаем уроки, созданные этим редактором
    lessons = editor.get_lessons()
    
    # Получаем документы, загруженные этим редактором
    documents = Document.objects.filter(uploaded_by=request.user)
    
    # Получаем все обращения обратной связи
    feedbacks = Feedback.objects.all().order_by('-created_at')
    feedback_count = feedbacks.count()
    
    context = {
        'editor': editor,
        'lessons': lessons,
        'lessons_count': lessons.count(),
        'active_lessons_count': lessons.filter(is_active=True).count(),
        'documents_count': documents.count(),
        'documents': documents,
        'feedback_count': feedback_count,
        'feedbacks': feedbacks,
    }
    return render(request, 'main/editor/dashboard.html', context)


@login_required
def admin_editors_view(request):
    """Админка для управления редакторами"""
    if not request.user.is_staff:
        return redirect('main:admin_login')
    
    editors = Editor.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Добавление нового редактора
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            full_name = request.POST.get('full_name')
            bio = request.POST.get('bio', '')
            
            # Валидация
            if not all([email, password, password_confirm, full_name]):
                messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            elif password != password_confirm:
                messages.error(request, 'Пароли не совпадают.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует.')
            else:
                try:
                    # Создаем пользователя
                    username = email.split('@')[0]  # Используем часть email как username
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name.split()[0] if full_name.split() else '',
                        last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                    )
                    
                    # Создаем редактора
                    editor = Editor.objects.create(
                        user=user,
                        email=email,
                        full_name=full_name,
                        bio=bio
                    )
                    
                    messages.success(request, f'Редактор {full_name} успешно добавлен!')
                except Exception as e:
                    messages.error(request, f'Ошибка при создании редактора: {str(e)}')
        
        elif action == 'edit':
            # Редактирование редактора
            editor_id = request.POST.get('editor_id')
            try:
                editor = Editor.objects.get(id=editor_id)
                editor.email = request.POST.get('email')
                editor.full_name = request.POST.get('full_name')
                editor.bio = request.POST.get('bio', '')
                
                # Обновляем пользователя
                editor.user.email = editor.email
                editor.user.first_name = editor.full_name.split()[0] if editor.full_name.split() else ''
                editor.user.last_name = ' '.join(editor.full_name.split()[1:]) if len(editor.full_name.split()) > 1 else ''
                editor.user.save()
                
                editor.save()
                messages.success(request, f'Редактор {editor.full_name} успешно обновлен!')
            except Editor.DoesNotExist:
                messages.error(request, 'Редактор не найден.')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении редактора: {str(e)}')
        
        elif action == 'toggle_status':
            # Изменение статуса редактора
            editor_id = request.POST.get('editor_id')
            activate = request.POST.get('activate') == 'True'
            try:
                editor = Editor.objects.get(id=editor_id)
                editor.is_active = activate
                editor.user.is_active = activate
                editor.user.save()
                editor.save()
                
                status_text = 'активирован' if activate else 'деактивирован'
                messages.success(request, f'Редактор {editor.full_name} {status_text}!')
            except Editor.DoesNotExist:
                messages.error(request, 'Редактор не найден.')
            except Exception as e:
                messages.error(request, f'Ошибка при изменении статуса: {str(e)}')
        
        elif action == 'delete':
            # Удаление редактора
            editor_id = request.POST.get('editor_id')
            try:
                editor = Editor.objects.get(id=editor_id)
                editor_name = editor.full_name
                editor.delete()  # Это также удалит связанного пользователя
                messages.success(request, f'Редактор {editor_name} успешно удален!')
            except Editor.DoesNotExist:
                messages.error(request, 'Редактор не найден.')
            except Exception as e:
                messages.error(request, f'Ошибка при удалении редактора: {str(e)}')
        
        return redirect('main:admin_editors')
    
    context = {
        'active_tab': 'editors',
        'editors': editors,
    }
    return render(request, 'main/admin/editors.html', context)

@login_required
def editor_lessons_view(request):
    """Страница управления уроками редактора"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete_lesson':
            lesson_id = request.POST.get('lesson_id')
            try:
                lesson = Lesson.objects.get(id=lesson_id, created_by=request.user)
                lesson_title = lesson.title
                lesson.delete()
                messages.success(request, f'Урок "{lesson_title}" успешно удален!')
            except Lesson.DoesNotExist:
                messages.error(request, 'Урок не найден.')
            try:
                from django.urls import reverse
                return redirect(f"{reverse('main:editor_dashboard')}?tab=lessons")
            except Exception:
                return redirect('main:editor_dashboard')
    
    lessons = editor.get_lessons()
    
    context = {
        'editor': editor,
        'lessons': lessons,
    }
    return render(request, 'main/editor/lessons.html', context)


@login_required
def editor_create_lesson_view(request):
    """Создание нового урока"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    if request.method == 'POST':
        # Логика создания урока
        title = request.POST.get('title')
        title_en = request.POST.get('title_en', '')
        title_kk = request.POST.get('title_kk', '')
        description = request.POST.get('description')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        category_id = request.POST.get('category')
        video = request.FILES.get('video')
        pdf_file = request.FILES.get('pdf_file')
        
        if title and description:
            lesson = Lesson.objects.create(
                title=title,
                title_en=title_en,
                title_kk=title_kk,
                description=description,
                description_en=description_en,
                description_kk=description_kk,
                created_by=request.user,
                category_id=category_id if category_id else None
            )
            
            # Обрабатываем загруженные файлы
            if video:
                lesson.video = video
            if pdf_file:
                lesson.pdf_file = pdf_file
            
            lesson.save()
            messages.success(request, 'Урок успешно создан!')
            try:
                from django.urls import reverse
                return redirect(f"{reverse('main:editor_dashboard')}?tab=lessons")
            except Exception:
                return redirect('main:editor_dashboard')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
    
    categories = LessonCategory.objects.all()
    context = {
        'editor': editor,
        'categories': categories,
    }
    return render(request, 'main/editor/create_lesson.html', context)


@login_required
def editor_edit_lesson_view(request, lesson_id):
    """Редактирование урока"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    try:
        lesson = Lesson.objects.get(id=lesson_id, created_by=request.user)
    except Lesson.DoesNotExist:
        messages.error(request, 'Урок не найден.')
        try:
            from django.urls import reverse
            return redirect(f"{reverse('main:editor_dashboard')}?tab=lessons")
        except Exception:
            return redirect('main:editor_dashboard')
    
    if request.method == 'POST':
        # Логика редактирования урока
        title = request.POST.get('title')
        title_en = request.POST.get('title_en', '')
        title_kk = request.POST.get('title_kk', '')
        description = request.POST.get('description')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        category_id = request.POST.get('category')
        is_active = request.POST.get('is_active') == 'on'
        video = request.FILES.get('video')
        pdf_file = request.FILES.get('pdf_file')
        
        if title and description:
            lesson.title = title
            lesson.title_en = title_en
            lesson.title_kk = title_kk
            lesson.description = description
            lesson.description_en = description_en
            lesson.description_kk = description_kk
            lesson.category_id = category_id if category_id else None
            lesson.is_active = is_active
            
            # Обрабатываем загруженные файлы
            if video:
                lesson.video = video
            if pdf_file:
                lesson.pdf_file = pdf_file
            
            lesson.save()
            messages.success(request, 'Урок успешно обновлен!')
            return redirect('main:editor_lessons')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
    
    categories = LessonCategory.objects.all()
    context = {
        'editor': editor,
        'lesson': lesson,
        'categories': categories,
    }
    return render(request, 'main/editor/edit_lesson.html', context)


@login_required
def editor_documents_view(request):
    """Страница управления документами редактора"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete_document':
            document_id = request.POST.get('document_id')
            try:
                document = Document.objects.get(id=document_id, uploaded_by=request.user)
                document_title = document.title
                document.delete()
                messages.success(request, f'Документ "{document_title}" успешно удален!')
            except Document.DoesNotExist:
                messages.error(request, 'Документ не найден.')
            try:
                from django.urls import reverse
                return redirect(f"{reverse('main:editor_dashboard')}?tab=documents")
            except Exception:
                return redirect('main:editor_dashboard')
    
    # Получаем документы, загруженные редактором
    documents = Document.objects.filter(uploaded_by=request.user).order_by('-created_at')
    
    context = {
        'editor': editor,
        'documents': documents,
    }
    return render(request, 'main/editor/documents.html', context)


@login_required
def editor_create_document_view(request):
    """Создание нового документа"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    if request.method == 'POST':
        # Логика создания документа
        title = request.POST.get('title')
        title_en = request.POST.get('title_en', '')
        title_kk = request.POST.get('title_kk', '')
        description = request.POST.get('description')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        file = request.FILES.get('file')
        file_en = request.FILES.get('file_en')
        file_kk = request.FILES.get('file_kk')
        category_id = request.POST.get('category')
        
        if title and file:
            document = Document.objects.create(
                title=title,
                title_en=title_en,
                title_kk=title_kk,
                description=description or '',
                description_en=description_en,
                description_kk=description_kk,
                file=file,
                file_en=file_en if file_en else None,
                file_kk=file_kk if file_kk else None,
                category_id=category_id if category_id else None,
                uploaded_by=request.user
            )
            messages.success(request, 'Документ успешно создан!')
            try:
                from django.urls import reverse
                return redirect(f"{reverse('main:editor_dashboard')}?tab=documents")
            except Exception:
                return redirect('main:editor_dashboard')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
    
    categories = DocumentCategory.objects.all()
    context = {
        'editor': editor,
        'categories': categories,
    }
    return render(request, 'main/editor/create_document.html', context)


@login_required
def editor_feedback_view(request):
    """Страница обратной связи для редактора"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')
    
    # Получаем все обращения обратной связи (как в админке)
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # Обработка изменения статуса (как в админке)
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        new_status = request.POST.get('status')
        
        if feedback_id and new_status and new_status.strip():
            try:
                feedback = Feedback.objects.get(pk=feedback_id)
                # Проверяем, что статус валидный
                valid_statuses = ['new', 'in_progress', 'resolved', 'closed']
                if new_status in valid_statuses:
                    old_status = feedback.status
                    feedback.status = new_status
                    feedback.save()
                    messages.success(request, f'Статус обращения #{feedback_id} изменен на "{feedback.get_status_display()}"!')
                else:
                    messages.error(request, f'Неверный статус: {new_status}. Допустимые значения: {", ".join(valid_statuses)}')
            except Feedback.DoesNotExist:
                messages.error(request, f'Обращение с ID {feedback_id} не найдено!')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении статуса: {str(e)}')
        else:
            if not feedback_id:
                messages.error(request, 'ID обращения не указан!')
            elif not new_status:
                messages.error(request, 'Новый статус не указан!')
            else:
                messages.error(request, 'Неверные данные для обновления статуса!')
        
        return redirect('main:editor_feedback')
    
    context = {
        'editor': editor,
        'feedbacks': feedbacks,
    }
    return render(request, 'main/editor/feedback.html', context)


@login_required
def editor_edit_document_view(request, document_id):
    """Редактирование документа редактором"""
    try:
        editor = Editor.objects.get(user=request.user)
        if not editor.is_verified:
            messages.error(request, 'Ваш аккаунт редактора неактивен.')
            return redirect('main:editor_login')
    except Editor.DoesNotExist:
        messages.error(request, 'У вас нет прав редактора.')
        return redirect('main:editor_login')

    try:
        document = Document.objects.get(id=document_id, uploaded_by=request.user)
    except Document.DoesNotExist:
        messages.error(request, 'Документ не найден.')
        return redirect('main:editor_documents')

    if request.method == 'POST':
        title = request.POST.get('title')
        title_en = request.POST.get('title_en', '')
        title_kk = request.POST.get('title_kk', '')
        description = request.POST.get('description', '')
        description_en = request.POST.get('description_en', '')
        description_kk = request.POST.get('description_kk', '')
        category_id = request.POST.get('category')
        file = request.FILES.get('file')
        file_en = request.FILES.get('file_en')
        file_kk = request.FILES.get('file_kk')

        if title:
            document.title = title
            document.title_en = title_en
            document.title_kk = title_kk
            document.description = description
            document.description_en = description_en
            document.description_kk = description_kk
            document.category_id = category_id if category_id else None
            if file:
                document.file = file
            if file_en:
                document.file_en = file_en
            if file_kk:
                document.file_kk = file_kk
            document.save()
            messages.success(request, 'Документ успешно обновлен!')
            try:
                from django.urls import reverse
                return redirect(f"{reverse('main:editor_dashboard')}?tab=documents")
            except Exception:
                return redirect('main:editor_documents')
        else:
            messages.error(request, 'Пожалуйста, заполните обязательные поля.')

    categories = DocumentCategory.objects.all()
    context = {
        'editor': editor,
        'document': document,
        'categories': categories,
    }
    return render(request, 'main/editor/edit_document.html', context)
