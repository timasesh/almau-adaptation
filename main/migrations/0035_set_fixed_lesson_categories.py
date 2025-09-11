from django.db import migrations


def set_fixed_lesson_categories(apps, schema_editor):
    LessonCategory = apps.get_model('main', 'LessonCategory')

    desired = [
        {
            'name': 'Documentolog',
            'name_en': 'Documentolog',
            'name_kk': 'Documentolog',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 1,
            'is_active': True,
        },
        {
            'name': 'Platonus',
            'name_en': 'Platonus',
            'name_kk': 'Platonus',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 2,
            'is_active': True,
        },
        {
            'name': 'Цифровая грамотность',
            'name_en': 'Digital Literacy',
            'name_kk': 'Цифрлық сауаттылық',
            'description': '',
            'description_en': '',
            'description_kk': '',
            'order_index': 3,
            'is_active': True,
        },
    ]

    names = {d['name'] for d in desired}

    # Create or update the desired categories
    for data in desired:
        obj, _created = LessonCategory.objects.update_or_create(
            name=data['name'],
            defaults=data,
        )

    # Deactivate any other categories
    LessonCategory.objects.exclude(name__in=names).update(is_active=False)


def reverse_set_fixed_lesson_categories(apps, schema_editor):
    # No destructive reverse; leave categories as-is
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_update_feedback_type_choices'),
    ]

    operations = [
        migrations.RunPython(set_fixed_lesson_categories, reverse_set_fixed_lesson_categories),
    ]


