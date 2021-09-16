from core.preMatricula.models import JCM, Region


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
