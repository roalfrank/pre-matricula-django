from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from core.preMatricula.models import PreMatricula

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
    return render(request, "sitio/panelAdmin.html", context)


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
