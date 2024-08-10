from django.urls import path
from .views import CustomUserUpdate


urlpatterns = [
    path('edit-account/', CustomUserUpdate.as_view(), name='account_edit'),
]
