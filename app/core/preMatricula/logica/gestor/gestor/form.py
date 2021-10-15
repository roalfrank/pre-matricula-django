from django.forms import ModelForm, ModelChoiceField, Select
from core.preMatricula.models import Gestor, JCP


class GestorForm(ModelForm):
    """Form definition for gestor."""
    jcp = ModelChoiceField(queryset=JCP.objects.all(), widget=Select(attrs={
        'class': 'select2'
    }))

    class Meta:
        """Meta definition for gestor."""

        model = Gestor
        fields = ('jcm',)
