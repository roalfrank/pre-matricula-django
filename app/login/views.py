from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from config import settings
# Create your views here.


def LoginUser(request):
    return render(request, "login/login.html")


class LoginFormView(LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context
