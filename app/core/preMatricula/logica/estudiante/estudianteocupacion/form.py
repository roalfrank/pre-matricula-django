from core.preMatricula.models import Ocupacion
from django.forms import ModelForm


class OcupacionEstudianteForm(ModelForm):
    """Form definition for OcupacionEstudiante."""

    class Meta:
        """Meta definition for OcupacionEstudiante."""

        model = Ocupacion
        fields = '__all__'
