import os
from django.conf import settings
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
from core.preMatricula.models import JCM, Region


def generar_pdf(template_name, context, name_pdf='pdf_generado', adjunto=False):
    response = HttpResponse(content_type='application/pdf')
    disposition_pdf = 'filename= "' + name_pdf + '.pdf"'
    if adjunto:
        disposition_pdf = 'attachement; ' + disposition_pdf

    response['Content-Disposition'] = disposition_pdf
    template = get_template(template_name)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error en la creacion del  pdf <pre>' + html + '</pre>')
    return response


def regionProvincia(id_provincia, formato='default'):
    if formato == 'select2':
        regiones = [{'id': i.id, 'text': i.__str__()}
                    for i in Region.objects.filter(jcp__entidad__municipio__provincia__pk=id_provincia)]
    else:
        regiones = Region.objects.filter(
            jcp__entidad__municipio__provincia__pk=id_provincia)
    return regiones


def jcmProvincia(id_provincia, formato='default'):
    if formato == 'select2':
        jcms = [{'id': i.id, 'text': i.__str__()}
                for i in JCM.objects.filter(entidad__municipio__provincia__pk=id_provincia)]
    else:
        jcms = JCM.objects.filter(
            entidad__municipio__provincia__pk=id_provincia)
    return jcms


def listado_matricula_estudiante(estudiante, json=False):
    listado_matricula = estudiante.prematriculaestudiante_set.all()
    listado_matricula_dict = {}
    print(listado_matricula)
    if listado_matricula.count() > 0:
        pass
    return listado_matricula
