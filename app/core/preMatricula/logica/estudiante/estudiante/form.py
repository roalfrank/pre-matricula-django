from core.preMatricula.models import Estudiante
from django.forms import ModelForm


class EstudianteForm(ModelForm):
    """Form definition for Estudiante."""

    class Meta:
        """Meta definition for Estudiante."""

        model = Estudiante
        fields = '__all__'
