from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Получает элемент из словаря по ключу"""
    return dictionary.get(key)

@register.filter
def get_progress_percentage(current, total):
    """Вычисляет процент прогресса"""
    if total and total > 0:
        return min(100, (current / total) * 100)
    return 0

@register.filter
def format_time(seconds):
    """Форматирует время в MM:SS"""
    if not seconds:
        return "00:00"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

@register.filter
def get_status_badge(progress, lesson, user):
    """Возвращает статус прогресса в виде бейджа"""
    if lesson.is_completed_by_user(user):
        return '<span class="badge badge-primary"><i class="fas fa-star"></i> Завершен</span>'
    elif progress.is_ready_to_complete:
        return '<span class="badge badge-success"><i class="fas fa-check"></i> Готов к завершению</span>'
    else:
        return '<span class="badge badge-secondary"><i class="fas fa-clock"></i> В процессе</span>'

@register.filter
def get_video_progress_percentage(progress):
    """Возвращает процент прогресса видео"""
    if hasattr(progress, 'video_max_progress_percent'):
        return min(100, progress.video_max_progress_percent)
    return 0

@register.filter
def get_slides_progress_percentage(progress):
    """Возвращает процент прогресса слайдов"""
    if hasattr(progress, 'slides_current_slide') and hasattr(progress, 'slides_total_slides'):
        if progress.slides_total_slides and progress.slides_total_slides > 0:
            return min(100, (progress.slides_current_slide / progress.slides_total_slides) * 100)
    return 0
