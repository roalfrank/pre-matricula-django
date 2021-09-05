from django.forms import ModelForm, ModelChoiceField, Select
from core.preMatricula.models import JCM, Region


class JcmForm(ModelForm):
    """Form definition for jcm."""

    class Meta:
        """Meta definition for jcm."""

        model = JCM
        fields = ('codigo_jcm', 'region')
