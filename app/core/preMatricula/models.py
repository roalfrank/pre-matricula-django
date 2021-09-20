import time
from django.db import models
from django.db.models.fields import BigIntegerField
from django.forms import model_to_dict
from django.contrib.auth.models import User
from config.settings import MEDIA_URL, STATIC_URL

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
    telefono = models.CharField(
        max_length=8, verbose_name="Telefono", null=True, blank=True)
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    municipio = models.ForeignKey(
        Municipio, verbose_name="Municipio", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        item['nombre_provincia'] = self.municipio.provincia.nombre
        item['provincia'] = self.municipio.provincia.pk
        item['nombre_municipio'] = self.municipio.nombre
        return item


class JCP(models.Model):
    codigo_jcp = models.CharField(
        max_length=10, verbose_name="Codigo JCP", unique=True)
    entidad = models.OneToOneField(
        Entidad, verbose_name="Entidad", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.entidad} - ({self.codigo_jcp})"

    def toJson(self):
        item = self.entidad.toJson()
        item['id_jcp'] = self.pk
        item['codigo_jcp'] = self.codigo_jcp
        return item


class Region(models.Model):
    codigo_region = models.CharField(
        max_length=10, verbose_name="Código Región", unique=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre Región")
    jcp = models.ForeignKey(
        JCP, verbose_name="Joven Club Provincial", on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.jcp.entidad.nombre})-{self.nombre}- ({self.codigo_region})"

    def toJson(self):
        item = model_to_dict(self)
        item['nombre_jcp'] = self.jcp.entidad.nombre
        return item


class JCM(models.Model):
    codigo_jcm = models.CharField(
        max_length=10, verbose_name="Código Joven Club Municipal", unique=True)
    entidad = models.OneToOneField(
        Entidad, on_delete=models.CASCADE, verbose_name="Entidad")
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, verbose_name="Región")

    def __str__(self):
        return f"{self.entidad.nombre}-({self.codigo_jcm})"

    def toJson(self):
        item = self.entidad.toJson()
        item['id_jcm'] = self.pk
        item['codigo_jcm'] = self.codigo_jcm
        item['region'] = self.region.pk
        item['nombre_region'] = self.region.nombre
        return item


class JCB(models.Model):
    codigo_jcb = models.CharField(
        max_length=10, verbose_name="Código Joven Club", unique=True)
    entidad = models.OneToOneField(
        Entidad, on_delete=models.CASCADE, verbose_name="Entidad")
    jcm = models.ForeignKey(
        JCM, on_delete=models.CASCADE, verbose_name="Joven Club Municipal")

    def __str__(self):
        return f"{self.entidad.nombre}-({self.codigo_jcb})"

    def toJson(self):
        item = self.entidad.toJson()
        item['id_jcb'] = self.pk
        item['codigo_jcb'] = self.codigo_jcb
        item['jcm'] = self.jcm.pk
        item['nombre_jcm'] = self.jcm.entidad.nombre
        return item

# Todos sobre Instructor


class Cargo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del cargo')

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class Instructor(models.Model):

    usuario_siscae = models.CharField(
        max_length=50, verbose_name="Usuario del siscae", null=True, blank=False)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuario",  primary_key=True)
    jcb = models.ForeignKey(
        JCB, on_delete=models.RESTRICT, verbose_name='Joven Club')
    cargo = models.ForeignKey(
        Cargo, on_delete=models.RESTRICT, verbose_name='Cargo')

    def __str__(self):
        return self.usuario.perfil.nombre


class Maestro(models.Model):
    instructor = models.OneToOneField(
        Instructor, on_delete=models.CASCADE, verbose_name='Instructor', primary_key=True)

    def __str__(self):
        return self.instructor.usuario.perfil.nombre

    def get_nombre(self):
        return f"{self.instructor.usuario.perfil.nombre} {self.instructor.usuario.perfil.apellido1} {self.instructor.usuario.perfil.apellido2}"

# todo sobre los estudiantes


class Ocupacion(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre Ocupación', unique=True)

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class Discapacidad(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre Discapacidad', unique=True)

    def __str__(self):
        return self.nombre

    def toJson(self):
        item = model_to_dict(self)
        return item


class CategoriaOcupacional(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre Categoría Ocupacional', unique=True)

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
        User, on_delete=models.CASCADE, verbose_name='usuario', primary_key=True)
    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name='Creado por', null=True, blank=True, default=None, related_name="creado_por")
    ocupacion = models.ForeignKey(
        Ocupacion, on_delete=models.RESTRICT, verbose_name='Ocupación')

    def __str__(self):
        return self.usuario.username

    def toJson(self):
        tiempo_inicial = time.time()
        #estudiante = {}
        estudiante = model_to_dict(self, fields=['usuario'])
        estudiante['nombre_usuario'] = self.usuario.perfil.nombre
        estudiante['username'] = self.usuario.username
        estudiante['provincia'] = self.usuario.perfil.municipio.provincia.nombre
        estudiante['ci'] = self.usuario.perfil.ci
        estudiante['correo'] = self.usuario.perfil.correo
        tiempo_final = time.time()
        tiempo = tiempo_final - tiempo_inicial
        print(f'Tiempo demorado estudiante:{tiempo}')
        return estudiante

    def datosAllJson(self):
        estudiante = model_to_dict(self)
        estudiante.update(self.usuario.perfil.toJson())
        estudiante['nombre_usuario'] = self.usuario.perfil.nombre
        estudiante['username'] = self.usuario.username
        return estudiante


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
    usuario = models.OneToOneField(
        User, on_delete=models.RESTRICT, primary_key=True)
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
        Instructor, on_delete=models.CASCADE, verbose_name='Gestor')
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
    corto = models.BooleanField(verbose_name='corto')
    nextCurso = models.ForeignKey(
        'preMatricula.Curso', on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(
        upload_to='curso/foto', default='curso_default.png', verbose_name="Foto", null=True, blank=True)

    def __str__(self):
        tipo_curso = "Largo"
        if self.corto:
            tipo_curso = "Corto"
        return f"{self.nombre}-{self.duracion} - {tipo_curso}"

    def get_foto(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        return '{}{}'.format(STATIC_URL, 'img/curso_default.png')


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
    likes = models.ManyToManyField(
        User, related_name='likes', blank=True, default=None)
    like_count = BigIntegerField(default=0)

    def __str__(self):
        return f"{self.curso}-(fecha={self.fecha_inicio}-{self.fecha_fin})-(estado={self.estado})"

    def numero_comentario(self):
        return Comentario.objects.filter(preMatricula=self).count()

# clase de relacion mucho a mucho con maestro


class PreMatriculaMaestro(models.Model):
    preMatricula = models.ForeignKey(
        PreMatricula, on_delete=models.CASCADE, verbose_name='Pre-Matricula')
    maestro = models.ForeignKey(
        Maestro, on_delete=models.CASCADE, verbose_name='Maestro')

    def __str__(self):
        return self.preMatricula.curso.nombre + self.maestro.instructor.usuario.perfil.nombre

# clase para mucho a mucho con estudiantes y matriculas


class PreMatriculaEstudiante(models.Model):
    preMatricula = models.ForeignKey(
        PreMatricula, on_delete=models.CASCADE, verbose_name='Pre-Matricula')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    activo = models.BooleanField(
        verbose_name='El Estudiante ha sido chequeado')

    # def __str__(self):
    #     return self.preMatricula.curso.nombre + "- " + self.estudiante.usuario.perfil.nombre

# los estudiantes pueden comentar


class Comentario(models.Model):
    texto = models.TextField(verbose_name='Texto del comentario')
    fecha_comentario = models.DateTimeField(
        auto_now=True, verbose_name='Fecha Creado')
    preMatricula = models.ForeignKey(
        PreMatricula, on_delete=models.CASCADE, verbose_name='Pre matricula')
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuario')
    respuestaA = models.ForeignKey(
        'preMatricula.Comentario', on_delete=models.CASCADE, verbose_name='Respuesta a', null=True, blank=True, default=None)
    aprobado = models.BooleanField(default=True)

    def __str__(self):
        return self.preMatricula.curso.nombre + '-' + self.usuario.perfil.nombre


# cursos de interes para los estudiantes

class CursoInteres(models.Model):
    frecuencia = models.IntegerField(verbose_name='Frecuencia')
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, verbose_name='Curso de Interes')
    municipio = models.ForeignKey(
        Municipio, on_delete=models.RESTRICT, verbose_name='Municipio')

    def __str__(self):
        return self.curso.nombre + '-' + self.municipio.nombre

# mucho a mucho con estudiantes y curso interes


class EstudianteCursoInteres(models.Model):
    cursoInteres = models.ForeignKey(
        CursoInteres, on_delete=models.CASCADE, verbose_name='Curso de Interes')

    sugerencia = models.CharField(max_length=200, verbose_name='Sugerencia')
    fecha_creado = models.DateField(verbose_name='fecha creado')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')

    def __str__(self):
        return self.cursoInteres.curso.nombre + '-' + self.estudiante.usuario.perfil.nombre
