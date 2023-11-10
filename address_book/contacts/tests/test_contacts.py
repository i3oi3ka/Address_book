from django.test import TestCase
from contacts.models import Contact
from django.urls import reverse
from rest_framework.test import APIClient


class TestContactFilters(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        Contact.objects.create(first_name="John", city="NY")
        Contact.objects.create(first_name="Jane", city="LA")

    def test_filter_by_first_name(self):
        url = reverse('contact-list')
        response = self.client.get(url, {'first_name': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "John")

    def test_filter_by_city(self):
        url = reverse('contact-list')
        response = self.client.get(url, {'city': 'NY'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['city'], "NY")