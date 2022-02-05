from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import datetime
from ..models import Batch, Course, Queue, Waiting_list, Section
from django.contrib.auth import get_user_model
from ..views import waiting_list, web


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

        self.user4 = get_user_model().objects.create(
            email='richard@gotham.com',
            hubspot_id='689',
            first_name='dick',
            last_name='grayson',
        )

        self.user5 = get_user_model().objects.create(
            email='minnie@disney.com',
            hubspot_id='810',
            first_name='minnie',
            last_name='mouse',
        )

        self.user6 = get_user_model().objects.create(
            email='johntan@gmail.com',
            hubspot_id='852',
            first_name='john',
            last_name='tan',
        )

        self.batch1 = Batch.objects.create(
            number=1,
            start_date=datetime.date.today() + datetime.timedelta(days=3),
            course=self.course1,
            max_capacity=2,
        )

        self.batch2 = Batch.objects.create(
            number=2,
            start_date=datetime.date.today() + datetime.timedelta(days=3),
            course=self.course1,
            max_capacity=20,
        )

        self.batch3 = Batch.objects.create(
            number=3,
            start_date=datetime.date.today() - datetime.timedelta(days=3),
            course=self.course1,
            max_capacity=0
        )

        self.waiting_list1 = Waiting_list.objects.create(
            batch=self.batch1
        )

        self.section1 = Section.objects.create(
            number=1,
            batch=self.batch1
        )

        self.section2 = Section.objects.create(
            number=2,
            batch=self.batch1
        )

        self.batch1.users.add(self.user4)
        self.batch1.users.add(self.user5)
        self.batch1.users.add(self.user6)

        self.section1.users.add(self.user4)
        self.section1.users.add(self.user5)
        self.section2.users.add(self.user6)

        self.waiting_list1.users.add(self.user2, through_defaults={'entry_date': datetime.date.today()})

        self.waiting_list1.users.add(self.user3,
                                     through_defaults={'entry_date': datetime.date.today() - datetime.timedelta(days=1)})

        self.client = Client()

    def test_waiting_list_GET(self):
        get_waiting_list_url = reverse('soyuz_app:get_waiting_list', args=[self.batch1.id])
        request = self.factory.get(get_waiting_list_url)
        request.user = self.user1
        response = waiting_list.get_waiting_list(request, self.batch1.id)
        waiting_list_students = list(self.waiting_list1.users.all().order_by('queue__entry_date'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(waiting_list_students[0], self.user3)
        self.assertEquals(self.waiting_list1.users.count(), 2)

    def test_delete_from_waiting_list_POST(self):
        delete_from_waiting_list_url = reverse('soyuz_app:delete_from_waiting_list')
        request = self.factory.post(delete_from_waiting_list_url, {
            'batch_id': self.batch1.id,
            'student_id': self.user2.id
        })

        request.user = self.user1
        response = waiting_list.delete_from_waiting_list(request)
        waiting_list_students = list(self.waiting_list1.users.all())

        self.assertEquals(response.status_code, 302)
        self.assertEquals(waiting_list_students[0], self.user3)
        self.assertEquals(self.waiting_list1.users.count(), 1)

    def test_signup_max_capacity_GET(self):
        response = self.client.get(reverse('soyuz_app:signup', args=[self.batch1.id, 'minnie@disney.com']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/max-capacity.html')

    def test_signup_max_capacity_POST_add_to_waiting_list(self):
        response = self.client.post(reverse('soyuz_app:signup', args=[self.batch1.id, 'clint@marvel.com']), data={
            "email": "clint@marvel.com",
            "first_name": "Clint",
            "last_name": "Barton",
            "password1": "qwerty1234",
            "password2": "qwerty1234"
        })

        self.assertEquals(self.waiting_list1.users.all().count(), 3)
        self.assertTemplateUsed(response, 'users/waiting-list-confirmation.html')

    def test_signup_max_capacity_POST_create_waiting_list(self):
        response = self.client.post(reverse('soyuz_app:signup', args=[self.batch3.id, 'nat@marvel.com']), data={
            "email": "nat@marvel.com",
            "first_name": "Natasha",
            "last_name": "Romanoff",
            "password1": "qwerty1234",
            "password2": "qwerty1234"
        })

        self.assertEquals(Waiting_list.objects.all().count(), 2)
        self.assertTemplateUsed(response, 'users/waiting-list-confirmation.html')

    def test_signup_registration_GET(self):
        response = self.client.get(reverse('soyuz_app:signup', args=[self.batch2.id, 'goofy@disney.com']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_registration_POST(self):
        response = self.client.post(reverse('soyuz_app:signup', args=[self.batch2.id, 'pepper@marvel.com']), data={
            "email": "pepper@marvel.com",
            "first_name": "Pepper",
            "last_name": "Potts",
            "password1": "qwerty1234",
            "password2": "qwerty1234"
        })

        batch_2_users = list(self.batch2.users.all())

        self.assertEquals(self.batch2.users.all().count(), 1)
        self.assertEquals(batch_2_users[0].email, 'pepper@marvel.com')
        self.assertEquals(response.status_code, 302)

    def test_signup_reg_link_expired_GET(self):
        response = self.client.get(reverse('soyuz_app:signup', args=[self.batch3.id, 'elsa@disney.com']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration-expired.html')

    def test_change_batch_capacity_POST_waiting_list_bigger_or_equals_change(self):
        request = self.factory.post(reverse('soyuz_app:change_batch_capacity'), {
            "new_batch_capacity": '4',
            "batch_id": self.batch1.id
        })

        request.user = self.user1
        response = web.change_batch_capacity(request)

        batch = Batch.objects.get(id=self.batch1.id)
        section1 = Section.objects.get(id=self.section1.id)
        section2 = Section.objects.get(id=self.section2.id)

        waiting_list = batch.waiting_list
        self.assertEquals(response.status_code, 302)
        self.assertEquals(batch.max_capacity, 4)
        self.assertEquals(waiting_list.users.all().count(), 1)
        self.assertEquals(section2.users.all().count(), 2)
        self.assertEquals(section1.users.all().count(), 2)

    def test_change_batch_capacity_POST_waiting_list_smaller_than_change(self):
        request = self.factory.post(reverse('soyuz_app:change_batch_capacity'), {
            "new_batch_capacity": '6',
            "batch_id": self.batch1.id
        })

        request.user = self.user1
        response = web.change_batch_capacity(request)

        batch1 = Batch.objects.get(number=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(batch1.max_capacity, 6)
        self.assertEquals(self.batch1.users.all().count(), 5)
