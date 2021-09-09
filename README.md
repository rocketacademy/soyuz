# Soyuz
Rocket Academy Backend Student System

![](https://news.in-24.com/content/uploads/2021/05/19/84e035c899.jpg)

[Soyuz](https://en.wikipedia.org/wiki/Soyuz_(spacecraft)) means "union" in Russian.

This is the backend system that coordinates all student and course activities and is the source of truth for data to run Rocket Academy courses.

# Links
https://soyuz-ra.herokuapp.com/
https://soyuz-ra.herokuapp.com/api/batches/

# Technical Specs

Soyuz is a Django app with a Postgres DB.

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
