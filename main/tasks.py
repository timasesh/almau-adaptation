from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task
def sync_ad_positions_task():
    """Фоновая задача синхронизации должностей"""
    logger.info("Запуск фоновой синхронизации AD/Entra ID")
    call_command("sync_ad_positions")
    logger.info("Синхронизация завершена")
