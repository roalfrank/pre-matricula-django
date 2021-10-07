from django.forms import ModelForm
from django.contrib.auth.models import User
from core.preMatricula.models import Estudiante


class UserCrearAutomaticoForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'is_active')
    # si viene de editar no cambia el pasword

    def save(self, commit=True, edit=False):
        user = super().save(commit=False)
        print('ver el valor de edit en save del UserCrearAutomaticoForm', edit)
        if not edit:
            user.set_password(self.cleaned_data["username"])
        if commit:
            user.save()
        return user


class EstudianteForm(ModelForm):
    """Form definition for estudiante."""
    class Meta:
        """Meta definition for estudiante."""

        model = Estudiante
        fields = ('ocupacion', 'categoria_ocupacional',
                  'discapacidad', 'usuario_sisce')
