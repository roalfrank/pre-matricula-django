from django.forms import ModelForm
from core.preMatricula.models import Curso


class CursoForm(ModelForm):
    """Form definition for curso."""
    class Meta:
        """Meta definition for curso."""

        model = Curso
        fields = '__all__'
