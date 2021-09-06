from django.forms import ModelForm, ModelChoiceField, Select
from django import forms
from core.preMatricula.models import JCM, Region


class JcmForm(ModelForm):
    """Form definition for jcm."""
    #region1 = forms.ChoiceField(choices=Region.objects.none())
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['region'].queryset = Region.objects.all()

    # def clean(self):
    #     print(self.fields['region'].queryset)
    #     return super().clean()

    class Meta:
        """Meta definition for jcm."""

        model = JCM
        fields = ('codigo_jcm', 'region')
