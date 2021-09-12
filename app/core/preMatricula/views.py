from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Estudiante

# Create your views here.


@login_required
@permission_required('preMatricula.view_estudiante', raise_exception=True)
def buscarEstudiante(request):
    if request.method == 'POST':
        id_estudiante = int(request.POST['id_estudiante'])
        estudiante = Estudiante.objects.filter(pk=id_estudiante)[0]
        datos = estudiante.datosAllJson()
        datos['enviado'] = True
        return JsonResponse(datos, safe=False)
    return JsonResponse([], safe=False)


@login_required
@permission_required('preMatricula.view_estudiante', raise_exception=True)
def uniqueUser(request):
    if request.method == 'POST':
        print('estoy en unique ')
        respuesta = {}
        respuesta['youPass'] = False
        username = (request.POST['username'])
        user = User.objects.filter(username=username)
        if not user:
            respuesta['youPass'] = True
        print(respuesta)
        return JsonResponse(respuesta, safe=False)
    return JsonResponse([], safe=False)
