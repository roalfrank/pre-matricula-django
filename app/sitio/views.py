from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from config import settings

# Create your views here.


@login_required
def index(request):
    group = request.user.groups.all().first()
    
    if group.name == "Admin":
        return redirect(reverse("sitio:panel-admin"))
    elif group.name == "Estudiante":
        return redirect(reverse("sitio:panel-estudiante"))
    elif group.name == "Gestor":
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
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre':"Roaldys","municipio":"Regla"},
            {'nombre':"Roaldys","municipio":"Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"},
            {'nombre': "Roaldys", "municipio": "Regla"}],
        'notificacioneEncabezado': [
            {'nombre': "Curso"},
            {'nombre': "Municipio"},
            {'nombre': "Accion"}
        ],
        'casiMatriculados': [
            {'nombre': "Roaldys", "municipio": "Regla",'tipo':'Corto'},
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
    return render(request, "sitio/panelEstudiante.html", context)

