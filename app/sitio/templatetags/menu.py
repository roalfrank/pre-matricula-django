from ..models import TipoModulo, Modulo
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def modulo_for_groups(request, tm):
    return [modulo for modulo in tm.modulos.all() if request.user.groups.all()[0] in modulo.grupos.all()]


@register.simple_tag
def tipo_menu(request):
    tipos = [tipo for tipo in TipoModulo.objects.filter(padre_tipo=None) if len(modulo_for_groups(request,tipo))>0]
    #tipo = TipoModulo.objects.filter(padre_tipo=None)
    return tipos



@register.simple_tag
def is_active_tm(request):
    try:
        modulos = Modulo.objects.all()
        for m in modulos:
            if m.get_url() == request.path:
                return m.tipo
        return None
    except:
        return None


@register.simple_tag
def is_papa(hijo, papa):
    try:
        if hijo.padre_tipo == papa:
            return True
        return False
        #print(f"{}")
        #print(f"{papa}")
        # if hijo in papa.padre_tipo.all():
        #     print(f"Si soy papa- {hijo}")
        #     return True
        # print(f'desde is_papa - {hijo}')
        # return False
    except:
        return False


@register.simple_tag
def activo(request, urlconfi):
    try:
        url_reverse = reverse(urlconfi)
        if request.path == url_reverse:
            return "active"
        return 'no-active'
    except:
        return "no-active"
