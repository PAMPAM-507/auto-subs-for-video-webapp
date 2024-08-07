import os

from celery import Celery, schedules
from celery.schedules import schedule
from celery.schedules import crontab
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_subs.settings')

app = Celery('auto_subs')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'authForModel': {
#         'task': 'ClinicWebsite.tasks.register_to_model',
#         # 'schedule': crontab(minute='*/5'),
#         'schedule': timedelta(seconds=290),
#     },
# }
