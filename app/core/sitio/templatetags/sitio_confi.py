from django import template
from ..models import Sitio_Web, Modulo

register = template.Library()


@register.simple_tag
def sitio_web():
    try:
        sitio = Sitio_Web.objects.all()[0]
        return sitio
    except:
        return None


@register.simple_tag
def activo_inicio(request):
    try:
        url_path = request.path
        lista_url = url_path.split('/')
        if len(lista_url) == 2:
            return 'active'
        return ''
    except:
        return ''


def get_modulo(url, ultimo):
    try:
        modulos = Modulo.objects.all()
        for m in modulos:
            if m.get_url() == url:
                return m.nombre
        if ultimo == 1:
            nombre = url.split('/')
            return nombre[-2].capitalize()
        else:
            return 'no'
    except:
        return 'no'


@register.simple_tag
def sitio_map(request):
    url_path = request.path
    lista_url = url_path.split('/')
    lista_url = lista_url[1:-1]
    data_map = []
    nombre_ultimo = get_modulo(url_path, 1)
    cant = len(lista_url)
    if cant == 1:
        data_map.append({"url": url_path, "nombre": lista_url[0]})
        ultimo = {"url": url_path, "nombre": nombre_ultimo}
        return {"cantidad": 1, "data": data_map, "ultimo": ultimo}
    elif cant == 0:
        return {"cantidad": 0}
    ultimo = {"url": url_path, "nombre": nombre_ultimo}
    url_aux = "/"
    for element in lista_url:
        url_aux += element + "/"
        nombre = get_modulo(url_aux, 0)
        if nombre == 'no':
            continue
        data_map.append({"url": url_aux, "nombre": nombre})
    return {"cantidad": 2, "data": data_map[:-1], "ultimo": ultimo}
