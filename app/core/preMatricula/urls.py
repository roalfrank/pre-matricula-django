from django.urls import path
from core.preMatricula.logica.tbentidad.Provincia.views import ProvinciaListView
from core.preMatricula.logica.tbentidad.estadousuario.views import EstadoView
from core.preMatricula.logica.tbentidad.cargoinstructor.views import CargoInstructorView
from core.preMatricula.logica.tbentidad.estudianteocupacion.views import OcupacionEstudianteView
from core.preMatricula.logica.tbsistema.estudiante.views import EstudianteView

app_name = "prematricula"

urlpatterns = [
    #url de tablas  pequenas sin dependencia
    path("provincia/", ProvinciaListView.as_view(), name="listar-provincia"),
    path("estado-usuario/", EstadoView.as_view(), name="estado-usuario"),
    path("cargo-instructor/", CargoInstructorView.as_view(),
        name="cargo-instructor"),
    path("estudiante-ocupacion/", OcupacionEstudianteView.as_view(),
        name="estudiante-ocupacion"),
    path("estudiante/", EstudianteView.as_view(),
        name="estudiante"),

]
