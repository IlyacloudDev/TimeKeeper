from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
import hashlib


def generate_hash_id(pk):
    """
    Generates a hashed ID based on the primary key.
    The SHA-256 algorithm is used.
    """
    return hashlib.sha256(str(pk).encode('utf-8')).hexdigest()


class Event(models.Model):
    """
    Model of Event.

    Fields:
        title: title of  event;
        content: content of event;
        created_at: date and time of creating event
        updated_at: date and time of updating event
        user: a foreign key for the "CustomUser" model with a one-to-many connection
    """
    hash_id = models.CharField(max_length=64, unique=True, blank=True, null=True, verbose_name=_('Hashed ID'))
    title = models.CharField(max_length=100, verbose_name=_('Title of event'))
    content = models.TextField(verbose_name=_('Content of event'), help_text=_('You have ability use "Markdown"'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and time of creating'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date and time of updating'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events', verbose_name=_('User'))

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект, чтобы получить id
        if not self.pk:  # Если объект новый, то сохраняем его
            super().save(*args, **kwargs)

        if not self.hash_id:
            self.hash_id = generate_hash_id(self.pk)  # Используем pk для генерации уникального хэша

        super().save(*args, **kwargs)  # Сохраняем объект с новым hash_id

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
