from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import datetime
from ..models import Batch, Course, Queue, Waiting_list
from django.contrib.auth import get_user_model
from ..views import waiting_list


class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.course1 = Course.objects.create(
            name='basics'
        )
        self.user1 = get_user_model().objects.create(
            email='ironman@marvel.com',
            hubspot_id='567',
            first_name='tony',
            last_name='stark',
            is_staff=True
        )

        self.user2 = get_user_model().objects.create(
            email='mickey@disney.com',
            hubspot_id='234',
            first_name='mickey',
            last_name='mouse',
        )

        self.user3 = get_user_model().objects.create(
            email='batman@gotham.com',
            hubspot_id='321',
            first_name='bruce',
            last_name='wayne',
        )

        self.batch1 = Batch.objects.create(
            number=1,
            start_date=datetime.date.today() - datetime.timedelta(days=1),
            course=self.course1
        )

        self.waiting_list1 = Waiting_list.objects.create(
            batch=self.batch1
        )

        self.waiting_list1.users.add(self.user2, through_defaults={'entry_date': datetime.date.today()})

        self.waiting_list1.users.add(self.user3,
                                     through_defaults={'entry_date': datetime.date.today() - datetime.timedelta(days=1)})

        self.waiting_list_url = reverse('soyuz_app:get_waiting_list', args=[self.batch1.id])

    def test_waiting_list_GET(self):
        request = self.factory.get(self.waiting_list_url)
        request.user = self.user1
        response = waiting_list.get_waiting_list(request, self.batch1.id)

        self.assertEquals(response.status_code, 200)

    def test_waiting_list_students(self):
        waiting_list_student = get_user_model().objects.filter(
            waiting_list=self.waiting_list1, queue__entry_date=datetime.date.today())

        self.assertEquals(waiting_list_student[0], self.user2)
        self.assertEquals(waiting_list_student.count(), 1)
