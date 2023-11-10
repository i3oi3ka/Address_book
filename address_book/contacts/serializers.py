from django.utils import timezone
from rest_framework import serializers

from .models import Contact, ContactGroup, Events


# class Post:
#     def __init__(self, name, description, created_at=None):
#         self.name = name
#         self.description = description
#         self.created_at = created_at or datetime.now()
#
#
# class PostSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=155)
#     description = serializers.CharField()
#     created_at = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         return Post(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name')
#         instance.description = validated_data.get('description')
#         instance.created_at = validated_data.get('created_at')
#         return instance

class ContactSerializer(serializers.ModelSerializer):
    # city = serializers.CharField(max_length=10)
    # phone = serializers.CharField(max_length=30, validators=[UniqueValidator(queryset=Contact.objects.all())])

    # def validate(self, data):
    #     if data['first_name'] == data['last_name']:
    #         raise serializers.ValidationError('hfgkljhklfgjklhfgkl')
    #
    #     return data
    #
    # def validate_city(self, value):
    #     if value == 'Incorrect':
    #         raise serializers.ValidationError('City cannot be "Incorrect"')
    #     return value
    #
    # def validate_phone(self, value):
    #     # Переконайтесь, що номер телефону починається з цифри
    #     if not value[0].isdigit():
    #         raise serializers.ValidationError("Номер телефону повинен починатися з цифри.")
    #     return value

    class Meta:
        model = Contact
        fields = '__all__'


class ContactEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name']


class ContactGroupSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = ContactGroup
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    contacts = ContactEventSerializer(many=True)

    class Meta:
        model = Events
        fields = '__all__'

    def validate_date_time(self, value):
        current_time = timezone.now()
        if value < current_time:
            raise serializers.ValidationError("Дата події не може бути менше поточної дати та часу.")
