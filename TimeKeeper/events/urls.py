from django.urls import path
from .views import test, EventCreate


urlpatterns = [
    path('', test, name='test'),
    path('create-event/', EventCreate.as_view(), name='event_create')
]