import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_delete, m2m_changed, post_save
from config.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.db import models
import random
import qrcode
from datetime import datetime
import time


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
        return f"Region-{self.nombre}-({self.jcp.entidad.nombre})"

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
        return f"{self.entidad.nombre}"

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
        return f"{self.entidad.nombre}"

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
        return f"{self.usuario.username}-{self.usuario.perfil.nombre}"

    def toJson(self):
        instrutor = model_to_dict(self, fields=['usuario'])
        instrutor['nombre_usuario'] = self.usuario.perfil.get_nombre()
        instrutor['username'] = self.usuario.username
        instrutor['ci'] = self.usuario.perfil.ci
        instrutor['correo'] = self.usuario.perfil.correo
        instrutor['jcb'] = self.jcb.entidad.nombre
        instrutor['image_user'] = self.usuario.perfil.get_image()
        instrutor['tipo'] = self.usuario.perfil.tipo
        if self.usuario.perfil.tipo == 'PR':
            instrutor['icono'] = '<i class="fas fa-graduation-cap" aria-hidden="true"></i>'
        else:
            instrutor['icono'] = ''
        return instrutor

    def datosAllJson(self):
        instructor = model_to_dict(self)
        instructor.update(self.usuario.perfil.toJson())
        instructor['nombre_usuario'] = self.usuario.perfil.nombre
        instructor['username'] = self.usuario.username
        instructor['id_jcp'] = self.jcb.jcm.region.jcp.id
        instructor['id_region'] = self.jcb.jcm.region.id
        instructor['id_jcm'] = self.jcb.jcm.id
        return instructor


class Maestro(models.Model):
    instructor = models.OneToOneField(
        Instructor, on_delete=models.CASCADE, verbose_name='Instructor', primary_key=True)

    def __str__(self):
        return self.instructor.usuario.username

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
        estudiante = model_to_dict(self, fields=['usuario'])
        estudiante['nombre_usuario'] = self.usuario.perfil.get_nombre()
        estudiante['username'] = self.usuario.username
        estudiante['provincia'] = self.usuario.perfil.municipio.provincia.nombre
        estudiante['ci'] = self.usuario.perfil.ci
        estudiante['correo'] = self.usuario.perfil.correo
        estudiante['image_user'] = self.usuario.perfil.get_image()
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
        User, on_delete=models.CASCADE, primary_key=True)
    jcm = models.ForeignKey(JCM, on_delete=models.CASCADE,
                            verbose_name='Joven Club Municipal')

    def __str__(self):
        return self.usuario.perfil.get_nombre()

    def toJson(self):
        gestor = model_to_dict(self, fields=['usuario'])
        gestor['id_gestor'] = self.pk
        gestor['nombre_usuario'] = self.usuario.perfil.get_nombre()
        gestor['username'] = self.usuario.username
        gestor['provincia'] = self.usuario.perfil.municipio.provincia.nombre
        gestor['ci'] = self.usuario.perfil.ci
        gestor['correo'] = self.usuario.perfil.correo
        gestor['jcm'] = self.jcm.entidad.nombre
        print('jcm', self.jcm.entidad.nombre)
        gestor['image_user'] = self.usuario.perfil.get_image()
        gestor['tipo'] = self.usuario.perfil.tipo
        if self.usuario.perfil.tipo == 'PR':
            gestor['icono'] = '<i class="fas fa-graduation-cap" aria-hidden="true"></i>'
        else:
            gestor['icono'] = ''
        return gestor

    def datosAllJson(self):
        gestor = model_to_dict(self)
        gestor.update(self.usuario.perfil.toJson())
        gestor['nombre_usuario'] = self.usuario.perfil.nombre
        gestor['username'] = self.usuario.username
        gestor['id_jcp'] = self.jcm.region.jcp.id
        gestor['id_region'] = self.jcm.region.id
        gestor['id_jcm'] = self.jcm.id
        return gestor
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
    HORAS24 = '24'
    HORAS36 = '36'
    HORAS64 = '64'
    CHOICE_TIPO = [(HORAS24, '24 horas'), (HORAS36, '36 horas'),
                   (HORAS64, "64 horas")]
    nombre = models.CharField(max_length=100, verbose_name='Nombre Curso')
    duracion = models.CharField(
        verbose_name='Duración en Horas', choices=CHOICE_TIPO, default=HORAS24, max_length=2)
    descripcion = models.TextField(verbose_name='Descripción del Curso')
    nextCurso = models.ForeignKey(
        'preMatricula.Curso', on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(
        upload_to='curso/foto', default='curso_default.png', verbose_name="Foto", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}-{self.duracion}"

    def get_foto(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        return '{}{}'.format(STATIC_URL, 'img/curso_default.png')

    def getNext(self):
        if self.nextCurso:
            curso = self.nextCurso.nombre + \
                "(" + self.nextCurso.duracion + "h)"
            return curso
        else:
            curso = 'No tiene'
            return curso

    def toJson(self):
        curso = model_to_dict(self, exclude=['foto'])
        curso['foto_url'] = self.get_foto()
        if len(self.descripcion) > 100:
            curso['descripcion_corta'] = self.descripcion[0:100]
            curso['descripcion_corta'] += ' (....)'
        else:
            curso['descripcion_corta'] = self.descripcion
        curso['nextCurso_nombre'] = self.getNext()

        return curso


# clase Pre matricula Principal
class PreMatricula(models.Model):
    ABIERTO = 'AB'
    CERRADO = 'CE'
    PROCESO = 'PR'
    CHOICE_ESTADO = [(ABIERTO, 'abierto'), (CERRADO, 'cerrado'),
                     (PROCESO, "proceso")]
    PRESENCIAL = 'PR'
    SEMIPRESENCIA = 'SE'
    CHOICE_MODALIDAD = [(PRESENCIAL, 'presencial'),
                        (SEMIPRESENCIA, 'semi-presencial')]
    curso = models.ForeignKey(
        Curso, on_delete=models.RESTRICT, verbose_name='Curso')
    jcb = models.ForeignKey(
        JCB, on_delete=models.CASCADE, verbose_name='Joven Club', blank=True, null=True, default=None)
    capacidad = models.IntegerField(
        verbose_name='Capacidad Total a Matricular')
    frecuencia = models.IntegerField(verbose_name='Frecuencia semanal')
    fecha_inicio = models.DateField(verbose_name='Fecha Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha Fin')
    estado = models.CharField(
        verbose_name='Estado', choices=CHOICE_ESTADO, default=ABIERTO, max_length=2)
    modalidad = models.CharField(
        verbose_name='Modalidad', choices=CHOICE_MODALIDAD, default=PRESENCIAL, max_length=2)
    likes = models.ManyToManyField(
        User, related_name='likes', blank=True, default=None)
    fecha_creado = models.DateTimeField(auto_now=True)

    def toJson(self):
        jsonMatricula = model_to_dict(
            self, exclude=['curso', 'jcb', 'likes', 'modalidad', 'fecha_inicio', 'fecha_fin', 'estado'])
        jsonMatricula['estado'] = self.get_estado_display()
        if self.estado == 'CE':
            jsonMatricula['estado_color'] = 'danger'
        elif self.estado == 'AB':
            jsonMatricula['estado_color'] = 'success'
        else:
            jsonMatricula['estado_color'] = 'warning'
        jsonMatricula['fecha_inicio'] = self.fecha_inicio.strftime(
            '%d/%m/%Y')
        jsonMatricula['fecha_fin'] = self.fecha_fin.strftime('%d/%m/%Y')
        jsonMatricula['nombre_curso'] = self.curso.nombre
        jsonMatricula['horas'] = self.curso.get_duracion_display()
        jsonMatricula['modalidad'] = self.get_modalidad_display()
        nextCurso_instancia = self.curso.nextCurso
        try:
            matricula_nexCurso = PreMatricula.objects.get(
                curso=nextCurso_instancia)
            jsonMatricula['nextCurso'] = matricula_nexCurso.curso.__str__()
            jsonMatricula['nextCurso_id'] = matricula_nexCurso.pk
        except:
            jsonMatricula['nextCurso'] = 'No tiene'
            jsonMatricula['nextCurso_id'] = 'no'
        jsonMatricula['foto_url'] = self.curso.get_foto()
        jsonMatricula['jcb'] = self.jcb.entidad.nombre
        jsonMatricula['jcm'] = self.jcb.jcm.entidad.nombre
        jsonMatricula['jcp'] = self.jcb.jcm.region.jcp.entidad.nombre
        jsonMatricula['cantidad_estudiante'] = self.cantidadEstudiante()
        if len(self.curso.descripcion) > 100:
            jsonMatricula['descripcion_curso'] = self.curso.descripcion[0:100]
            jsonMatricula['descripcion_curso'] += ' (....)'
        else:
            jsonMatricula['descripcion_curso'] = self.curso.descripcion
        return jsonMatricula

    def toJsonForm(self):
        jsonMatricula = model_to_dict(
            self, exclude=['curso', 'jcb', 'tipo_grupo', 'likes', 'modalidad', 'fecha_inicio', 'fecha_fin', 'estado'])
        jsonMatricula['estado'] = self.get_estado_display()
        jsonMatricula['fecha_inicio'] = self.fecha_inicio.strftime(
            '%d/%m/%Y')
        jsonMatricula['fecha_fin'] = self.fecha_fin.strftime('%d/%m/%Y')
        jsonMatricula['nombre_curso'] = self.curso.nombre
        jsonMatricula['descripcion_curso'] = self.curso.descripcion
        jsonMatricula['horas'] = self.tipo_grupo.nombre
        jsonMatricula['nextCurso'] = self.nextCurso.__str__()
        return jsonMatricula

    def __str__(self):
        return f"{self.curso}-(fecha={self.fecha_inicio}-{self.fecha_fin})-(estado={self.get_estado_display()})"

    def numero_comentario(self):
        return Comentario.objects.filter(preMatricula=self).count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('prematricula:matricula-page')

    def cantidadEstudiante(self):
        estudiantes = PreMatriculaEstudiante.objects.filter(
            preMatricula=self).count()
        return estudiantes

    def esNuevo(self):
        fecha_now = datetime.now()
        print("fecha actual", fecha_now)
        print("fecha crado", self.fecha_creado.replace(tzinfo=None))
        resta = fecha_now - self.fecha_creado.replace(tzinfo=None)
        if resta.days < 7:
            return True
        return False

    def actualizad_estado(self):
        cantidad_estudiante = self.cantidadEstudiante()
        if self.cantidadEstudiante() < self.capacidad:
            self.estado = self.ABIERTO
        elif cantidad_estudiante == self.capacidad:
            self.estado = self.CERRADO
        else:
            self.estado = self.PROCESO
        self.save()

    def listadoEstudiante(self):
        estudiantes = PreMatriculaEstudiante.objects.filter(
            preMatricula=self)
        return estudiantes

# singal para cuando se edita una matricula


# @receiver(post_save, sender=PreMatricula)
# def change_matricula(sender, instance, created, **kwargs):
#     print('datos update', kwargs)
#     if not created:
#         print('dentro de post_save no creado')
#         jsonMatricula = instance.toJson()
#         # conectamos al websocket de like
#         print(jsonMatricula)
#         channel_layer = get_channel_layer()
#         nombre_grupo = 'update_matricula_' + str(instance.pk)
#         # lanzamiento de mensaje a websocket
#         async_to_sync(channel_layer.group_send)(nombre_grupo, {
#             'type': 'send_message',
#             'matricula': jsonMatricula
#         })

# signal para cuando se cambia el like de la matricula y asi lanzar un mensaje al websocket de like
@receiver(m2m_changed, sender=PreMatricula.likes.through)
def like_change(sender, instance, action, **kwargs):
    contador_like = instance.likes.all().count()
    # conectamos al websocket de like
    channel_layer = get_channel_layer()
    nombre_grupo = 'like_matricula_' + str(instance.pk)
    # lanzamiento de mensaje a websocket
    async_to_sync(channel_layer.group_send)(nombre_grupo, {
        'type': 'send_message',
        'contador_like': contador_like
    })


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
        verbose_name='El Estudiante ha sido chequeado', default=False)

    def __str__(self):
        return self.preMatricula.curso.nombre + "- " + self.estudiante.usuario.perfil.nombre

    def save(self, *args, **kwargs):
        cantidad_estudiante = self.preMatricula.cantidadEstudiante()
        if cantidad_estudiante >= self.preMatricula.capacidad:
            return False

        # conectamos al websocket de de update matricula
        channel_layer = get_channel_layer()
        nombre_grupo = 'update_matricula_' + str(self.preMatricula.pk)
        cant_mas_uno = cantidad_estudiante + 1
        if cant_mas_uno == self.preMatricula.capacidad:
            self.preMatricula.estado = 'CE'
            self.preMatricula.save()
            # lanzamiento de mensaje a websocket de update matricula
            async_to_sync(channel_layer.group_send)(nombre_grupo, {
                'type': 'send_message',
                'evento': 'cerrado',
                'datos': {
                    'cant_estudiante': cant_mas_uno,
                    'estado': self.preMatricula.get_estado_display()
                }
            })
        else:
            # lanzamiento sin el estado
            async_to_sync(channel_layer.group_send)(nombre_grupo, {
                'type': 'send_message',
                'evento': 'no cerrado',
                'datos': {
                        'cant_estudiante': cant_mas_uno,
                        'estado': self.preMatricula.get_estado_display()
                }
            })
        return super().save(self, *args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     matricula = self.preMatricula
    #     print('matricula se borra un estudiante', matricula)
    #     object_delete = super().delete(self, *args, **kwargs)
    #     print('matricula borro un estudiante', matricula)
    #     matricula.actualizad_estado()
    #     return object_delete


@receiver(post_delete, sender=PreMatriculaEstudiante)
def actualizarMatricula(sender, instance, **kwargs):
    # conectamos al websocket de de update matricula
    channel_layer = get_channel_layer()
    nombre_grupo = 'update_matricula_' + str(instance.preMatricula.pk)
    instance.preMatricula.actualizad_estado()
    cant_estudiante = instance.preMatricula.cantidadEstudiante()
    async_to_sync(channel_layer.group_send)(nombre_grupo, {
        'type': 'send_message',
        'evento': 'no cerrado',
        'datos': {
            'cant_estudiante': cant_estudiante,
            'estado': instance.preMatricula.get_estado_display()
        }
    })

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
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.preMatricula.curso.nombre}-{self.usuario.perfil.nombre}-{self.fecha_comentario}'


@receiver(post_save, sender=Comentario)
def comentarioADD(sender, instance, created, **kwargs):
    print('comentario nuevo o update ', instance)
    cantidad_comentario = Comentario.objects.filter(
        preMatricula=instance.preMatricula).count()
    context = {}
    datos = {}
    datos['id_comentario'] = instance.pk
    datos['cantidad_comentario'] = cantidad_comentario
    context['type'] = 'send_message'
    # conectamos al websocket de de comentario_matricula_
    channel_layer = get_channel_layer()
    nombre_grupo = 'comentario_matricula_' + str(instance.preMatricula.pk)
    hijo = False
    if created:
        if instance.aprobado:

            if instance.respuestaA:
                hijo = True
                datos['id_comentario_a'] = instance.respuestaA.pk

            context['evento'] = 'new'
            datos['hijo'] = hijo
            context['datos'] = datos
        else:
            context['evento'] = 'new_no_aprobado'
    else:
        if instance.aprobado:
            if instance.respuestaA:
                hijo = True
                datos['id_comentario_a'] = instance.respuestaA.pk
            context['evento'] = 'update'
            datos['hijo'] = hijo
            context['datos'] = datos
        else:
            context['evento'] = 'update_no_aprobado'
    async_to_sync(channel_layer.group_send)(nombre_grupo, context)

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
