from django.forms import forms, ModelChoiceField, Select
from core.preMatricula.models import Curso


class EstudianteCursosForm(forms.Form):
    cursos = ModelChoiceField(queryset=Curso.objects.all(), required=False, widget=Select(attrs={
        'class': 'select2'
    }))
