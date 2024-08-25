from django import forms
from .models import Event
from django.utils.translation import gettext_lazy as _


class EventCreateForm(forms.ModelForm):
    """
    Form for creating event.
    """
    class Meta:
        model = Event
        fields = ['title', 'content']


class EventDeleteConfirmationForm(forms.Form):
    """
    Form for confirmation of event deleting
    """
    sentence = forms.CharField(
        label=_("Repeat sentence below"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
