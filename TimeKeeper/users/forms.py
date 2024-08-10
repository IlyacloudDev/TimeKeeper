from django import forms
from django.templatetags.static import static
from allauth.account.forms import SignupForm
from .models import CustomUser


class CustomSignupForm(SignupForm):
    """
    Custom signup form with the default avatar set depending on gender
    """
    gender = forms.ChoiceField(choices=CustomUser.GENDER_TYPES, required=True)

    def save(self, request):
        user = super().save(request)
        user.gender = self.cleaned_data.get('gender')
        if user.gender == 'FE':
            user.avatar = 'default_avatars/female.jpg'
        else:
            user.avatar = 'default_avatars/male.jpg'
        user.save()
        return user
