from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import web, user, slack


class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved1(self):
        url = reverse('soyuz_app:get_batches')
        self.assertEquals(resolve(url).func, web.get_batches)

    def test_list_url_is_resolved2(self):
        url = reverse('soyuz_app:get_sections', kwargs={'course_name': 'course_name', 'batch_number': 'batch_number'})
        self.assertEquals(resolve(url).func, web.get_sections)

    def test_list_url_is_resolved3(self):
        url = reverse('soyuz_app:switch_sections')
        self.assertEquals(resolve(url).func, web.switch_sections)

    def test_list_url_is_resolved5(self):
        url = reverse('soyuz_app:delete_from_batch')
        self.assertEquals(resolve(url).func, web.delete_from_batch)

    def test_list_url_is_resolved6(self):
        url = reverse('soyuz_app:add_to_batch')
        self.assertEquals(resolve(url).func, web.add_to_batch)

    def test_list_url_is_resolved7(self):
        url = reverse('soyuz_app:add_to_section')
        self.assertEquals(resolve(url).func, web.add_to_section)

    def test_list_url_is_resolved8(self):
        url = reverse('soyuz_app:get_student_list')
        self.assertEquals(resolve(url).func, web.get_student_list)

    def test_list_url_is_resolved9(self):
        url = reverse('soyuz_app:reassign_sections')
        self.assertEquals(resolve(url).func, web.reassign_sections)

    def test_list_url_is_resolved10(self):
        url = reverse('soyuz_app:check_slack_registration')
        self.assertEquals(resolve(url).func, web.check_slack_registration)

    def test_list_url_is_resolved11(self):
        url = reverse('soyuz_app:create_batch_channel')
        self.assertEquals(resolve(url).func, web.create_batch_channel)

    def test_list_url_is_resolved12(self):
        url = reverse('soyuz_app:assign_sections')
        self.assertEquals(resolve(url).func, web.assign_sections)

    def test_list_url_is_resolved13(self):
        url = reverse('soyuz_app:create_channels')
        self.assertEquals(resolve(url).func, web.add_to_batch)

    def test_list_url_is_resolved14(self):
        url = reverse('soyuz_app:event_hook')
        self.assertEquals(resolve(url).func, slack.event_hook)

    def test_list_url_is_resolved15(self):
        url = reverse('soyuz_app:change_batch_capacity')
        self.assertEquals(resolve(url).func, web.change_batch_capacity)

    def test_list_url_is_resolved16(self):
        url = reverse('soyuz_app:create_section_channel')
        self.assertEquals(resolve(url).func, web.create_section_channel)

    def test_list_url_is_resolved17(self):
        url = reverse('soyuz_app:sectionless_assign')
        self.assertEquals(resolve(url).func, web.sectionless_assign)
