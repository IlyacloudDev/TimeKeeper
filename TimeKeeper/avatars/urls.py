from django.urls import path
from .views import FormattingAvatar


urlpatterns = [
    path('formatting-avatar/', FormattingAvatar.as_view(), name='format_avatar')
]
