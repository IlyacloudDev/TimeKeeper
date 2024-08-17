from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Administrative panel for the model Event
    """
    list_display = ('title', 'created_at', 'updated_at', 'user')
    search_fields = ('title',)
