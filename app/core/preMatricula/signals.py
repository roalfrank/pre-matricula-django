from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import PreMatriculaEstudiante


@receiver(post_delete, sender=PreMatriculaEstudiante)
def actualizarMatricula(sender, instance, **kwargs):
    print('desde signal', instance)
