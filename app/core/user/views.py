from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import DetailView
from django.contrib.auth.models import User
from core.user.models import Perfil


# Create your views here.


def estaUsuario(request):
    estas = True
    print(request.POST)
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'chequearUsuario':
            try:
                user = User.objects.get(
                    username__iexact=request.POST['username'])
                print(user)
                estas = False
            except:
                print("no encontro nada")
                estas = True
    return JsonResponse(estas, safe=False)


def verperfil(request):
    return redirect(f"/user/perfil/{request.user.perfil.pk}/")


class PerfilDetailView(DetailView):
    model = Perfil
    data = {
        'title': "Perfil",
        'icono_titulo': "fas fa-user-circle"
    }
    template_name = "user/perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Perfil"
        context['icono_titulo'] = "fas fa-user-circle"
        print(self.get_object())
        return context
