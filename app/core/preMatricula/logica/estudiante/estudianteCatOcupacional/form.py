from core.preMatricula.models import CategoriaOcupacional
from django.forms import ModelForm


class CategoriaOcupacionalEstudianteForm(ModelForm):
    """Form definition for CategoriaOcupacional-Estudiante."""

    class Meta:
        """Meta definition for CategoriaOcupacional-Estudiante."""

        model = CategoriaOcupacional
        fields = '__all__'
