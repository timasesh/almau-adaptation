#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almau_adaptation.settings')
django.setup()

from main.models import LessonCategory

def create_categories():
    """Создает тестовые категории уроков"""
    
    categories_data = [
        {
            'name': 'Основы адаптации',
            'name_en': 'Adaptation Basics',
            'name_kk': 'Бейімделу негіздері',
            'description': 'Базовые уроки по адаптации к университетской жизни',
            'description_en': 'Basic lessons on adapting to university life',
            'description_kk': 'Университет өміріне бейімделу туралы негізгі сабақтар',
            'order_index': 1
        },
        {
            'name': 'Академические навыки',
            'name_en': 'Academic Skills',
            'name_kk': 'Академиялық дағдылар',
            'description': 'Уроки по развитию академических навыков',
            'description_en': 'Lessons on developing academic skills',
            'description_kk': 'Академиялық дағдыларды дамыту туралы сабақтар',
            'order_index': 2
        },
        {
            'name': 'Техническая поддержка',
            'name_en': 'Technical Support',
            'name_kk': 'Техникалық қолдау',
            'description': 'Уроки по работе с техническими системами',
            'description_en': 'Lessons on working with technical systems',
            'description_kk': 'Техникалық жүйелермен жұмыс туралы сабақтар',
            'order_index': 3
        },
        {
            'name': 'Карьерное развитие',
            'name_en': 'Career Development',
            'name_kk': 'Мансаптық даму',
            'description': 'Уроки по планированию карьеры',
            'description_en': 'Lessons on career planning',
            'description_kk': 'Мансапты жоспарлау туралы сабақтар',
            'order_index': 4
        }
    ]
    
    for data in categories_data:
        category, created = LessonCategory.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"Создана категория: {category.name}")
        else:
            print(f"Категория уже существует: {category.name}")

if __name__ == '__main__':
    create_categories()
    print("Готово!")

