from core.preMatricula.models import Maestro


def cantidadMaestro():
    cant = Maestro.objects.all().count()
    return cant
