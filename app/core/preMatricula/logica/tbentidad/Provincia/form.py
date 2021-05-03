from django.forms import ModelForm
from core.preMatricula.models import Provincia

class ProvinciaForm(ModelForm):
    """Form definition for Provincia."""

    class Meta:
        """Meta definition for Provinciaform."""

        model = Provincia
        fields = '__all__'
