from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
# from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from .models import Event, CustomUser
from .forms import EventCreateForm, EventDeleteConfirmationForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'  # Указываем, что происходит создание
        return context


class EventUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating content and title of event
    """
    form_class = EventCreateForm
    model = Event
    template_name = 'events/create.html'
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        hash_id = self.kwargs.get('hash_id')
        user = CustomUser.objects.get(pk=self.request.user.id)  # текущий аутентифицированный пользователь
        event = Event.objects.get(hash_id=hash_id, user=user)

        return event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'  # Указываем, что происходит создание
        return context


class EventDetail(LoginRequiredMixin, DetailView):
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
        return Event.objects.filter(user=self.request.user).order_by('-updated_at')


class EventDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting event
    """
    model = Event
    form_class = EventDeleteConfirmationForm
    template_name = 'events/delete.html'
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        hash_id = self.kwargs.get('hash_id')
        user = CustomUser.objects.get(pk=self.request.user.id)  # текущий аутентифицированный пользователь
        event = Event.objects.get(hash_id=hash_id, user=user)

        return event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event = self.get_object()
        sentence = f'I want to delete "{event.title}"!'
        context['sentence'] = sentence

        return context

    def form_valid(self, form):
        sentence_form_user = form.cleaned_data.get('sentence')
        event = self.get_object()
        expected_sentence = f'I want to delete "{event.title}"!'

        if expected_sentence == sentence_form_user:
            event.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            form.add_error('sentence', _("Sentences must match in content"))
            return self.form_invalid(form)
