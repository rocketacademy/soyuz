# Generated by Django 3.2.7 on 2022-01-06 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soyuz_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='max_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]