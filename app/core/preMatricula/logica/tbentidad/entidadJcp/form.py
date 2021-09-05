from core.preMatricula.models import Entidad, JCP, Provincia, Municipio
from django.forms import ModelForm, ModelChoiceField, Select


class EntidadForm(ModelForm):
    """Form definition for entidad."""
    provincia = ModelChoiceField(queryset=Provincia.objects.all(), widget=Select(attrs={
        'class': 'select2'
    }))

    class Meta:
        """Meta definition for entidad."""

        model = Entidad
        fields = ['nombre', 'telefono', 'direccion', 'provincia', 'municipio']


class JcpForm(ModelForm):
    """Form definition for entidad."""

    class Meta:
        """Meta definition for entidad."""

        model = JCP
        fields = ('codigo_jcp',)
