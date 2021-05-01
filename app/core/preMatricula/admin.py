from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Entidad)
admin.site.register(Region)
admin.site.register(JCP)
admin.site.register(JCM)
admin.site.register(JCB)
admin.site.register(Municipio)
admin.site.register(Provincia)
admin.site.register(Cargo)
admin.site.register(Curso)
admin.site.register(CursoInteres)
admin.site.register(CursoSiscae)
admin.site.register(CategoriaOcupacional)
admin.site.register(Estudiante)
admin.site.register(EstudianteCursoInteres)
admin.site.register(EstadoMatricula)
admin.site.register(Comentario)
admin.site.register(PreMatricula)
admin.site.register(PreMatriculaEstudiante)
admin.site.register(PreMatriculaMaestro)
admin.site.register(TipoGrupo)
admin.site.register(Modalidad)
admin.site.register(Maestro)
admin.site.register(Instructor)
admin.site.register(InstructorEstudiante)
admin.site.register(Ocupacion)
admin.site.register(Discapacidad)
admin.site.register(Gestor)
admin.site.register(GestorEstudiante)
admin.site.register(EstudianteCursoSiscae)

