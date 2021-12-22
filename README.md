# Soyuz

Rocket Academy Backend Student System

https://soyuz-ra-staging.herokuapp.com/

![](https://news.in-24.com/content/uploads/2021/05/19/84e035c899.jpg)

[Soyuz](<https://en.wikipedia.org/wiki/Soyuz_(rocket_family)>) means "union" in Russian. Soyuz is a rocket that, according to wikipedia, has "_over 1,900 flights since its debut in 1966, [and is] the most frequently used launch vehicle in the world as of 2021._"

Soyuz is the backend system that coordinates all student and course activities and is the source of truth for data to run Rocket Academy courses.

# Links

https://soyuz-ra.herokuapp.com/
https://soyuz-ra.herokuapp.com/batch/2/hubspot_id/10/email/kai@yahoo.com/first_name/kai/last_name/wow

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

## SASS Reference

https://github.com/jrief/django-sass-processor

#### Manage SASS files locally

```
python manage.py compilescss # run sass
python manage.py collectstatic --clear # delete static file cache
python manage.py compilescss --delete-files # get rid of files
```

### Static Files

https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/
https://docs.djangoproject.com/en/3.2/howto/static-files/

## Email

`DJANGO_DEFAULT_FROM_EMAIL` is set to: hello@rocketacademy.co

## Local Dev Setup

Install EditorConfig for VS Code: https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig

#### pipenv

https://pipenv-fork.readthedocs.io/en/latest/basics.html

Instructions from this guide:
https://jayden-chua.medium.com/virtual-environments-pip-and-pipenv-on-macos-8f3178b13b75

Install pipenv:

```
python3 -m pip install --user pipenv
```

Print out the pip path:

```
python3 -m site --user-base # /Users/jayden/Library/Python/3.7/bin/
```

Make sure pipenv is in your path:

```
echo 'export PATH=/Users/jayden/Library/Python/3.7/bin:$PATH' >> ~/.profile
```

#### install the soyuz dependencies

```
pipenv install
```

#### soyuz django commands

```
dropdb soyuz_db
create_db soyuz_db
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py makemigrations soyuz_app
python manage.py migrate soyuz_app
python manage.py loaddata soyuz_app/fixtures/seed.json
```

#### show all routes

```
python manage.py show_urls
```

# Setting Local Dev Env Vars

```
echo 'export DJANGO_READ_DOT_ENV_FILE=True' >> ~/.profile
echo 'export DJANGO_ENV=development' >> ~/.profile
```

Setup the Git precommit hooks: https://pre-commit.com/

```
pre-commit install
```

#### Skip Pre Commit

git commit --no-verify
git push --no-verify

## Dev Email Setup

Install Mail Hog: https://github.com/mailhog/MailHog

Mailhog gives a nice web page local interface to email generated by the app.

Mac

```
brew update && brew install mailhog
```

Run it:

```
/usr/local/opt/mailhog/bin/MailHog
```

Go to the local server: http://localhost:8025

# Heroku Setup

```bash
heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py makemigrations soyuz_app
heroku run python manage.py migrate soyuz_app
heroku run python manage.py loaddata soyuz_app/fixtures/seed.json
heroku run python manage.py collectstatic
```

From: https://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html?highlight=heroku

```
heroku create --buildpack heroku/python

heroku buildpacks:add --index 2 https://github.com/drpancake/heroku-buildpack-django-sass.git --remote staging

heroku addons:create heroku-postgresql:hobby-dev

# On Windows use double quotes for the time zone, e.g.
# heroku pg:backups schedule --at "02:00 America/Los_Angeles" DATABASE_URL

heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL  --remote staging

heroku pg:promote DATABASE_URL

heroku addons:create heroku-redis:hobby-dev --remote staging

heroku config:set PYTHONHASHSEED=random --remote staging

heroku config:set WEB_CONCURRENCY=4 --remote staging

heroku config:set DJANGO_DEBUG=False  --remote staging

heroku config:set DJANGO_SETTINGS_MODULE=soyuz_app.settings.production  --remote staging

heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)" --remote staging

# need this to turn off debug scripts
heroku config:set DJANGO_ENV="production" --remote staging

# Generating a 32 character-long random string without any of the visually similar characters "IOl01":
heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"  --remote staging


# Set this to your Heroku app url, e.g. 'bionic-beaver-28392.herokuapp.com'
heroku config:set DJANGO_ALLOWED_HOSTS='soyuz-ra-staging.herokuapp.com rocketacademy.co' --remote staging

git push heroku master

heroku run python manage.py createsuperuser

heroku run python manage.py check --deploy

heroku open
```

#### setting postgres backups on Heroku

```
heroku pg:backups:schedule DATABASE_URL --at '02:00 Asia/Singapore' --remote staging
```

# View Testing Code

```
import json
from django.http import HttpResponse
from django.core import serializers

def test(request):
    batch = Batch.objects.get(number=1)
    json_obj = json.dumps(batch, indent=4, sort_keys=True, default=str)

    return HttpResponse(json_obj)
```

# Django Relationships

#### "backwards" relationships

https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects

# Slack API

#### Slack Web API

https://api.slack.com/web

#### Slack Events API

https://api.slack.com/apis/connections/events-api
