from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
def estaUsuario(request):
    estas = True
    print(request.POST)
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'chequearUsuario':
            try:
                user = User.objects.get(username__iexact=request.POST['username'])   
                print(user)
                estas=False             
            except:
                print("no encontro nada")
                esta=True
    return JsonResponse(estas,safe=False)

def perfil(request):
    data = {
        'title': "Perfil",
        'icono_titulo': "fas fa-user-circle"
    }
    return render(request, "user/perfil.html", data)
