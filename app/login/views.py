from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView,TemplateView
from django.template.loader import render_to_string
from django.urls import reverse
from config import settings
from django.contrib.auth.forms import UserCreationForm
from sitio.utilitario import mandar_correo
from .form import UserRegistrationForm,UserPerfilRegistrationForm
# Create your views here.


class LoginFormView(LoginView):
    template_name = 'login/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        cuerpo= render_to_string("sitio/email.html")
        mandar_correo("roaldis.garcia@cha.jovenclub.cu",
                      "Hola desde django con utilitario", cuerpo, html=True)
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context



#registrar
class RegistarView(CreateView):
    form_class = UserCreationForm
    template_name='login/registrar.html'
    success_url= '/login/registrar/success/'

    def dispatch(self, request, *args, **kwargs):
        print(request.POST)
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(reverse('login:registrado'))
        return context


class BienRegistradoView(TemplateView):
    template_name = 'login/bienRegistrado.html'
