from core.preMatricula.models import EstadoMatricula
from django.forms import ModelForm


class EstadoMatriculaForm(ModelForm):
    """Form definition for Tipo de curso."""

    class Meta:
        """Meta definition for Tipo de curso."""

        model = EstadoMatricula
        fields = '__all__'
