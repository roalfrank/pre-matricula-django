from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from config import settings
from core.sitio.utilitario import mandar_correo
from .form import UserRegistrationForm, UserPerfilRegistrationForm
from core.preMatricula.models import Municipio
# Create your views here.


class LoginFormView(LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        # cuerpo= render_to_string("sitio/email.html",{
        #     'link_activar':'Aqui va el linck para activar'
        # })
        # mandar_correo("roaldis.garcia@cha.jovenclub.cu",
        #               "Hola desde django con utilitario", cuerpo, html=True)

        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


# registrar
class RegistarUsuarioOnlineView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'login/registrar.html'
    success_url = reverse_lazy('sitio:enrutador-sistema')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_user = UserRegistrationForm(request.POST)
        form_perfil = UserPerfilRegistrationForm(
            request.POST, request.FILES, prefix="perfil")
        if form_user.is_valid() and form_perfil.is_valid():
            user = form_user.save(commit=False)
            # user.is_active=False
            user.save()
            grupo_estudiante = Group.objects.filter(name='Estudiante')[0]
            user.groups.add(grupo_estudiante)
            user_perfil = form_perfil.save(commit=False)
            user_perfil.user = user
            user_perfil.save()
            cuerpo = render_to_string("sitio/email.html", {
                'link_activar': 'Link para activar',

            })
            mandar_correo(user_perfil.correo,
                          "Hola desde django con utilitario", cuerpo, html=True)

            return redirect(reverse_lazy('sitio:enrutador-sistema'))

        return render(request, self.template_name, {'formPerfil': form_perfil, 'form': form_user})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formPerfil'] = UserPerfilRegistrationForm(prefix="perfil")
        return context


class BienRegistradoView(TemplateView):
    template_name = 'login/bienRegistrado.html'
