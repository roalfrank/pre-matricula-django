from django.forms import ModelForm, ModelChoiceField, Select
from core.preMatricula.models import Instructor, JCP


class InstructorForm(ModelForm):
    """Form definition for instructor."""
    jcp = ModelChoiceField(queryset=JCP.objects.all(), widget=Select(attrs={
        'class': 'select2'
    }))

    class Meta:
        """Meta definition for instructor."""

        model = Instructor
        fields = ('usuario_siscae', 'jcb',
                  'cargo')
