from django.urls import path
# importaciones para entidades
from core.preMatricula.logica.tbentidad.Provincia.views import ProvinciaListView, buscarMunicipios
from core.preMatricula.logica.tbentidad.entidadMunicipio.views import MunicipioView
from core.preMatricula.logica.tbentidad.entidadJcp.views import JcpView
from core.preMatricula.logica.tbentidad.entidadRegion.views import RegionListView, buscarRegion
from core.preMatricula.logica.tbentidad.entidadJcm.views import JcmView, buscarJCM
from core.preMatricula.logica.tbentidad.entidadJcb.views import JcbView, buscarJCB
# importaciones para instructores
from core.preMatricula.logica.instructor.cargoinstructor.views import CargoInstructorView
from core.preMatricula.logica.instructor.instructor.views import InstructorView, InstructorDetailView, InstructorDetailCargarFormAddView, buscarInstructor
# importaciones para gestores
from core.preMatricula.logica.gestor.gestor.views import GestorView, deleteGestorTrabajador, GestorDetailView, GestorDetailCargarFormAddView, GestorCargarFormAddTrabajadorView, buscarGestor, buscarTrabajador
# importaciones para estudiantes
from core.preMatricula.logica.estudiante.estudianteocupacion.views import OcupacionEstudianteView
from core.preMatricula.logica.estudiante.estudiantediscapacidad.views import DiscapacidadEstudianteView
from core.preMatricula.logica.estudiante.estudianteCatOcupacional.views import CategoriaOcupacionalEstudianteView
from core.preMatricula.logica.estudiante.estudiante.views import EstudianteView, EstudianteDetailView, EstudianteDetailCargarFormAddView
# importaciones para cursos
from core.preMatricula.logica.curso.curso.views import CursoView, CursoDetailView, CursoDetailCargarFormAddView, buscarCurso
from core.preMatricula.logica.curso.cursoTipo.views import TipoCursoView
# importaciones para matricula
from core.preMatricula.logica.matricula.matriculaModalidad.views import ModalidadMatriculaView
from core.preMatricula.logica.matricula.matriculaEstado.views import EstadoMatriculaView
from core.preMatricula.logica.matricula.matricula.views import MatriculaDetailView, likeMatricula, addEstudianteMatricula, listar_estudiante_matriculado_carrucel, getDetallePageMatricula, estudianteEstaMatriculado

# importaciones para admin
from core.preMatricula.logica.admin.admin.views import AdminView, AdminDetailView, AdminDetailCargarFormAddView, buscarAdmin

# importaciones de comentarios
from core.preMatricula.logica.comentario.views import ListarComentariosPorMatricula, AddComentario, rowComentario, rowComentarioHijo

# importaciones para los metodos del sistema globales
from .views import buscarEstudiante, pdf_estudiantes, uniqueUser

# importaciones de las pruebas


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
    path("entidad-jcb/buscar/", buscarJCB, name="entidad-jcb-buscar"),
    path("entidad-jcm/buscar/", buscarJCM, name="entidad-jcm-buscar"),
    path("entidad-region/buscar/", buscarRegion, name="entidad-region-buscar"),

    # --- Istructor enlaces -----
    path("cargo-instructor/", CargoInstructorView.as_view(),
         name="cargo-instructor"),
    path("instructor/", InstructorView.as_view(), name="instructor"),
    path("instructor-detail/<int:pk>/",
         InstructorDetailView.as_view(), name="instructor-detail"),
    path("instructor-add-form/",
         InstructorDetailCargarFormAddView.as_view(), name="instructor-add-form"),
    path("instructor-datos/", buscarInstructor, name="instructor-datos"),
    path("buscar-instructores/", buscarTrabajador, name="buscar-instructores"),


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
    # ----Gestor enlaces---------
    path("gestor/", GestorView.as_view(), name="gestor"),
    path("gestor-detail/<int:pk>/",
         GestorDetailView.as_view(), name="gestor-detail"),
    path("gestor-add-form/",
         GestorDetailCargarFormAddView.as_view(), name="gestor-add-form"),
    path("gestor-add-form-trabajador/",
         GestorCargarFormAddTrabajadorView.as_view(), name="gestor-add-form-trabajador"),
    path("gestor-datos/", buscarGestor, name="gestor-datos"),
    path("gestor-delete-trabajador/", deleteGestorTrabajador,
         name="gestor-delete-trabajador"),

    # -----todo relacionados con los admin
    path("admin/", AdminView.as_view(), name="admin"),
    path("admin-detail/<int:pk>/",
         AdminDetailView.as_view(), name="admin-detail"),
    path("admin-add-form/",
         AdminDetailCargarFormAddView.as_view(), name="admin-add-form"),
    path("admin-datos/", buscarAdmin, name="admin-datos"),

    # --- Todo relacionado con los cursos
    path("curso-tipo/", TipoCursoView.as_view(),
         name="curso-tipo"),
    path("curso/", CursoView.as_view(), name="curso"),
    path("curso-detail/<int:pk>/",
         CursoDetailView.as_view(), name="curso-detail"),
    path("curso-add-form/",
         CursoDetailCargarFormAddView.as_view(), name="curso-add-form"),
    path("curso-datos/", buscarCurso, name="curso-datos"),


    # --- Todo relacionado con los matricula
    path("matricula-modalidad/", ModalidadMatriculaView.as_view(),
         name="matricula-modalidad"),
    path("matricula-estado/", EstadoMatriculaView.as_view(),
         name="matricula-estado"),
    path("matricula-detalle/<int:pk>/", MatriculaDetailView.as_view(),
         name="matricula-detalle"),
    path("matricula-pagina/<int:id>/",
         getDetallePageMatricula, name="matricula-page"),
    path("matricula-like/",
         likeMatricula, name="matricula-like"),
    path("matricula-estudiante-add/",
         addEstudianteMatricula, name="matricula-estudiante-add"),
    path("matricula-estudiante-listar-carrucel/<int:id_matricula>",
         listar_estudiante_matriculado_carrucel, name="matricula-estudiante-listar-carrucel"),
    path("matricula-estudiante-esta/",
         estudianteEstaMatriculado, name="matricula-estudiante-esta"),

    # todo sobre comentarios
    path("listado-comentario/",
         ListarComentariosPorMatricula, name="comentario-listar"),
    path("add-comentario/",
         AddComentario, name="comentario-add"),
    path("row-comentario/",
         rowComentario, name="row-comentario"),
    path("row-comentario-hijo/",
         rowComentarioHijo, name="row-comentario-hijo"),

    # url de pruebas
    # generar pdf de prueba
    path('generar-pdf/', pdf_estudiantes, name='generar-pdf'),

]
