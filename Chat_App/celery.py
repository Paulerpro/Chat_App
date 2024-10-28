import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Chat_App.settings")

celery_app = Celery("Chat_App.settings")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()