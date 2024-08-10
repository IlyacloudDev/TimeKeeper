from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import CustomUser
from .forms import CustomUserUpdateForm


class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating user data
    """

    form_class = CustomUserUpdateForm
    model = CustomUser
    template_name = 'users/update.html'
    success_url = reverse_lazy('test')

    def get_object(self, queryset=None):
        return self.request.user
