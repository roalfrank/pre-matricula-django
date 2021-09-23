from django.urls import path
# importaciones para entidades
from core.preMatricula.logica.tbentidad.Provincia.views import ProvinciaListView, buscarMunicipios
from core.preMatricula.logica.tbentidad.entidadMunicipio.views import MunicipioView
from core.preMatricula.logica.tbentidad.entidadJcp.views import JcpView
from core.preMatricula.logica.tbentidad.entidadRegion.views import RegionListView
from core.preMatricula.logica.tbentidad.entidadJcm.views import JcmView
from core.preMatricula.logica.tbentidad.entidadJcb.views import JcbView
# importaciones para instructores
from core.preMatricula.logica.instructor.cargoinstructor.views import CargoInstructorView
# importaciones para estudiantes
from core.preMatricula.logica.estudiante.estudianteocupacion.views import OcupacionEstudianteView
from core.preMatricula.logica.estudiante.estudiantediscapacidad.views import DiscapacidadEstudianteView
from core.preMatricula.logica.estudiante.estudianteCatOcupacional.views import CategoriaOcupacionalEstudianteView
from core.preMatricula.logica.estudiante.estudiante.views import EstudianteView, EstudianteDetailView, EstudianteDetailCargarFormAddView
# importaciones para cursos
from core.preMatricula.logica.curso.cursoTipo.views import TipoCursoView
# importaciones para matricula
from core.preMatricula.logica.matricula.matriculaModalidad.views import ModalidadMatriculaView
from core.preMatricula.logica.matricula.matriculaEstado.views import EstadoMatriculaView
from core.preMatricula.logica.matricula.matricula.views import MatriculaDetailView, likeMatricula

# importaciones de comentarios
from core.preMatricula.logica.comentario.views import ListarComentariosPorMatricula, AddComentario

# importaciones para los metodos del sistema globales
from .views import buscarEstudiante, uniqueUser, DetalleMatriculaPage, getDetalle


app_name = "prematricula"

urlpatterns = [
    # Enlaces a los metodos del sistema globales
    path("estudiante-datos/", buscarEstudiante, name="estudiante-datos"),
    path("unique-username/", uniqueUser, name="unique-username"),

    # Enlaces de las entidades
    path("provincia/", ProvinciaListView.as_view(), name="listar-provincia"),
    path("municipio/buscar/", buscarMunicipios, name="buscar-municipios"),
    path("municipio/buscar/region<int:region>",
         buscarMunicipios, name="buscar-municipios-region"),
    path("entidad-municipio/", MunicipioView.as_view(), name="entidad-municipio"),
    path("entidad-jcp/", JcpView.as_view(), name="entidad-jcp"),
    path("entidad-region/", RegionListView.as_view(), name="entidad-region"),
    path("entidad-jcm/", JcmView.as_view(), name="entidad-jcm"),
    path("entidad-jcb/", JcbView.as_view(), name="entidad-jcb"),

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
    path("estudiante/", EstudianteView.as_view(), name="estudiante"),
    path("estudiante-detail/<int:pk>/",
         EstudianteDetailView.as_view(), name="estudiante-detail"),
    path("estudiante-add-form/",
         EstudianteDetailCargarFormAddView.as_view(), name="estudiante-add-form"),


    # --- Todo relacionado con los cursos
    path("curso-tipo/", TipoCursoView.as_view(),
         name="curso-tipo"),


    # --- Todo relacionado con los matricula
    path("matricula-modalidad/", ModalidadMatriculaView.as_view(),
         name="matricula-modalidad"),
    path("matricula-estado/", EstadoMatriculaView.as_view(),
         name="matricula-estado"),
    path("matricula-detalle/<int:pk>/", MatriculaDetailView.as_view(),
         name="matricula-detalle"),
    path("matricula-page/<int:id>/",
         getDetalle, name="matricula-page"),
    path("matricula-like/",
         likeMatricula, name="matricula-like"),

    # todo sobre comentarios
    path("listado-comentario/",
         ListarComentariosPorMatricula, name="comentario-listar"),
    path("add-comentario/",
         AddComentario, name="comentario-add"),


]
