from django.forms import ModelForm, ModelChoiceField, Select
from core.preMatricula.models import PreMatricula, JCP


class PreMatriculaForm(ModelForm):
    """Form definition for PreMatricula."""
    jcp = ModelChoiceField(queryset=JCP.objects.all(), required=False, widget=Select(attrs={
        'class': 'select2'
    }))

    class Meta:
        """Meta definition for PreMatricula."""

        model = PreMatricula
        fields = '__all__'
