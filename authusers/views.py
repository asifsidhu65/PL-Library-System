from braces.views import AnonymousRequiredMixin, LoginRequiredMixin
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import FormView, TemplateView
from .forms import AuthSignupForm, AuthLoginForm


class AuthLoginView(AnonymousRequiredMixin, FormView):
    template_name = 'authusers/login.html'
    form_class = AuthLoginForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        login(self.request, form.user)
        expiry = settings.ACCOUNT_REMEMBER_ME_EXPIRY if form.cleaned_data.get("remember") else 0
        self.request.session.set_expiry(expiry)
        return HttpResponseRedirect('/')


class AuthSignupView(AnonymousRequiredMixin, FormView):

    template_name = "authusers/signup.html"
    form_class = AuthSignupForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        data = form.cleaned_data
        user = User()
        user.is_active = True
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.username = data.get('username')
        user.email = data.get('email')
        user.set_password(data.get('password'))
        user.save()
        user = authenticate(username=user.username, password=data.get('password'))

        if user:
            login(self.request, user)

        return HttpResponseRedirect('/')


class AuthLogoutView(LoginRequiredMixin, View):
    http_method_names = ['get']
    template_name = 'authusers/logout.html'

    def get(self, *args, **kwargs):
        auth.logout(self.request)
        return render(self.request, self.template_name, context={})




