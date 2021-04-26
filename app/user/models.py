from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL, STATIC_URL

CHOICES_CARGO = [
    ("c", "Instructor C"),
    ("d", "Instructor D"),
    ("e", "Económico"),
    ("d", "Director")

]


class User(AbstractUser):
    entidad = models.ForeignKey(
        to='sitio.Entidad', on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(
        max_length=15, choices=CHOICES_CARGO, null=True, blank=True)

    def __str__(self):
        return f"{self.username}"


class Etiqueta_Domina(models.Model):
    nombre = models.CharField(
        max_length=40, verbose_name="Etiqueta para Domina")

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuario")
    avatar = models.ImageField(
        upload_to='users/avatar', verbose_name="Avatar")
    estudios = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Estudios")
    direccion = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Dirección")
    telefono = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Teléfono")
    notas = models.CharField(max_length=200, null=True,
                             blank=True, verbose_name="Notas")
    domina = models.ManyToManyField(Etiqueta_Domina)

    def __str__(self):
        return f"{self.user.username}"

    def get_image(self):
        if self.avatar:
            return '{}{}'.format(MEDIA_URL, self.avatar)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
