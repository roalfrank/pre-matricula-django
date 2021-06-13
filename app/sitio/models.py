from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group
from user.models import User
# Create your models here.


class Sitio_Web(models.Model):
    nombre = models.CharField(
        max_length=20, unique=True, verbose_name="Nombre del sitio")
    color_activo_menu = models.CharField(
        max_length=20, verbose_name="Color activo menu", default="#007bff")
    color_no_activo_menu = models.CharField(
        max_length=20, verbose_name="Color menu no activo", default="#11101070")
    color_sider = models.CharField(
        max_length=20, verbose_name="Color sider", default="#0087c3")
    color_footer = models.CharField(
        max_length=20, verbose_name="Color footer", default="#e8e8ea")
    color_header = models.CharField(
        max_length=20, verbose_name="Color header", default="#26bdef")
    color_text_body = models.CharField(
        max_length=20, verbose_name="Color Texto Body", default="rgb(9, 79, 102)")
    color_contenido = models.CharField(
        max_length=20, verbose_name="Color contenido", default="#fffff")
    color_fondo_inicio = models.CharField(
        max_length=20, verbose_name="Color Fondo Inicio", default="#26bdef")

    icono = models.CharField(max_length=20, null=True, blank=True,
                             verbose_name="Icono del sitio Barra Lateral")

    def __str__(self):
        return f"{self.nombre} - Icono: {self.icono}"


class TipoModulo(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre Modulo")
    icono = models.CharField(max_length=20, verbose_name="Icono")
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
