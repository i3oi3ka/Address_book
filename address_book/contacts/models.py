from django.db import models


# class CustomUser(AbstractUser):
#     date_of_birth = models.DateField(null=True, blank=True)

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    url = models.URLField(max_length=200, )
    phone = models.CharField(max_length=30)
    image = models.ImageField(upload_to='contacts/', blank=True, null=True)

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        # зберігаємо початковий стан об'єкта
        self._initial_state = self.__dict__.copy()

    def save(self, *args, **kwargs):
        # Якщо у контакта вже є PK (тобто він існує), то визначаємо змінені поля
        if self.pk:
            changed_fields = []
            for field_name, initial_value in self._initial_state.items():
                if field_name != "id" and getattr(self, field_name) != initial_value:
                    changed_fields.append(f"{field_name}: {initial_value} -> {getattr(self, field_name)}")

            # Зберігаємо контакт
            super(Contact, self).save(*args, **kwargs)

            if changed_fields:
                details = f"Contact {self.first_name} {self.last_name} was updated. Changes: {', '.join(changed_fields)}"
                ContactActivityLog.objects.create(
                    contact=self,
                    activity_type="EDITED",
                    details=details
                )
        else:
            # Якщо це новий контакт, спочатку зберігаємо його
            super(Contact, self).save(*args, **kwargs)
            # Після збереження контакту, додаємо запис "Created" в ContactActivityLog
            ContactActivityLog.objects.create(
                contact=self,
                activity_type="CREATED",
                details=f"Contact {self.first_name} {self.last_name} was created."
            )


class ContactGroup(models.Model):
    name = models.CharField(max_length=50)
    contacts = models.ManyToManyField(Contact, related_name='contact_groups')

    def __str__(self):
        return self.name


class Events(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=50)
    contacts = models.ManyToManyField(Contact, related_name='events')

    def __str__(self):
        return self.title


class ContactActivityLog(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[('CREATED', 'Created'), ('EDITED', 'Edited')])
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"{self.contact} was {self.activity_type}: {self.timestamp}"
