from django.forms import ModelForm
from django.contrib.auth.models import User


class UserCrearAutomaticoFormAdmin(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'is_active', 'is_staff')
    # si viene de editar no cambia el pasword

    def save(self, commit=True, edit=False):
        user = super().save(commit=False)
        if not edit:
            user.set_password(self.cleaned_data["username"])
        if commit:
            user.save()
        return user
