from django import template
from main.context_processors import get_translation

register = template.Library()

@register.simple_tag(takes_context=True)
def trans(context, text):
    """Кастомный тег для переводов (оставлен с именем trans для обратной совместимости)."""
    request = context['request']
    current_language = request.session.get('django_language', 'ru')
    return get_translation(text, current_language)

# Явные алиасы, чтобы избежать конфликта с django i18n trans
@register.simple_tag(takes_context=True, name='t')
def t_tag(context, text):
    request = context['request']
    current_language = request.session.get('django_language', 'ru')
    return get_translation(text, current_language)

@register.simple_tag(takes_context=True, name='tr')
def tr_tag(context, text):
    request = context['request']
    current_language = request.session.get('django_language', 'ru')
    return get_translation(text, current_language)