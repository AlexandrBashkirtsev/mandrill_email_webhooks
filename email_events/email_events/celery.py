'''Celery settings'''
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "email_events.settings")
app = Celery("email_events")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()