from django.contrib import admin

from .models import Contact, ContactGroup, Events

admin.site.register(Contact)
admin.site.register(ContactGroup)
admin.site.register(Events)
