from django import forms
from django.utils.translation import gettext_lazy as _


class AvatarForm(forms.Form):
    """
    Form for processing an image from the user
    """
    avatar = forms.ImageField(
        required=True,
        label=_("Upload an image for formatting")
    )
