from __future__ import absolute_import, unicode_literals
import os
import environ
from celery import Celery
from celery.schedules import crontab

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env("DJANGO_SETTINGS_MODULE"))

app = Celery('soyuz_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    CELERY_BROKER_URL=env("REDIS_URL"),
    CELERY_RESULT_BACKEND=env("REDIS_URL"),
    CELERY_BEAT_SCHEDULE={
        'send-rejection-email': {
            'task': 'soyuz_app.tasks.send_basics_rejection_email',
            'schedule': crontab(hour='8'),
        },
    })

app.autodiscover_tasks()
