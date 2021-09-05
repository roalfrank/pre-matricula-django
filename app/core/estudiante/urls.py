from django.urls import path
from .views import listar_cursos

app_name = "estudiante"

urlpatterns = [
    path("listar-curso/", listar_cursos, name="listar-curso"),
]
