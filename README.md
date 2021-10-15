# Soyuz
Rocket Academy Backend Student System

https://soyuz-ra-staging.herokuapp.com/

![](https://news.in-24.com/content/uploads/2021/05/19/84e035c899.jpg)

[Soyuz](https://en.wikipedia.org/wiki/Soyuz_(spacecraft)) means "union" in Russian.

This is the backend system that coordinates all student and course activities and is the source of truth for data to run Rocket Academy courses.

# Links
https://soyuz-ra.herokuapp.com/
https://soyuz-ra.herokuapp.com/api/batches/

# Technical Specs

#### Backend
Soyuz is a Django app with Django Rest Framework and a Postgres DB.

#### Front-end
CSS is built using SASS with Bootstrap.

## Django Rest Framework Reference
https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react

Auth: https://www.django-rest-framework.org/api-guide/authentication/

## Heroku Settings Reference
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment

### Heroku PG Reference

https://help.heroku.com/GDQ74SU2/django-migrations

```bash
heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py makemigrations soyuz_app
heroku run python manage.py migrate soyuz_app
heroku run python manage.py loaddata soyuz_app/seed.json
```
## SASS Reference
https://www.accordbox.com/blog/how-use-scss-sass-your-django-project-python-way/

### Static Files
https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/
https://docs.djangoproject.com/en/3.2/howto/static-files/

# Local Dev Setup

Install EditorConfig for VS Code: https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig

```
dropdb soyuz_db
create_db soyuz_db
pip install -r requirements/local.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py makemigrations soyuz_app
python manage.py migrate soyuz_app
python manage.py loaddata soyuz_app/seed.json
```

Setup the Git precommit hooks:
```
pre-commit install
```

#### Skip Pre Commit
git commit --no-verify
git push --no-verify

# Heroku Setup
From: https://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html?highlight=heroku
```
heroku create --buildpack heroku/python

heroku addons:create heroku-postgresql:hobby-dev

# On Windows use double quotes for the time zone, e.g.
# heroku pg:backups schedule --at "02:00 America/Los_Angeles" DATABASE_URL

heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL  --remote staging

heroku pg:promote DATABASE_URL

heroku addons:create heroku-redis:hobby-dev --remote staging

heroku addons:create mailgun:starter --remote staging


heroku config:set PYTHONHASHSEED=random --remote staging


heroku config:set WEB_CONCURRENCY=4 --remote staging


heroku config:set DJANGO_DEBUG=False  --remote staging

heroku config:set DJANGO_SETTINGS_MODULE=soyuz_app.settings.production  --remote staging

heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)" --remote staging


# Generating a 32 character-long random string without any of the visually similar characters "IOl01":
heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"  --remote staging


# Set this to your Heroku app url, e.g. 'bionic-beaver-28392.herokuapp.com'
heroku config:set DJANGO_ALLOWED_HOSTS='soyuz-ra-staging.herokuapp.com rocketacademy.co' --remote staging

# Assign with AWS_ACCESS_KEY_ID
heroku config:set DJANGO_AWS_ACCESS_KEY_ID=

# Assign with AWS_SECRET_ACCESS_KEY
heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=

# Assign with AWS_STORAGE_BUCKET_NAME
heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=

git push heroku master

heroku run python manage.py createsuperuser

heroku run python manage.py check --deploy

heroku open
```
