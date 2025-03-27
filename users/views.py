import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView
from config.settings import DEFAULT_FROM_EMAIL
from .forms import CustomUserCreationForm, CustomUserEditForm
from .models import CustomUser
from django.http import HttpResponseForbidden


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.has_perm('users.view_customuser'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Вы не можете просматривать этот объект.")


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("mailing:index")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Приветствуем вас на нашем сайте! Перейдите по ссылке для подтверждения эл. почты {url}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],)
        return super().form_valid(form)


@method_decorator(permission_required('users.can_block_user'), name='dispatch')
class UserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        system_user = get_object_or_404(CustomUser, pk=pk)
        system_user.is_active = not system_user.is_active
        system_user.save()
        return redirect("users:users")


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.token = ''
    user.save()
    return redirect(reverse("users:login"))


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'users/user_profile_edit.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self):
        return self.request.user
