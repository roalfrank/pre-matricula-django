from core.preMatricula.models import PreMatricula
from django.http import JsonResponse
from django.shortcuts import render
from core.preMatricula.models import Comentario

#from .form import TipoCursoForm


def ListarComentariosPorMatricula(request):
    template_name = 'comentario/listar_comentario.html'
    if request.method == 'POST':
        id_matricula = int(request.POST['id_matricula'])
        listado = Comentario.objects.filter(
            preMatricula__pk=id_matricula, aprobado=True, respuestaA=None).order_by('-fecha_comentario',)
        print(listado)
        respuesta = {
            'id_matricula': id_matricula,
            'object_list': listado
        }

        return render(request, template_name, respuesta)


def AddComentario(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.POST['texto'])
        respuesta = {}
        try:
            action = request.POST['action']
            id_matricula = int(request.POST['id_matricula'])

            matricula = PreMatricula.objects.get(pk=id_matricula)
            texto = request.POST['texto']
            comentario = Comentario(
                texto=texto, preMatricula=matricula, usuario=request.user)
            if action == 'hijo':
                id_comentarioa = int(request.POST['id_comentario'])
                comentarioa = Comentario.objects.get(pk=id_comentarioa)
                comentario.respuestaA = comentarioa
            if request.user.perfil.tipo == 'ES':
                comentario.aprobado = False
                respuesta['estudiante'] = True
            else:
                respuesta['estudiante'] = False
            comentario.save()
            respuesta['error'] = False

        except Exception as e:
            respuesta['error'] = True
            print(e)
            respuesta['error_text'] = e
        return JsonResponse(respuesta, safe=False)
