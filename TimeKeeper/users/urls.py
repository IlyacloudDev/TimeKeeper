from django.urls import path
from .views import CustomUserUpdate, CustomUserDelete


urlpatterns = [
    path('edit-account/', CustomUserUpdate.as_view(), name='account_edit'),
    path('delete-account/', CustomUserDelete.as_view(), name='account_delete'),
]
