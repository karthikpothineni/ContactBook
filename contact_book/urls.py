from django.conf.urls import url, include
from .views.contactViews import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/v1/contact', ContactViewSet ,base_name='contacts')
router.register(r'api/v1/user', UserViewSet ,base_name='user')


urlpatterns = [
    url(r'^api/v1/login', LoginViewSet.as_view({ 'post': 'login'}), name='login'),
    url(r'^api/v1/get-contacts', ContactViewSet.as_view({ 'post': 'get_contacts'}), name='get_contacts'),
    url(r'^api/v1/health',  healthcheck_view.as_view()),
    url(r'^', include(router.urls)),
]
