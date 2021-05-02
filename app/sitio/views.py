from django.shortcuts import render, redirect
from config import settings

# Create your views here.


def dashBoardPrincipal(request):
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
    return render(request, "sitio/dashboartPrincipal.html", context)

