from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.humanize.templatetags.humanize import naturaltime
from core.preMatricula.models import PreMatricula
from core.preMatricula.models import Comentario

#from .form import TipoCursoForm


def rowComentarioHijo(request):
    if request.method == 'POST':
        id_comentario_hijo = int(request.POST['id_comentario_hijo'])
        id_comentario_papa = int(request.POST['id_comentario_papa'])
        comentario_hijo = Comentario.objects.filter(
            pk=id_comentario_hijo).first()
        cant_comentario_a_papa = Comentario.objects.filter(
            respuestaA__pk=id_comentario_papa, aprobado=True).count()
        context = {}
        html_string = render_to_string(
            'comentario/row_comentario_hijo.html', {'comentario': comentario_hijo}, request)
        context['html'] = html_string
        context['cantidad_respuesta'] = cant_comentario_a_papa
        context['texto'] = comentario_hijo.texto
        return JsonResponse(context, safe=False)


def rowComentario(request):
    if request.method == 'POST':
        id_comentario = int(request.POST['id_comentario'])
        comentario = Comentario.objects.filter(pk=id_comentario).first()
        id_matricula = comentario.preMatricula.pk
        context = {}
        html_string = render_to_string(
            'comentario/row_comentario.html', {'comentario': comentario, 'id_matricula': id_matricula}, request)
        context['html'] = html_string
        #context['fecha'] = naturaltime(comentario.fecha_comentario)
        context['fecha'] = comentario.fecha_comentario

        return JsonResponse(context, safe=False)


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
