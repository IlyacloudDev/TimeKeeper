from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom model of User with extra avatar-field and gender-field.
    """

    female = 'FE'
    male = 'MA'
    GENDER_TYPES = [
        (female, _('Female')),
        (male, _('Male')),
    ]

    gender = models.CharField(
        max_length=2,
        choices=GENDER_TYPES,
        default=female,
        verbose_name=_('Gender of user')
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name=_('Avatar of user')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
