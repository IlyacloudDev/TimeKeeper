from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


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

    title = models.CharField(max_length=100, verbose_name=_('Title of event'))
    content = models.TextField(verbose_name=_('Content of event'), help_text=_('You have ability use "Markdown"'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and time of creating'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date and time of updating'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events', verbose_name=_('User'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
