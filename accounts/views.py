from typing import Any, Dict
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, ProfileForm, CustomPasswordChangeForm


class Registration(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:list')
        return super().get(request, *args, **kwargs)

### Login
class Login(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:list')
        return super().get(request, *args, **kwargs)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('blog:list')


class Update(LoginRequiredMixin, FormView):
    template_name = 'accounts/update.html'
    form_class = ProfileForm
    success_url = reverse_lazy('blog:list')

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        initial['nickname'] = self.request.user.nickname
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, self.request.user)
        return super().form_valid(form)


class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('blog:list')
    template_name = 'accounts/change_password.html'


Registration = Registration.as_view()
Login = Login.as_view()
Logout = Logout.as_view()
Update = Update.as_view()
PasswordChange = PasswordChange.as_view()
