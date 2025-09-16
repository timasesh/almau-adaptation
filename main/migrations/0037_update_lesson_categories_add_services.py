from django.db import migrations


def set_lesson_categories(apps, schema_editor):
    LessonCategory = apps.get_model('main', 'LessonCategory')

    desired = [
        {
            'name': 'Цифровая грамотность',
            'name_en': 'Digital Literacy',
            'name_kk': 'Цифрлық сауаттылық',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 1,
            'is_active': True,
        },
        {
            'name': 'Documentolog',
            'name_en': 'Documentolog',
            'name_kk': 'Documentolog',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 2,
            'is_active': True,
        },
        {
            'name': 'Platonus',
            'name_en': 'Platonus',
            'name_kk': 'Platonus',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 3,
            'is_active': True,
        },
        {
            'name': 'Сервисы',
            'name_en': 'Services',
            'name_kk': 'Қызметтер',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 4,
            'is_active': True,
        },
    ]

    names = {d['name'] for d in desired}

    for data in desired:
        LessonCategory.objects.update_or_create(
            name=data['name'],
            defaults=data,
        )

    # Ensure all desired are active and ordered correctly; keep other categories untouched


def reverse_set_lesson_categories(apps, schema_editor):
    # No-op reverse migration
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_remove_lesson_difficulty_level'),
    ]

    operations = [
        migrations.RunPython(set_lesson_categories, reverse_set_lesson_categories),
    ]


