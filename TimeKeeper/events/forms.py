from django import forms
from .models import Event


class EventCreateForm(forms.ModelForm):
    """
    Form for creating event.
    """
    class Meta:
        model = Event
        fields = ['title', 'content']
