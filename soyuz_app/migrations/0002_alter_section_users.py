# Generated by Django 3.2.7 on 2021-10-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soyuz_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='users',
            field=models.ManyToManyField(blank=True, to='soyuz_app.User'),
        ),
    ]