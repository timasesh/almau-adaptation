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
    # Поддержка как моделей, так и словарей (для старых представлений/фикстур)
    if isinstance(faq, dict):
        # Пробуем языковые ключи, затем общий
        if language == 'en' and faq.get('question_en'):
            return faq.get('question_en')
        if language == 'kk' and faq.get('question_kk'):
            return faq.get('question_kk')
        return faq.get('question', '')
    return getattr(faq, 'get_question', lambda lang: faq.question)(language)

@register.filter
def get_faq_answer(faq, language='ru'):
    if isinstance(faq, dict):
        if language == 'en' and faq.get('answer_en'):
            return faq.get('answer_en')
        if language == 'kk' and faq.get('answer_kk'):
            return faq.get('answer_kk')
        return faq.get('answer', '')
    return getattr(faq, 'get_answer', lambda lang: faq.answer)(language)

@register.filter
def get_category_name(category, language='ru'):
    if category is None:
        return ''
    if isinstance(category, dict):
        if language == 'en' and category.get('name_en'):
            return category.get('name_en')
        if language == 'kk' and category.get('name_kk'):
            return category.get('name_kk')
        return category.get('name', '')
    return getattr(category, 'get_name', lambda lang: category.name)(language)

# Generic getters for about and contacts models
@register.filter
def get_text(obj, language='ru'):
    return getattr(obj, 'get_text', lambda lang: getattr(obj, 'text', ''))(language)