from django.urls import path
# importaciones para entidades
from core.preMatricula.logica.tbentidad.Provincia.views import ProvinciaListView, buscarMunicipios
from core.preMatricula.logica.tbentidad.entidadMunicipio.views import MunicipioView
# importaciones para instructores
from core.preMatricula.logica.instructor.cargoinstructor.views import CargoInstructorView
# importaciones para estudiantes
from core.preMatricula.logica.estudiante.estudianteocupacion.views import OcupacionEstudianteView
from core.preMatricula.logica.estudiante.estudiantediscapacidad.views import DiscapacidadEstudianteView
from core.preMatricula.logica.estudiante.estudianteCatOcupacional.views import CategoriaOcupacionalEstudianteView
from core.preMatricula.logica.estudiante.estudiante.views import EstudianteView
# importaciones para cursos
from core.preMatricula.logica.curso.cursoTipo.views import TipoCursoView
# importaciones para matricula
from core.preMatricula.logica.matricula.matriculaModalidad.views import ModalidadMatriculaView
from core.preMatricula.logica.matricula.matriculaEstado.views import EstadoMatriculaView


app_name = "prematricula"

urlpatterns = [
    # Enlaces de las entidades
    path("provincia/", ProvinciaListView.as_view(), name="listar-provincia"),
    path("municipio/buscar/", buscarMunicipios, name="buscar-municipios"),
    path("entidad-municipio/", MunicipioView.as_view(), name="entidad-municipio"),
    # --- Istructor enlaces -----
    path("cargo-instructor/", CargoInstructorView.as_view(),
         name="cargo-instructor"),
    # --Estudiante enlaces -----
    path("estudiante-ocupacion/", OcupacionEstudianteView.as_view(),
         name="estudiante-ocupacion"),
    path("estudiante-discapacidad/", DiscapacidadEstudianteView.as_view(),
         name="estudiante-discapacidad"),
    path("estudiante-categoria-ocupacional/", CategoriaOcupacionalEstudianteView.as_view(),
         name="estudiante-cat-ocupacional"),
    path("estudiante/", EstudianteView.as_view(),
         name="estudiante"),
    # --- Todo relacionado con los cursos
    path("curso-tipo/", TipoCursoView.as_view(),
         name="curso-tipo"),
    # --- Todo relacionado con los matricula
    path("matricula-modalidad/", ModalidadMatriculaView.as_view(),
         name="matricula-modalidad"),
    path("matricula-estado/", EstadoMatriculaView.as_view(),
         name="matricula-estado"),

]
