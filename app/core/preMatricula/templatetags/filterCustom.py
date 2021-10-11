from ..models import Comentario
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def comentario_hijos(request, comentario_papa):
    return Comentario.objects.filter(respuestaA=comentario_papa, aprobado=True).order_by('fecha_comentario',)


@register.simple_tag
def qr_crear(base_url, id):
    return str(base_url) + str(id)+'/'
