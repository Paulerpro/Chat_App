from .celery import celery_app

# ensures the celery_app below is import once django kick-offs
__all__ = ("celery_app")