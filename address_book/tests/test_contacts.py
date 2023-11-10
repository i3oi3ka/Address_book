import pytest

from contacts.models import Contact
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def contact_factory():
    def factory(**data):
        return Contact.objects.create(**data)

    return factory


@pytest.mark.django_db  # ств нова база даних для тестів і видалиться після тестів
def test_filter_by_first_name(api_client, contact_factory):
    contact1 = contact_factory(first_name='Vlad', city='Kharkiv')
    contact2 = contact_factory(first_name='Vova', city='Lviv')

    response = api_client.get(reverse("contact-list"), {'first_name': 'Vlad'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['first_name'] == contact1.first_name


@pytest.mark.django_db  # ств нова база даних для тестів і видалиться після тестів
def test_filter_by_city(api_client, contact_factory):
    contact1 = contact_factory(first_name='Vlad', city='Kharkiv')
    contact2 = contact_factory(first_name='Vova', city='Lviv')

    response = api_client.get(reverse("contact-list"), {'city': 'Lviv'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['first_name'] == contact2.first_name
