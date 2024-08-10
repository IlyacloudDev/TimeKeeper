from django.contrib import admin
from django.utils.html import format_html


from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Administrative panel for the model CustomUser
    """
    list_display = ('username', 'email', 'gender')
    search_fields = ('username', 'email')
