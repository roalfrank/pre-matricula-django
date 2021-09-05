from django.test import TestCase
from core.preMatricula.models import Provincia

def crear_datos(hasta):
    for n in range(1,hasta):
        nombre = f"roal-{n}"
        provincia = Provincia(nombre=nombre)
        provincia.save()


crear_datos(30)
