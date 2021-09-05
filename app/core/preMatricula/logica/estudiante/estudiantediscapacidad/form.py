from core.preMatricula.models import Discapacidad
from django.forms import ModelForm


class DiscapacidadEstudianteForm(ModelForm):
    """Form definition for Discapacidad-Estudiante."""

    class Meta:
        """Meta definition for Discapacidad-Estudiante."""

        model = Discapacidad
        fields = '__all__'
