from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Instruction, Process

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
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь')
    }
    return render(request, 'main/dashboard.html', context)

@login_required
def processes_instructions_view(request):
    """Вкладка Процессы и Инструкции с современным дизайном"""
    # Получаем процессы и инструкции из базы (или тестовые данные если пусто)
    processes = list(Process.objects.filter(is_active=True).order_by('-created_at'))
    instructions = list(Instruction.objects.filter(is_active=True).order_by('-created_at'))
    
    # Получаем параметры поиска и фильтрации
    search_query = request.GET.get('search', '')
    current_tab = request.GET.get('tab', 'all')
    
    # Фильтруем процессы и инструкции по поисковому запросу
    filtered_processes = processes
    filtered_instructions = instructions
    
    if search_query:
        # Поиск без учета регистра для латиницы и кириллицы
        search_query = search_query.lower()
        filtered_processes = [p for p in processes if 
                            search_query in p.title.lower() or 
                            search_query in p.description.lower()]
        
        filtered_instructions = [i for i in instructions if 
                               search_query in i.title.lower() or 
                               search_query in i.description.lower()]
    
    if not processes:
        processes = [
            Process(title="Как пользоваться Career AlmaU?", description="Тестовый текст процесса."),
            Process(title="Как подать заявку на мероприятие в Документологе?", description="Тестовый текст процесса."),
            Process(title="Куда писать за помощью?", description="Тестовый текст процесса.")
        ]
    if not instructions:
        instructions = [
            Instruction(title="Как пользоваться Career AlmaU?", description="Тестовый текст инструкции."),
            Instruction(title="Как подать заявку на мероприятие в Документологе?", description="Тестовый текст инструкции."),
            Instruction(title="Куда писать за помощью?", description="Тестовый текст инструкции.")
        ]
    
    return render(request, 'main/processes_instructions.html', {
        'processes': processes,
        'instructions': instructions,
        'filtered_processes': filtered_processes,
        'filtered_instructions': filtered_instructions,
        'search_query': search_query,
        'current_tab': current_tab
    })

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
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь')
    }
    
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
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'user_name': teacher.full_name if teacher else (request.user.first_name or request.user.email.split('@')[0] if request.user.email else 'Пользователь')
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
    
    # Базовый queryset только активных документов
    documents = Document.objects.filter(is_active=True)
    
    # Применяем фильтр по категории сначала (для оптимизации)
    if category_filter:
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
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in doc.title.lower()
                desc_match = search_query in doc.description.lower()
                category_match = search_query in doc.category.name.lower()
                
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
    
    # Увеличиваем счетчик скачиваний
    document.increment_download_count()
    
    # Возвращаем файл для скачивания
    if document.file and os.path.exists(document.file.path):
        response = FileResponse(
            open(document.file.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(document.file.name)
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
    
    # Базовый queryset только активных документов
    documents = Document.objects.filter(is_active=True)
    
    # Применяем фильтр по категории сначала (для оптимизации)
    if category_filter:
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
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in doc.title.lower()
                desc_match = search_query in doc.description.lower()
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
        'current_category': category_filter
    })
    
    return JsonResponse({
        'success': True,
        'html': documents_html,
        'count': documents.count()
    })
def processes_instructions_view(request):
    """View для страницы процессов и инструкций"""
    from .models import Process, Instruction
    from django.db.models import Q

    search_query = request.GET.get('search', '')
    tab_filter = request.GET.get('tab', '')

    # Получаем активные процессы и инструкции
    processes = Process.objects.filter(is_active=True)
    instructions = Instruction.objects.filter(is_active=True)

    # Применяем фильтр по вкладке
    filtered_processes = processes
    filtered_instructions = instructions

    if tab_filter == 'processes':
        filtered_instructions = Instruction.objects.none()
    elif tab_filter == 'instructions':
        filtered_processes = Process.objects.none()

    # Применяем поиск (нечувствительный к регистру)
    # Используем Python поиск из-за проблем SQLite с кириллицей в icontains
    if search_query:
        search_query = search_query.strip().lower()
        if search_query:
            # Фильтруем процессы
            all_processes = list(filtered_processes)
            filtered_processes_ids = []
            
            for proc in all_processes:
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in proc.title.lower()
                desc_match = search_query in proc.description.lower()
                
                if title_match or desc_match:
                    filtered_processes_ids.append(proc.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_processes_ids:
                filtered_processes = filtered_processes.filter(id__in=filtered_processes_ids)
            else:
                filtered_processes = filtered_processes.none()
            
            # Фильтруем инструкции
            all_instructions = list(filtered_instructions)
            filtered_instructions_ids = []
            
            for instr in all_instructions:
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in instr.title.lower()
                desc_match = search_query in instr.description.lower()
                
                if title_match or desc_match:
                    filtered_instructions_ids.append(instr.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_instructions_ids:
                filtered_instructions = filtered_instructions.filter(id__in=filtered_instructions_ids)
            else:
                filtered_instructions = filtered_instructions.none()

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
        'filtered_processes': filtered_processes,
        'filtered_instructions': filtered_instructions,
        'search_query': search_query,
        'current_tab': tab_filter if tab_filter else 'all',
    }

    return render(request, 'main/processes_instructions.html', context)

def processes_instructions_api_search(request):
    """API для поиска процессов и инструкций без перезагрузки страницы"""
    from .models import Process, Instruction
    from django.template.loader import render_to_string
    
    search_query = request.GET.get('search', '')
    tab_filter = request.GET.get('tab', '')
    
    # Получаем активные процессы и инструкции
    processes = Process.objects.filter(is_active=True)
    instructions = Instruction.objects.filter(is_active=True)

    # Применяем фильтр по вкладке
    filtered_processes = processes
    filtered_instructions = instructions

    if tab_filter == 'processes':
        filtered_instructions = Instruction.objects.none()
    elif tab_filter == 'instructions':
        filtered_processes = Process.objects.none()

    # Применяем поиск (нечувствительный к регистру)
    # Используем Python поиск из-за проблем SQLite с кириллицей в icontains
    if search_query:
        search_query = search_query.strip().lower()
        if search_query:
            # Фильтруем процессы
            all_processes = list(filtered_processes)
            filtered_processes_ids = []
            
            for proc in all_processes:
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in proc.title.lower()
                desc_match = search_query in proc.description.lower()
                
                if title_match or desc_match:
                    filtered_processes_ids.append(proc.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_processes_ids:
                filtered_processes = filtered_processes.filter(id__in=filtered_processes_ids)
            else:
                filtered_processes = filtered_processes.none()
            
            # Фильтруем инструкции
            all_instructions = list(filtered_instructions)
            filtered_instructions_ids = []
            
            for instr in all_instructions:
                # Проверяем вхождение поискового запроса в разные поля
                title_match = search_query in instr.title.lower()
                desc_match = search_query in instr.description.lower()
                
                if title_match or desc_match:
                    filtered_instructions_ids.append(instr.id)
            
            # Фильтруем queryset по найденным ID
            if filtered_instructions_ids:
                filtered_instructions = filtered_instructions.filter(id__in=filtered_instructions_ids)
            else:
                filtered_instructions = filtered_instructions.none()
    
    # Рендерим только список процессов и инструкций
    processes_instructions_html = render_to_string('main/processes_instructions_list_partial.html', {
        'filtered_processes': filtered_processes,
        'filtered_instructions': filtered_instructions,
        'search_query': search_query,
        'current_tab': tab_filter if tab_filter else 'all'
    })
    
    return JsonResponse({
        'success': True,
        'html': processes_instructions_html,
        'count': filtered_processes.count() + filtered_instructions.count()
    })
