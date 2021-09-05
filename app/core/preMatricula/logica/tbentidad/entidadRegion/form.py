from core.preMatricula.models import Region
from django.forms import ModelForm


class RegionForm(ModelForm):
    """Form definition for region."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jcp'].widget.attrs['class'] = 'select2'

    class Meta:
        """Meta definition for region."""

        model = Region
        fields = '__all__'
