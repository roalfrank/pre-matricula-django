from core.preMatricula.models import Modalidad
from django.forms import ModelForm


class ModalidadMatriculaForm(ModelForm):
    """Form definition for Tipo de curso."""

    class Meta:
        """Meta definition for Tipo de curso."""

        model = Modalidad
        fields = '__all__'
