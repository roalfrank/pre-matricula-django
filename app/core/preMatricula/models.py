from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User

# Create your models here.


class Provincia(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name="Provincia", unique=True)

    def toJson(self):
        item = model_to_dict(self)
        item['cantmunicipio'] = self.municipio_set.all().count()
        return item

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Municipio")
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        item['nombre_provincia'] = self.provincia.__str__()
        return item


class Entidad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Entidad")
    telefono = models.CharField(max_length=8, verbose_name="Telefono")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    municipio = models.ForeignKey(
        Municipio, verbose_name="Municipio", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class JCP(models.Model):
    codigo_jcp = models.CharField(
        max_length=10, verbose_name="Codigo JCP", unique=True)
    entidad = models.OneToOneField(
        Entidad, verbose_name="Entidad", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.entidad} - ({self.codigo_jcp})"


class Region(models.Model):
    codigo_region = models.CharField(
        max_length=10, verbose_name="Código Región")
    nombre = models.CharField(max_length=50, verbose_name="Nombre Región")
    jcp = models.ForeignKey(
        JCP, verbose_name="Joven Club Provincial", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - ({self.codigo_region})"


class JCM(models.Model):
    codigo_jcm = models.CharField(
        max_length=10, verbose_name="Código Joven Club Municipal")
    entidad = models.OneToOneField(
        Entidad, on_delete=models.CASCADE, verbose_name="Entidad")
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, verbose_name="Región")

    def __str__(self):
        return f"{self.entidad.nombre}-({self.codigo_jcm})"


class JCB(models.Model):
    codigo_jcb = models.CharField(
        max_length=10, verbose_name="Código Joven Club")
    entidad = models.OneToOneField(
        Entidad, on_delete=models.CASCADE, verbose_name="Entidad")
    jcm = models.ForeignKey(
        JCM, on_delete=models.CASCADE, verbose_name="Joven Club Municipal")

    def __str__(self):
        return f"{self.entidad.nombre}-({self.codigo_jcb})"

# Todos sobre Instructor


class Cargo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del cargo')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class Instructor(models.Model):
    ci = models.IntegerField(
        verbose_name="Carnet Identidad", unique=True)
    usuario_siscae = models.CharField(
        max_length=50, verbose_name="Usuario del siscae", null=True, blank=False)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuario")
    jcb = models.ForeignKey(
        JCB, on_delete=models.RESTRICT, verbose_name='Joven Club')
    cargo = models.ForeignKey(
        Cargo, on_delete=models.RESTRICT, verbose_name='Cargo')

    def __str__(self):
        return self.usuario.perfil.nombre


class Maestro(models.Model):
    instructor = models.OneToOneField(
        Instructor, on_delete=models.CASCADE, verbose_name='Instructor')

    def __str__(self):
        return self.instructor

# todo sobre los estudiantes


class Ocupacion(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre Ocupación')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class Discapacidad(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre Discapacidad')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class CategoriaOcupacional(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre Categoría Ocupacional')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class CursoSiscae(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre Curso Siscae')

    def __str__(self):
        return self.nombre

# clase estudiantes


class Estudiante(models.Model):
    usuario_sisce = models.CharField(
        max_length=30, verbose_name='Usuario del siscae', null=True, blank=True)
    discapacidad = models.ForeignKey(
        Discapacidad, on_delete=models.RESTRICT, verbose_name='Discapacidad')
    categoria_ocupacional = models.ForeignKey(
        CategoriaOcupacional, on_delete=models.RESTRICT, verbose_name='Categoría Ocupacional')
    usuario = models.OneToOneField(
        User, on_delete=models.RESTRICT, verbose_name='usuario')
    ocupacion = models.ForeignKey(
        Ocupacion, on_delete=models.RESTRICT, verbose_name='Ocupación')

    def __str__(self):
        return self.usuario.perfil

    def toJson(self):
        return model_to_dict(self)


# mucho a mucho cursosiscae y estudiante

class EstudianteCursoSiscae(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    cursoSiscae = models.ForeignKey(
        CursoSiscae, on_delete=models.CASCADE, verbose_name='Curso Siscae')

    def __str__(self):
        return self.estudiante+'-' + self.cursoSiscae

# Gestor de JCM es un usuario


class Gestor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)
    jcm = models.ForeignKey(JCM, on_delete=models.RESTRICT,
                            verbose_name='Joven Club Municipal')

    def __str__(self):
        return self.usuario.perfil
# fin del gestor

# relacion Mucho a Mucho de Gesto y estudiante , un gestor puede crear muchas estudiantes


class GestorEstudiante(models.Model):
    gestor = models.ForeignKey(
        Gestor, on_delete=models.CASCADE, verbose_name='Gestor')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    fecha_creado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gestor} - {self.estudiante} - {self.fecha_creado}"

# clase para saber cual instructor crea a un estudiantes


class InstructorEstudiante(models.Model):
    instructor = models.ForeignKey(
        Gestor, on_delete=models.CASCADE, verbose_name='Gestor')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    fecha_creado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.instructor} - {self.estudiante} - {self.fecha_creado}"

# Todo relacionado a Cursos


class Curso(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre Curso')
    duracion = models.IntegerField(verbose_name='Duración en Horas')
    descripcion = models.TextField(verbose_name='Descripción del Curso')
    corto = models.BooleanField(verbose_name='Tipo de Curso')
    nextCurso = models.ForeignKey(
        'preMatricula.Curso', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        tipo_curso = "Largo"
        if self.corto:
            tipo_curso = "Corto"
        return f"{self.nombre}-{self.duracion} - {tipo_curso}"


# Modalidad de la preMatricula
class Modalidad(models.Model):
    nombre = models.CharField(
        max_length=50, verbose_name='Nombre de la Modalidad')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class EstadoMatricula(models.Model):
    nombre = models.CharField(
        max_length=50, verbose_name='Nombre del Estado Matricula')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class TipoGrupo(models.Model):
    nombre = models.CharField(
        max_length=50, verbose_name='Tipo de Grupo')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item
# clase Pre matricula Principal


class PreMatricula(models.Model):
    curso = models.ForeignKey(
        Curso, on_delete=models.RESTRICT, verbose_name='Curso')
    capacidad = models.IntegerField(
        verbose_name='Capacidad Total a Matricular')
    frecuencia = models.IntegerField(verbose_name='Frecuencia semanal')
    fecha_inicio = models.DateField(verbose_name='Fecha Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha Fin')
    estado = models.ForeignKey(
        EstadoMatricula, on_delete=models.RESTRICT, verbose_name='Estado de la PreMatricula')
    modalidad = models.ForeignKey(
        Modalidad, on_delete=models.RESTRICT, verbose_name='Modalidad')
    tipo_grupo = models.ForeignKey(
        TipoGrupo, on_delete=models.RESTRICT, verbose_name='Tipo Grupo')

    def __str__(self):
        return f"{self.curso}-(fecha={self.fecha_inicio}-{self.fecha_fin})-(estado={self.estado})"

# clase de relacion mucho a mucho con maestro


class PreMatriculaMaestro(models.Model):
    preMatricula = models.ForeignKey(
        PreMatricula, on_delete=models.CASCADE, verbose_name='Pre-Matricula')
    maestro = models.ForeignKey(
        Maestro, on_delete=models.CASCADE, verbose_name='Maestro')

    def __str__(self):
        return self.preMatricula + self.maestro

# clase para mucho a mucho con estudiantes y matriculas


class PreMatriculaEstudiante(models.Model):
    preMatricula = models.ForeignKey(
        PreMatricula, on_delete=models.CASCADE, verbose_name='Pre-Matricula')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    activo = models.BooleanField(
        verbose_name='El Estudiante ha sido chequeado')

    def __str__(self):
        return self.preMatricula + "- " + self.estudiante

# los estudiantes pueden comentar


class Comentario(models.Model):
    texto = models.TextField(verbose_name='Texto del comentario')
    fecha_comentario = models.DateField(
        auto_now=True, verbose_name='Fecha Creado')
    preMatricula = models.ForeignKey(
        PreMatricula, on_delete=models.CASCADE, verbose_name='Pre matricula')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')

    def __str__(self):
        return self.preMatricula + '-' + self.estudiante+'-'+self.fecha_comentario


# cursos de interes para los estudiantes

class CursoInteres(models.Model):
    frecuencia = models.IntegerField(verbose_name='Frecuencia')
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, verbose_name='Curso de Interes')
    municipio = models.ForeignKey(
        Municipio, on_delete=models.RESTRICT, verbose_name='Municipio')

    def __str__(self):
        return self.curso + '-' + self.municipio

# mucho a mucho con estudiantes y curso interes


class EstudianteCursoInteres(models.Model):
    cursoInteres = models.ForeignKey(
        CursoInteres, on_delete=models.CASCADE, verbose_name='Curso de Interes')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    sugerencia = models.CharField(max_length=200, verbose_name='Sugerencia')
    fecha_creado = models.DateField(verbose_name='fecha creado')

    def __str__(self):
        return self.cursoInteres + '-' + self.estudiante + '-' + self.fecha_creado
