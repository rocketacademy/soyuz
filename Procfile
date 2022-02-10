web: gunicorn soyuz_project.wsgi --log-file -
release: python manage.py migrate
worker: celery --app soyuz_project worker -l INFO
