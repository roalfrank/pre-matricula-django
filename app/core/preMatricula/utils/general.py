from core.preMatricula.models import Region


def RegionProvincia(id_provincia, formato='default'):
    if formato == 'select2':
        region = [{'id': i.id, 'text': i.__str__()}
                  for i in Region.objects.filter(jcp__entidad__municipio__provincia__pk=id_provincia)]
    else:
        region = Region.objects.filter(
            jcp__entidad__municipio__provincia__pk=id_provincia)
    return region
