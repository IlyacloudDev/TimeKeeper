from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Event, CustomUser
from .forms import EventCreateForm


@login_required
def test(request):
    return render(request, 'base.html')


class EventCreate(LoginRequiredMixin, CreateView):
    form_class = EventCreateForm
    model = Event
    template_name = 'events/create.html'
    success_url = reverse_lazy('test')

    def form_valid(self, form):
        form.instance.user = CustomUser.objects.get(pk=self.request.user.id)
        return super().form_valid(form)
