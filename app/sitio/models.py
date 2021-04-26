from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group
from user.models import User
# Create your models here.


class Sitio_Web(models.Model):
    nombre = models.CharField(
        max_length=20, unique=True, verbose_name="Nombre del sitio")
    color_activo_menu = models.CharField(
        max_length=20, verbose_name="Color activo menu", default="#2d0604c7")
    color_no_activo_menu = models.CharField(
        max_length=20, verbose_name="Color menu no activo", default="#11101070")
    color_sider = models.CharField(
        max_length=20, verbose_name="Color sider", default="#343a40")
    color_footer = models.CharField(
        max_length=20, verbose_name="Color footer", default="#343a40")
    color_header = models.CharField(
        max_length=20, verbose_name="Color header", default="#343a40")
    color_text_body = models.CharField(
        max_length=20, verbose_name="Color Texto Body", default="rgb(9, 79, 102)")
    color_contenido = models.CharField(
        max_length=20, verbose_name="Color contenido", default="rgb(9, 79, 102)")
    color_fondo_inicio = models.CharField(
        max_length=20, verbose_name="Color Fondo Inicio", default="rgb(9, 79, 102)")

    icono = models.CharField(max_length=20, null=True, blank=True,
                             verbose_name="Icono del sitio Barra Lateral")

    def __str__(self):
        return f"{self.nombre} - Icono: {self.icono}"


class TipoModulo(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre Modulo")
    icono = models.CharField(max_length=20, unique=True, verbose_name="Icono")
    padre_tipo = models.ForeignKey('TipoModulo', on_delete=models.CASCADE,
                                   verbose_name="Padre", related_name="padre", null=True, blank=True)
    estado = models.BooleanField()

    def __str__(self):
        return f"{self.nombre} - {self.estado} "


class Modulo(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre del menú")
    icono = models.CharField(max_length=20, verbose_name="Icono del Menú")
    tipo = models.ForeignKey(TipoModulo, on_delete=models.CASCADE,
                             verbose_name="Tipo de Módulo", related_name="modulos")
    url_path = models.CharField(
        max_length=50, verbose_name="Url", default="sitio:listar")
    estado = models.BooleanField()
    grupos = models.ManyToManyField(
        Group, verbose_name="Grupos")

    def __str__(self):
        return f"{self.nombre} - {self.tipo.nombre}"

    def get_url(self):
        try:
            url_ok = reverse(self.url_path)
            return url_ok
        except:
            return "#"

# modelos de la entidad


class Jcc(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre Jcc')
    endidad_lugar = models.OneToOneField(
        to="sitio.Entidad", on_delete=models.SET_NULL, null=True, blank=True)
    director = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Entidad(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre Entidad')
    direccion = models.CharField(
        max_length=300, verbose_name="Direccion", null=True, blank=True)
    telefono = models.CharField(max_length=8, verbose_name="Telefono")
    from_jcc = models.ForeignKey(Jcc, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
