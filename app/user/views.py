from django.shortcuts import render

# Create your views here.


def perfil(request):
    data = {
        'title': "Perfil",
        'icono_titulo': "fas fa-user-circle"
    }
    return render(request, "user/perfil.html", data)
