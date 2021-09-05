from core.preMatricula.models import Cargo
from django.forms import ModelForm


class CargoInstructorForm(ModelForm):
    """Form definition for CargoInstructor."""

    class Meta:
        """Meta definition for CargoInstructor."""

        model = Cargo
        fields = '__all__'
