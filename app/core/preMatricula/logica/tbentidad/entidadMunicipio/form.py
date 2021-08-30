from core.preMatricula.models import Municipio
from django.forms import ModelForm


class MunicipioForm(ModelForm):
    """Form definition for Tipo de curso."""

    class Meta:
        """Meta definition for Tipo de curso."""

        model = Municipio
        fields = '__all__'
