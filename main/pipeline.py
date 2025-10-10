import logging

logger = logging.getLogger(__name__)


def sync_position_from_ad(strategy, details, response, user=None, *args, **kwargs):
    job_title = response.get("jobTitle") or details.get("job_title")

    # ⚡ Добавим лог, чтобы видеть, что возвращает Microsoft
    logger.warning(f"[SSO DEBUG] job_title from AD: {job_title}")
    logger.warning(f"[SSO DEBUG] response keys: {list(response.keys())}")

    if job_title:
        from .models import Position
        position, _ = Position.objects.get_or_create(name=job_title)
        if hasattr(user, "profile"):
            user.profile.position = position
            user.profile.save()
