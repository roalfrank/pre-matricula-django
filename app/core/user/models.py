from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from config.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from core.preMatricula.models import Municipio


class Perfil(models.Model):
    ESTUDIANTE = 'ES'
    PROFESOR = 'PR'
    GESTOR = 'GE'
    INSTRUCTOR = 'IN'
    ADMIN = 'AD'
    CHOICE_TIPO = [(ESTUDIANTE, 'Estudiante'), (PROFESOR, 'Profesor'),
                   (GESTOR, "Gestor"), (INSTRUCTOR, 'Instructor'), (ADMIN, 'Admin')]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuario")
    ci = models.IntegerField(verbose_name="Carne Identidad", unique=True)
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    apellido1 = models.CharField(
        max_length=150, verbose_name="Apellido Paterno")
    apellido2 = models.CharField(
        max_length=150, verbose_name="Apellido Materno")
    direccion = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Dirección")
    municipio = models.ForeignKey(
        Municipio, on_delete=models.RESTRICT, verbose_name='Municipio')
    telefono = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Teléfono")
    correo = models.CharField(
        max_length=100, verbose_name="Correo", unique=True)
    avatar = models.ImageField(
        upload_to='users/avatar', default='default.png', verbose_name="Avatar", null=True, blank=True)
    tipo = models.CharField(
        max_length=2,
        choices=CHOICE_TIPO,
        default=ESTUDIANTE,
    )
    gestor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}{self.user.username}"

    def get_image(self):
        if self.avatar:
            return '{}{}'.format(MEDIA_URL, self.avatar)
        print('{}{}'.format(STATIC_URL, 'img/default.png'))
        return '{}{}'.format(STATIC_URL, 'img/default.png')

    def toJson(self):
        perfil = model_to_dict(self, exclude=['avatar'])
        perfil['provincia'] = self.municipio.provincia.pk
        return perfil

    def toJsonAdmin(self):
        perfil = {}
        perfil['usuario'] = self.user.pk
        perfil['nombre_usuario'] = self.get_nombre()
        perfil['username'] = self.user.username
        perfil['provincia'] = self.municipio.provincia.nombre
        perfil['ci'] = self.ci
        perfil['correo'] = self.correo
        perfil['image_user'] = self.get_image()
        return perfil

    def toJsonAdminAll(self):
        perfil = model_to_dict(self, exclude=['avatar'])
        perfil['usuario'] = self.user.pk
        perfil['nombre_usuario'] = self.get_nombre()
        perfil['username'] = self.user.username
        perfil['provincia'] = self.municipio.provincia.pk

        return perfil

    def get_nombre(self):
        return f'{self.nombre} {self.apellido1} {self.apellido2}'
