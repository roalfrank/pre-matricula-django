from core.preMatricula.models import Provincia
from django.forms import ModelForm
from user.models import Estado


class EstadoUsuarioForm(ModelForm):
    """Form definition for Provincia."""

    class Meta:
        """Meta definition for Provinciaform."""

        model = Estado
        fields = '__all__'
