import django_filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from .models import Contact, ContactGroup, Events
from .serializers import ContactSerializer, ContactGroupSerializer, EventSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response


# class IsOver18(BasePermission):
#     """
#     Дозволити доступ лише користувачам, яким 18 і більше років.
#     """
#     message = "Доступ заборонено для користувачів молодших 18 років."
#
#     def has_permission(self, request, view):
#         if request.user.date_of_birth:
#             today = date.today()
#             age = today.year - request.user.date_of_birth.year - (
#                         (today.month, today.day) < (request.user.date_of_birth.month, request.user.date_of_birth.day))
#             return age >= 18
#         return False


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['first_name', 'city']


class ContactGroupViewSet(ModelViewSet):
    queryset = ContactGroup.objects.prefetch_related('contacts')
    serializer_class = ContactGroupSerializer


class EventViewSet(ModelViewSet):
    queryset = Events.objects.prefetch_related('contacts')
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend]
    search_fields = ['title', 'description']


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    # filter_backends = [filters.SearchFilter]
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = ContactFilter
    # search_fields = ['first_name', 'last_name', 'city', 'country', 'street']
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny]
# def get_permissions(self):
#     """
#     Instantiates and returns the list of permissions that this view requires.
#     """
#     if self.action == 'list':
#         permission_classes = [IsAuthenticated]
#     else:
#         permission_classes = [IsAdminUser]
#     return [permission() for permission in permission_classes]
# class ContactList(ListAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['first_name', 'last_name', 'street']
#     permission_classes = [IsAuthenticated]
#
#
#     # def get(self, request, format=None):
#     #     contacts = Contact.objects.all()
#     #     serializer = ContactSerializer(contacts, many=True)  # передаємо список контактів
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
#     #
#     # def post(self, request, format=None):
#     #     serializer = ContactSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ContactCreate(CreateAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#
#
# class ContactUpdate(UpdateAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#
#
# class ContactRetrieve(RetrieveAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#     #lookup_field = поле за яким витягуємо обєкт
#
#
# class ContactDestroy(DestroyAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#
# # class ContactDetail(APIView):
# #     def get_object(self, pk):
# #         try:
# #             return Contact.objects.get(pk=pk)
# #         except Contact.DoesNotExist:
# #             raise Http404
# #
# #     def get(self, request, pk, format=None):
# #         contact = self.get_object(pk)
# #         serializer = ContactSerializer(contact)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
# #
# #     def put(self, request, pk, format=None):
# #         contact = self.get_object(pk)
# #         serializer = ContactSerializer(contact, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk, format=None):
# #         contact = self.get_object(pk)
# #         contact.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
