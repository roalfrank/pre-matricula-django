from django.urls import path
from core.preMatricula.logica.tbentidad.Provincia.views import ProvinciaListView
from core.preMatricula.logica.tbentidad.estadousuario.views import EstadoView
app_name = "prematricula"

urlpatterns = [
    #url de tablas  pequenas sin dependencia
    path("provincia/", ProvinciaListView.as_view(), name="listar-provincia"),
    path("estado-usuario/", EstadoView.as_view(), name="estado-usuario"),

]
