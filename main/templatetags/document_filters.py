from django import template

register = template.Library()

@register.filter
def get_title(document, language='ru'):
    """Получить название документа на указанном языке"""
    return document.get_title(language)

@register.filter
def get_description(document, language='ru'):
    """Получить описание документа на указанном языке"""
    return document.get_description(language)

# Универсальные фильтры для процессов/инструкций/FAQ/категорий

@register.filter
def get_process_title(process, language='ru'):
    return getattr(process, 'get_title', lambda lang: process.title)(language)

@register.filter
def get_process_description(process, language='ru'):
    return getattr(process, 'get_description', lambda lang: process.description)(language)

@register.filter
def get_instruction_title(instruction, language='ru'):
    return getattr(instruction, 'get_title', lambda lang: instruction.title)(language)

@register.filter
def get_instruction_description(instruction, language='ru'):
    return getattr(instruction, 'get_description', lambda lang: instruction.description)(language)

@register.filter
def get_faq_question(faq, language='ru'):
    return getattr(faq, 'get_question', lambda lang: faq.question)(language)

@register.filter
def get_faq_answer(faq, language='ru'):
    return getattr(faq, 'get_answer', lambda lang: faq.answer)(language)

@register.filter
def get_category_name(category, language='ru'):
    return getattr(category, 'get_name', lambda lang: category.name)(language)

# Generic getters for about and contacts models
@register.filter
def get_text(obj, language='ru'):
    return getattr(obj, 'get_text', lambda lang: getattr(obj, 'text', ''))(language)