from django.urls import path
from core.preMatricula.logica.tbentidad.Provincia.views import createProvincia

app_name = "prematricula"

urlpatterns = [
    path("provincia/list/", createProvincia, name="listar-provincia"),
]
