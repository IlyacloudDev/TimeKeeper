from django import forms
from django.shortcuts import reverse
from allauth.account.forms import SignupForm
from PIL import Image
from .models import CustomUser
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class CustomSignupForm(SignupForm):
    """
    Custom signup form with the default avatar set depending on gender
    """
    gender = forms.ChoiceField(choices=CustomUser.GENDER_TYPES, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        min_length = 3
        max_length = 14
        if len(username) < min_length or len(username) > max_length:
            raise forms.ValidationError(
                _(f'Username must be between {min_length} and {max_length} characters.')
            )
        return username

    def save(self, request):
        user = super().save(request)
        user.gender = self.cleaned_data.get('gender')
        if user.gender == 'FE':
            user.avatar = 'default_avatars/female.jpg'
        else:
            user.avatar = 'default_avatars/male.jpg'
        user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    """
    Form for updating user data
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'gender', 'avatar']

    def clean_username(self):
        username = self.cleaned_data['username']
        min_length = 3
        max_length = 14
        if len(username) < min_length or len(username) > max_length:
            raise forms.ValidationError(
                _(f'Username must be between {min_length} and {max_length} characters.')
            )
        return username

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        image = Image.open(avatar)
        width, height = image.size
        if width != height:
            # Получаем URL для страницы форматирования изображения
            format_url = reverse('format_avatar')  # Убедитесь, что 'format_avatar' - правильное имя URL
            error_message = format_html(
                'The avatar must be square (1:1 aspect ratio). You can change the scale of the image <a href="{0}">here</a>.',
                format_url
            )
            raise forms.ValidationError(error_message)

        # Можно также добавить проверку на минимальный/максимальный размер изображения
        max_dimension = 3000
        if width > max_dimension or height > max_dimension:
            raise forms.ValidationError(f"Image size should not exceed {max_dimension}x{max_dimension} pixels.")
        return avatar


class PasswordConfirmationForm(forms.Form):
    """
    Form for confirmation password of user's account
    """
    password = forms.CharField(
        label=_("Please enter your password to confirm"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
