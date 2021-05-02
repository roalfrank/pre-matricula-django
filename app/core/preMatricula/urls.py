from django.urls import path
from core.preMatricula.logica.tbentidad.Provincia.views import ProvinciaListView

app_name = "prematricula"

urlpatterns = [
    path("provincia/", ProvinciaListView.as_view(), name="listar-provincia"),
]
