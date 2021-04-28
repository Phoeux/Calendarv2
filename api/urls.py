from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('users', views.UserModelViewset, basename='users'),
router.register('countries', views.CountryModelViewset, basename='countries'),
router.register('holidays', views.HolidayModelViewset, basename='holidays'),
router.register('events', views.EventModelViewset, basename='events'),

urlpatterns = [
    path('', include((router.urls, 'api'))),

]
