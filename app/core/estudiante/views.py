from django.shortcuts import render

# Create your views here.


def listar_cursos(request):
    return render(request, "estudiante/listar_curso.html")
