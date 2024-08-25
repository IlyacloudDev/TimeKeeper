from django.urls import path
from .views import EventCreate, EventDetail, EventList, EventUpdate, EventDelete


urlpatterns = [
    path('create-event/', EventCreate.as_view(), name='event_create'),
    path('list-events/', EventList.as_view(), name='event_list'),
    path('detail-event/<str:hash_id>/', EventDetail.as_view(), name='event_detail'),
    path('update-event/<str:hash_id>/', EventUpdate.as_view(), name='event_update'),
    path('delete-event/<str:hash_id>/', EventDelete.as_view(), name='event_delete')
]
