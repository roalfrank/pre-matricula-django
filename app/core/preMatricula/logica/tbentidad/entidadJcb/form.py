from django.forms import ModelForm
from core.preMatricula.models import JCB


class JcbForm(ModelForm):
    """Form definition for jcb."""
    #region1 = forms.ChoiceField(choices=Region.objects.none())
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['region'].queryset = Region.objects.all()

    # def clean(self):
    #     print(self.fields['region'].queryset)
    #     return super().clean()

    class Meta:
        """Meta definition for jcb."""

        model = JCB
        fields = ('codigo_jcb', 'jcm')
