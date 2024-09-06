import os
from django.contrib.auth import authenticate
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import CustomUser
from .forms import CustomUserUpdateForm, PasswordConfirmationForm


class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating user data
    """

    form_class = CustomUserUpdateForm
    model = CustomUser
    template_name = 'users/update.html'
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)

        self.object.refresh_from_db()
        old_avatar_path = self.object.avatar.path

        # проверяем, пользователь изменил только пол в настройках пользователя или же ещё аватар
        if ('gender' in form.changed_data) and ('avatar' not in form.changed_data):
            # если пользователь изменил только пол, смотри, стоит ли у него дефолтная аватарка
            if self.request.user.avatar.url in ['/media/default_avatars/female.jpg', '/media/default_avatars/male.jpg']:
                # если стоит дефолтная аватарка, меняем на другую дефолтную аватарку в зависимости от пола
                if self.request.user.avatar.url == '/media/default_avatars/female.jpg':
                    self.request.user.avatar = 'default_avatars/male.jpg'
                    user.save()
                else:
                    self.request.user.avatar = 'default_avatars/female.jpg'
                    user.save()
        elif 'avatar' in form.changed_data:
            new_avatar = form.cleaned_data.get('avatar')
            self.request.user.avatar = new_avatar  # Присваиваем новый аватар
            if os.path.exists(old_avatar_path) and old_avatar_path not in ['/media/default_avatars/female.jpg', '/media/default_avatars/male.jpg']:  # Удаляем старый аватар после сохранения
                os.remove(old_avatar_path)
            user.save()  # Сохраняем пользователя с новым аватаром
        return super().form_valid(form)


class CustomUserDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting user account
    """
    model = CustomUser
    form_class = PasswordConfirmationForm
    template_name = 'users/delete.html'
    success_url = reverse_lazy('start')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        user = authenticate(username=self.request.user.username, password=password)
        if user is not None:
            # Удаляем пользователя
            self.request.user.delete()
            # Перенаправляем на success_url
            return HttpResponseRedirect(self.success_url)
        else:
            form.add_error('password', _("Password incorrect. Please try again."))
            return self.form_invalid(form)
