from django.forms import ModelForm
from core.preMatricula.models import Instructor


class InstructorForm(ModelForm):
    """Form definition for instructor."""
    class Meta:
        """Meta definition for instructor."""

        model = Instructor
        fields = ('usuario_siscae', 'jcb',
                  'cargo')
