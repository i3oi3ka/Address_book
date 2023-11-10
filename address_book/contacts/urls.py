from rest_framework.routers import DefaultRouter

from .views import ContactViewSet, ContactGroupViewSet, EventViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet, basename='contact')
router.register('contact_group', ContactGroupViewSet, basename='contact_group')
router.register('event', EventViewSet, basename='event')


urlpatterns = router.urls
