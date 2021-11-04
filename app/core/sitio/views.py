import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from core.preMatricula.models import PreMatricula
from core.preMatricula.logica.curso.curso.views import cantCursos
from core.preMatricula.logica.estudiante.estudiante.views import (
    cantEstudiantes,
    cant_estudiantes_no_matriculados,
    reporte_estudiante_semana_actual,
    matriculados_en_la_semana_actual
)
from core.preMatricula.logica.maestro.views import cantidadMaestro

from config import settings

# Create your views here.


def index(request):
    context = {}
    context['base_url'] = "{0}://{1}{2}".format(
        request.scheme, request.get_host(), '/sistema/matricula-pagina/')
    context['listado_curso'] = PreMatricula.objects.all().order_by(
        "-fecha_creado")[0:8]
    print(context['listado_curso'])
    return render(request, "sitio/inicio/index.html", context)


@login_required
def enrutadorSistema(request):
    group = request.user.groups.all().first()

    if group.name == "Admin":
        return redirect(reverse("sitio:panel-admin"))
    elif group.name == "Estudiante":
        return redirect(reverse("sitio:panel-estudiante"))
    elif group.name == "Gestor":
        return redirect(reverse("sitio:panel-gestor"))
    elif group.name == "Instructor":
        return redirect(reverse("sitio:panel-gestor"))
    elif group.name == "Maestro":
        return redirect(reverse("sitio:panel-gestor"))
    else:

        return HttpResponseForbidden()


def dashBoardGestor(request):
    if not request.user.is_authenticated:
        return redirect("login:login-user")
    context = {
        "title": "Panel Principal",
        'notificaciones': [
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"}],
        'notificacioneEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        'casiMatriculados': [
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'}],
        'casiMatriculadosEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Tipo"},
            {'nombre': "Accion"}
        ],
        'cursosRecientes': [
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"}],
        'cursosRecientesEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        "icono_titulo": "fas fa-tachometer-alt"
    }
    return render(request, "sitio/panelGestor.html", context)


def dashBoardAdmin(request):
    if not request.user.is_authenticated:
        return redirect("login:login-user")
    context = {
        "title": "Panel Principal",
        'notificaciones': [
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"}],
        'notificacioneEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        'casiMatriculados': [
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Roaldys", "municipio": "Regla", 'tipo': 'Corto'}],
        'casiMatriculadosEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Tipo"},
            {'nombre': "Accion"}
        ],
        'cursosRecientes': [
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"}],
        'cursosRecientesEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        "icono_titulo": "fas fa-tachometer-alt"
    }
    context['cantidadCurso'] = cantCursos()
    context['cantidadEstudiante'] = cantEstudiantes()
    context['cantidadMaestro'] = cantidadMaestro()
    context['cantidadNoMatriculado'] = cant_estudiantes_no_matriculados()
    # usuarios en la semana cantidad
    context['reporte_semanal_estudiante'] = reporte_semanal_estudiante_admin()
    # fin usuarios en la semana cantidad
    context['reporte_semanal_estudiante_matriculados'] = reporte_semanal_estudiante_matriculado_admin()
    # fin usuarios en la semana cantidad matriculados
    return render(request, "sitio/panelAdmin.html", context)


def reporte_semanal_estudiante_matriculado_admin():
    # usuarios en la semana cantidad matriculados
    matriculados_en_la_semana_actual_sedult = matriculados_en_la_semana_actual()
    reporte_semanal_estudiante_matriculados = {}
    reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_actual'] = matriculados_en_la_semana_actual_sedult['cantidad_estudiantes_semana_matriculado_actual']
    reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada'] = matriculados_en_la_semana_actual_sedult['cantidad_estudiantes_semana_matriculado_pasada']
    if reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_actual'] < reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada']:
        reporte_semanal_estudiante_matriculados['maximo'] = reporte_semanal_estudiante_matriculados[
            'cantidad_estudiantes_semana_matriculado_pasada']
    else:
        reporte_semanal_estudiante_matriculados['maximo'] = reporte_semanal_estudiante_matriculados[
            'cantidad_estudiantes_semana_matriculado_actual']
    # si las cantidades son 0 ,
    if reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_actual'] == 0 and reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada'] == 0:
        reporte_semanal_estudiante_matriculados['color_porciento'] = 'danger'
        reporte_semanal_estudiante_matriculados['porciento'] = '0%'
        reporte_semanal_estudiante_matriculados['icono'] = 'fas fa-warning'
    # si las cantidades semana anterior es 0
    elif reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada'] == 0:
        reporte_semanal_estudiante_matriculados['color_porciento'] = 'success'
        reporte_semanal_estudiante_matriculados['porciento'] = str(
            reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_actual'])+' estudiante'
        reporte_semanal_estudiante_matriculados['icono'] = 'fas fa-arrow-up'
    elif reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_actual'] == 0:
        reporte_semanal_estudiante_matriculados['color_porciento'] = 'danger'
        reporte_semanal_estudiante_matriculados['porciento'] = '-100%'
        reporte_semanal_estudiante_matriculados['icono'] = 'fas fa-arrow-down'
    else:
        diferencia_cant_semanal = reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada'] - \
            reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_actual']
        if diferencia_cant_semanal == 0:
            reporte_semanal_estudiante_matriculados['color_porciento'] = 'warning'
            reporte_semanal_estudiante_matriculados['porciento'] = "100%"
            reporte_semanal_estudiante_matriculados['icono'] = 'fas fa-warning'
        elif diferencia_cant_semanal < 0:
            diferencia_cant_semanal = diferencia_cant_semanal * -1
            porciento_semana = (diferencia_cant_semanal * 100) / \
                reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada']
            reporte_semanal_estudiante_matriculados['porciento'] = str(
                porciento_semana)+'%'
            reporte_semanal_estudiante_matriculados['color_porciento'] = 'success'
            reporte_semanal_estudiante_matriculados['icono'] = 'fas fa-arrow-up'
        else:
            porciento_semana = (diferencia_cant_semanal * 100) / \
                reporte_semanal_estudiante_matriculados['cantidad_estudiantes_semana_matriculado_pasada']
            reporte_semanal_estudiante_matriculados['porciento'] = str(
                porciento_semana)+'%'
            reporte_semanal_estudiante_matriculados['color_porciento'] = 'danger'
            reporte_semanal_estudiante_matriculados['icono'] = 'fas fa-arrow-down'
    reporte_semanal_estudiante_matriculados['lista_cantidad_estudiantes_dias_matriculado_actual'] = matriculados_en_la_semana_actual_sedult[
        'lista_cantidad_estudiantes_dias_matriculado_actual']
    reporte_semanal_estudiante_matriculados['lista_cantidad_estudiantes_dias_matriculado_pasado'] = matriculados_en_la_semana_actual_sedult[
        'lista_cantidad_estudiantes_dias_matriculado_pasado']
    return reporte_semanal_estudiante_matriculados


def reporte_semanal_estudiante_admin():
    # llamo al metodo para saber las cantidades de estudiantes semana actual y anterior
    datos_reporte_semanal_nuevos = reporte_estudiante_semana_actual()
    # diccionario almacenar los datos a mandar para la plantilla
    reporte_semanal_estudiante = {}
    # guardo cantidad de estudiantes semana actual
    reporte_semanal_estudiante['cantidadEstudianteSemana'] = datos_reporte_semanal_nuevos['cantidad_estudiantes_semana_actual']
    # cantidad de estudiantes semana pasada
    reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior'] = datos_reporte_semanal_nuevos['cantidad_estudiantes_semana_pasada']
    # comprobar las cantidades para saber que condicion tomar
    if reporte_semanal_estudiante['cantidadEstudianteSemana'] < reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior']:
        reporte_semanal_estudiante['maximo'] = reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior']
    else:
        reporte_semanal_estudiante['maximo'] = reporte_semanal_estudiante['cantidadEstudianteSemana']
    # si las cantidades son 0 ,
    if reporte_semanal_estudiante['cantidadEstudianteSemana'] == 0 and reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior'] == 0:
        reporte_semanal_estudiante['color_porciento'] = 'danger'
        reporte_semanal_estudiante['porciento'] = '0%'
        reporte_semanal_estudiante['icono'] = 'fas fa-warning'
    # si las cantidades semana anterior es 0
    elif reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior'] == 0:
        reporte_semanal_estudiante['color_porciento'] = 'success'
        reporte_semanal_estudiante['porciento'] = str(
            reporte_semanal_estudiante['cantidadEstudianteSemana'])+' estudiante'
        reporte_semanal_estudiante['icono'] = 'fas fa-arrow-up'
    elif reporte_semanal_estudiante['cantidadEstudianteSemana'] == 0:
        reporte_semanal_estudiante['color_porciento'] = 'danger'
        reporte_semanal_estudiante['porciento'] = '-100%'
        reporte_semanal_estudiante['icono'] = 'fas fa-arrow-down'
    else:
        diferencia_cant_semanal = reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior'] - \
            reporte_semanal_estudiante['cantidadEstudianteSemana']
        if diferencia_cant_semanal == 0:
            reporte_semanal_estudiante['color_porciento'] = 'warnig'
            reporte_semanal_estudiante['porciento'] = "100%"
            reporte_semanal_estudiante['icono'] = 'fas fa-warning'
        elif diferencia_cant_semanal < 0:
            diferencia_cant_semanal = diferencia_cant_semanal * -1
            porciento_semana = (diferencia_cant_semanal * 100) / \
                reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior']
            reporte_semanal_estudiante['porciento'] = str(porciento_semana)+'%'
            reporte_semanal_estudiante['color_porciento'] = 'success'
            reporte_semanal_estudiante['icono'] = 'fas fa-arrow-up'
        else:
            porciento_semana = (diferencia_cant_semanal * 100) / \
                reporte_semanal_estudiante['cantidadEstudianteSemanaAnterior']
            reporte_semanal_estudiante['porciento'] = str(porciento_semana)+'%'
            reporte_semanal_estudiante['color_porciento'] = 'danger'
            reporte_semanal_estudiante['icono'] = 'fas fa-arrow-down'
    # cargar las listas de las cantidades por dias en contecxt
    reporte_semanal_estudiante['lista_cantidad_estudiantes_dias_actual'] = datos_reporte_semanal_nuevos['lista_cantidad_estudiantes_dias_actual']
    reporte_semanal_estudiante['lista_cantidad_estudiantes_dias_pasado'] = datos_reporte_semanal_nuevos['lista_cantidad_estudiantes_dias_pasado']
    return reporte_semanal_estudiante


def dashBoardEstudiante(request):
    if not request.user.is_authenticated:
        return redirect("login:login-user")
    context = {
        "title": "Panel Principal",
        'notificaciones': [
            {'nombre': "Aprobada su solicitud", "municipio": "SM"},
            {'nombre': "Verifique su perfil", "municipio": "Regla"},
            {'nombre': "dsdfsdf", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"}],
        'notificacioneEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        'casiMatriculados': [
            {'nombre': "Curso de Python", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Aprendiendo Windows", "municipio": "SMP", 'tipo': 'Corto'},
            {'nombre': "Curso Tablet", "municipio": "Cerro", 'tipo': 'Largo'},
            {'nombre': "Dibujando con Paint", "municipio": "Plaza", 'tipo': 'Corto'},
            {'nombre': "Word Básico", "municipio": "Guanabacoa", 'tipo': 'largo'}],
        'casiMatriculadosEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Tipo"},
            {'nombre': "Accion"}
        ],
        'cursosRecientes': [
            {'nombre': "Curso de Python", "municipio": "Regla", 'tipo': 'Corto'},
            {'nombre': "Aprendiendo Windows", "municipio": "SMP", 'tipo': 'Corto'},
            {'nombre': "Curso Tablet", "municipio": "Cerro", 'tipo': 'Largo'},
            {'nombre': "Dibujando con Paint", "municipio": "Plaza", 'tipo': 'Corto'},
            {'nombre': "Word Básico", "municipio": "Guanabacoa", 'tipo': 'largo'}],
        'cursosRecientesEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        "icono_titulo": "fas fa-tachometer-alt"
    }
    return render(request, "sitio/panelEstudiante.html", context)
