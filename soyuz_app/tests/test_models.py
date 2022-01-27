import datetime
from django.test import TestCase

from django.contrib.auth import get_user_model
from ..models import Waiting_list, Batch, Course, Queue


class TestModels(TestCase):

    def setUp(self):
        self.student1 = get_user_model().objects.create(
            email='mickey@disney.com',
            hubspot_id='234',
            first_name='mickey',
            last_name='mouse',
        )

        self.student2 = get_user_model().objects.create(
            email='ironman@marvel.com',
            hubspot_id='567',
            first_name='tony',
            last_name='stark',
        )

        self.course1 = Course.objects.create(
            name='basics'
        )

        self.batch1 = Batch.objects.create(
            number=1,
            start_date=datetime.date.today() - datetime.timedelta(days=1),
            course=self.course1
        )

    def test_create_waiting_list(self):

        self.waiting_list1 = Waiting_list.objects.create(
            batch=self.batch1
        )
        self.assertEquals(self.waiting_list1.batch, self.batch1)

    def test_add_students_to_waiting_list(self):

        self.waiting_list1 = Waiting_list.objects.create(
            batch=self.batch1
        )

        self.waiting_list1.users.add(self.student1, through_defaults={'entry_date': datetime.date.today()})

        self.waiting_list1.users.add(self.student2, through_defaults={
                                     'entry_date': datetime.date.today() - datetime.timedelta(days=1)})

        waiting_list_users = get_user_model().objects.filter(
            waiting_list=self.waiting_list1,
            queue__entry_date=datetime.date.today()
        )

        self.assertEquals(waiting_list_users[0], self.student1)
        self.assertEquals(self.waiting_list1.users.count(), 2)
