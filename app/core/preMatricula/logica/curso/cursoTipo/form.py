from core.preMatricula.models import TipoGrupo
from django.forms import ModelForm


class TipoCursoForm(ModelForm):
    """Form definition for Tipo de curso."""

    class Meta:
        """Meta definition for Tipo de curso."""

        model = TipoGrupo
        fields = '__all__'
