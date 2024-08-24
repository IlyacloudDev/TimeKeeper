from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from .models import Event, CustomUser
from .forms import EventCreateForm


class EventCreate(LoginRequiredMixin, CreateView):
    """
    View for creating event
    """
    form_class = EventCreateForm
    model = Event
    template_name = 'events/create.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.user = CustomUser.objects.get(pk=self.request.user.id)
        return super().form_valid(form)


class EventDetail(LoginRequiredMixin, DeleteView):
    """
    View for checking details of event. (Use hashed ID in URL for checking)
    """
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        hash_id = self.kwargs.get('hash_id')
        user = CustomUser.objects.get(pk=self.request.user.id)  # текущий аутентифицированный пользователь

        event = Event.objects.get(hash_id=hash_id, user=user)

        return event


class EventList(LoginRequiredMixin, ListView):
    """
    View for checking all own events
    """
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
