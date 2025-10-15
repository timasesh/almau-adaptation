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

@register.filter
def get_instruction_title(instruction, lang='ru'):
    """Возвращает название инструкции на нужном языке с fallback"""
    lang = (lang or 'ru').split('-')[0]
    if lang == 'en' and instruction.title_en:
        return instruction.title_en
    elif lang == 'kk' and instruction.title_kk:
        return instruction.title_kk
    return instruction.title  # fallback

@register.filter
def get_instruction_description(instruction, lang='ru'):
    """Возвращает описание инструкции на нужном языке с fallback"""
    lang = (lang or 'ru').split('-')[0]
    if lang == 'en' and instruction.description_en:
        return instruction.description_en
    elif lang == 'kk' and instruction.description_kk:
        return instruction.description_kk