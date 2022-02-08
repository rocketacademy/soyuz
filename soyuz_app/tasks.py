from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Batch, Waiting_list
from .emails.basics_rejection import send_rejection_email
import datetime


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_basics_rejection_email():
    today = datetime.date.today()

    try:
        batch = Batch.objects.get(start_date=today, course__name='basics')
    except Batch.DoesNotExist:
        pass
    else:

        try:
            waiting_list = batch.waiting_list
        except Waiting_list.DoesNotExist:
            pass
        else:
            waiting_list_students = waiting_list.users.all()

            for student in waiting_list_students:
                send_rejection_email(student, batch)
