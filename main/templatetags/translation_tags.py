from django import template
from main.context_processors import get_translation

register = template.Library()

@register.simple_tag(takes_context=True)
def trans(context, text):
    """Кастомный тег для переводов"""
    request = context['request']
    current_language = request.session.get('django_language', 'ru')
    return get_translation(text, current_language)