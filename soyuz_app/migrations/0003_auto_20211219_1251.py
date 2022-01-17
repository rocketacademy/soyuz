# Generated by Django 3.2.7 on 2021-12-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soyuz_app', '0002_batch_max_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='slack_channel_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='slack_channel_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='slack_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
