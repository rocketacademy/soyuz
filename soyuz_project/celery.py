import os

import environ
from celery import Celery

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soyuz_project.settings")

app = Celery("soyuz_project")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    CELERY_BROKER_URL=env("REDISCLOUD_URL"), CELERY_RESULT_BACKEND=env("REDISCLOUD_URL")
)

# example to have celery run a task at set intervals
# app.conf.update(CELERY_BEAT_SCHEDULE={
#  'do-stuff-at-interval': {
#        'task': 'soyuz_project.celery.debug_task',
#         # seconds
#        'schedule': 3.0,
#     },
# })

# Load task modules from all registered Django apps.
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@app.task(bind=True)
def debug_task(self):
    print(f"FRequest: {self.request!r}")


@app.task(bind=True)
def hello(self):
    print(f"FRequest: {self.request!r}")
