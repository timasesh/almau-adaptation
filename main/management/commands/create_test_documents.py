from django.core.management.base import BaseCommand
from main.models import DocumentCategory, Document
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import transaction
import datetime

class Command(BaseCommand):
    help = 'Создает тестовые категории и документы для демонстрации'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Получаем или создаем суперпользователя для загрузки
                admin_user, created = User.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@almau.edu.kz',
                        'is_staff': True,
                        'is_superuser': True
                    }
                )
                
                # Создаем категории в нужном порядке согласно скриншоту
                categories_data = [
                    {
                        'name': 'Уставы и регламенты',
                        'description': 'Основные документы университета: уставы, регламенты, положения',
                        'order_index': 1
                    },
                    {
                        'name': 'Политика безопасности',
                        'description': 'Документы по информационной безопасности и защите данных',
                        'order_index': 2
                    },
                    {
                        'name': 'Шаблоны заявлений',
                        'description': 'Готовые формы и шаблоны для различных заявлений',
                        'order_index': 3
                    },
                    {
                        'name': 'Финансовые документы',
                        'description': 'Финансовые отчеты, бюджеты и связанные документы',
                        'order_index': 4
                    },
                    {
                        'name': 'Инструкции и процедуры',
                        'description': 'Пошаговые инструкции и рабочие процедуры',
                        'order_index': 5
                    },
                    {
                        'name': 'Кадровые документы',
                        'description': 'Документы по управлению персоналом',
                        'order_index': 6
                    }
                ]
                
                categories = {}
                for cat_data in categories_data:
                    category, created = DocumentCategory.objects.update_or_create(
                        name=cat_data['name'],
                        defaults={
                            'description': cat_data['description'],
                            'order_index': cat_data['order_index']
                        }
                    )
                    categories[cat_data['name']] = category
                    if created:
                        self.stdout.write(f"Создана категория: {category.name}")
                    else:
                        self.stdout.write(f"Обновлена категория: {category.name} (порядок: {category.order_index})")
                
                # Создаем тестовые документы как на скриншоте
                test_documents = [
                    {
                        'title': 'Политика информационной безопасности',
                        'category': 'Политика безопасности',
                        'date': datetime.date(2024, 2, 8)
                    },
                    {
                        'title': 'Заявление на отпуск (шаблон)',
                        'category': 'Шаблоны заявлений',
                        'date': datetime.date(2024, 6, 15)
                    },
                    {
                        'title': 'Заявление на отпуск',
                        'category': 'Шаблоны заявлений',
                        'date': datetime.date(2024, 7, 1)
                    },
                    {
                        'title': 'Устав университета',
                        'category': 'Уставы и регламенты',
                        'date': datetime.date(2023, 3, 12)
                    },
                    {
                        'title': 'Инструкция по работе в системе Helpdesk',
                        'category': 'Инструкции и процедуры',
                        'date': datetime.date(2023, 3, 28)
                    },
                    {
                        'title': 'Кодекс корпоративной этики',
                        'category': 'Кадровые документы',
                        'date': datetime.date(2024, 1, 1)
                    },
                    {
                        'title': 'Бюджет университета на 2024 год',
                        'category': 'Финансовые документы',
                        'date': datetime.date(2024, 1, 15)
                    }
                ]
                
                for doc_data in test_documents:
                    # Проверяем, существует ли уже документ
                    if not Document.objects.filter(title=doc_data['title']).exists():
                        # Создаем пустой PDF-файл для демонстрации
                        fake_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
                        
                        doc = Document.objects.create(
                            title=doc_data['title'],
                            description=f"Описание документа: {doc_data['title']}",
                            category=categories[doc_data['category']],
                            uploaded_by=admin_user,
                            is_active=True
                        )
                        
                        # Создаем файл
                        filename = f"{doc.title.replace(' ', '_')}.pdf"
                        doc.file.save(filename, ContentFile(fake_pdf_content), save=True)
                        
                        # Устанавливаем дату создания
                        doc.created_at = datetime.datetime.combine(doc_data['date'], datetime.time())
                        doc.save()
                        
                        self.stdout.write(f"Создан документ: {doc.title}")
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nТестовые данные успешно созданы!\n'
                        f'Категорий: {len(categories)}\n'
                        f'Документов: {len(test_documents)}\n\n'
                        f'Перейдите на /documents/ для просмотра!'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании тестовых данных: {e}')
            ) 