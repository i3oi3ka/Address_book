import psycopg2
from django.test import TestCase
from django.db.utils import IntegrityError

from contacts.models import Contact, ContactActivityLog, ContactGroup
from django.urls import reverse
from rest_framework.test import APIClient
import pytest
import unittest
from unittest.mock import patch

from contacts.serializers import ContactSerializer, ContactGroupSerializer


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


# Фікстура для створення контакту
@pytest.fixture
def contact():
    return Contact.objects.create(
        first_name="John",
        last_name="Doe",
        country="USA",
        city="NY",
        street="Main street",
        url="https://example.com",
        phone="+1234567890",
        image=None  # можна додати зображення, якщо потрібно
    )


# Створіть новий контакт.
# Використайте mock для мокання методу видалення.
# Перевірте, чи об'єкт не був дійсно видалений з бази даних.
@pytest.mark.django_db
def test_contact_delete_mocker(mocker, contact):
    mock_contact_delete = mocker.patch.object(
        Contact,
        'delete',
        return_value="delete mocker")

    result = contact.delete()
    mock_contact_delete.assert_called()
    assert contact.first_name == "John"
    assert result == "delete mocker"
    mock_contact_delete.assert_called_once()


# Напишіть тест, який перевіряє чи створюється запис в ContactActivityLog при створені нового контакту.
# Код проекту: https://github.com/vladysllav/adress_book
@pytest.mark.django_db
def test_contact_activity_log(contact):
    contact_activity = ContactActivityLog.objects.get(contact=contact.id)
    assert contact_activity.activity_type == "CREATED"


@pytest.fixture
def contact_edit(contact):
    contact.first_name = "Vlad"
    contact.save()
    return contact


# Напишіть тест, який при зміні даних контакту перевіряє, чи було зафіксовано зміни в ContactActivityLog.
@pytest.mark.django_db
def test_contact_activity_log_change(contact_edit):
    contact_activity = ContactActivityLog.objects.filter(contact=contact_edit.id)
    assert contact_activity[1].activity_type == "EDITED"


# Використайте pytest-mock, щоб "замокати" метод збереження контакту так, щоб реальне збереження не відбувалося.
@pytest.mark.django_db
def test_contact_save_with_mocker(mocker, contact):
    mock_contact_save = mocker.patch.object(
        Contact,
        'save',
        return_value="save was mocked")
    contact.first_name = "Vlad"
    result = contact.save()
    mock_contact_save.assert_called()
    assert contact.first_name == "Vlad"
    assert result == "save was mocked"
    mock_contact_save.assert_called_once()
    contact = Contact.objects.get(id=contact.id)
    assert contact.first_name == "John"


# Замокайте створення ContactActivityLog (виклику метода create), внесіть зміни до існуючого контакту.
# Перевірте, чи зміни коректно зберіглися.
# Перевірте, чи ContactActivityLog.objects.create був викликаний з відповідними аргументами.
@pytest.mark.django_db
def test_contact_change_with_mocker(mocker, contact):
    mock_activity_log = mocker.patch.object(
        ContactActivityLog.objects,
        'create',
        return_value={
            "contact": contact.id,
            "activity_type": "Edited",
            "details": f"Contact {contact.first_name} {contact.last_name} was edited."})
    contact.first_name = "Vlad"
    contact.save()
    mock_activity_log.assert_called()
    assert contact.first_name == "Vlad"
    mock_activity_log.assert_called_once_with(contact=contact,
                                              activity_type='EDITED',
                                              details='Contact Vlad Doe was updated. Changes: first_name: John -> Vlad')


# Тест на перевірку серіалізації
@pytest.mark.django_db
def test_contact_serializer(contact):
    serialized = ContactSerializer(contact)
    assert serialized.data["first_name"] == "John"
    assert serialized.data["last_name"] == "Doe"
    assert serialized.data["country"] == "USA"
    assert serialized.data["city"] == "NY"
    assert serialized.data["street"] == "Main street"
    assert serialized.data["url"] == "https://example.com"
    assert serialized.data["phone"] == "+1234567890"
    assert serialized.data["image"] is None  # якщо у вас є зображення, перевірте його URL тут


@pytest.mark.django_db
def test_create_double_contact():
    with pytest.raises(IntegrityError):
        Contact.objects.create(first_name="John", last_name="Snow")
        # Try to create another Contact with the same first_name "John"
        Contact.objects.create(first_name="John", last_name="Snow")


# 6. Тест створення групи контактів
# Створіть нову групу та додайте до неї контакти.
# Перевірте, чи контакти коректно додані до групи.
class TestContactGroup(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        Contact.objects.create(first_name="John", city="NY")
        Contact.objects.create(first_name="Jane", city="LA")
        Contact.objects.create(first_name="Vlad", city="Texas")
        group = ContactGroup.objects.create(name="friends")
        contacts = Contact.objects.all()
        for contact in contacts:
            group.contacts.add(contact)

    def test_contact_duble(self):
        Contact.objects.create(first_name="John", last_name="Sn")
        # Try to create another Contact with the same first_name "John"
        with self.assertRaises(IntegrityError):
            Contact.objects.create(first_name="John", last_name="Sn")

    def test_group_create(self):
        url = reverse('contact_group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['contacts'][0]['first_name'], "John")
        self.assertEqual(response.data[0]['contacts'][1]['city'], "LA")
        self.assertEqual(response.data[0]['contacts'][2]['first_name'], "Vlad")
        self.assertEqual(response.data[0]['name'], "friends")

    @pytest.mark.django_db
    def test_contact_group_serializer(self):
        contact_group = ContactGroup.objects.get(name="friends")
        serialized = ContactGroupSerializer(contact_group)
        assert serialized.data["name"] == "friends"
        assert serialized.data["contacts"][0]["first_name"] == "John"
        assert serialized.data["contacts"][2]["city"] == "Texas"
