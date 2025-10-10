import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "almau_adaptation.settings")

app = Celery("almau_adaptation")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
