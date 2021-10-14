from django.forms import ModelForm, ModelChoiceField, Select
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.user.models import User, Perfil
from core.preMatricula.models import Provincia, JCP


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserPerfilRegistrationForm(ModelForm):
    provincia = ModelChoiceField(queryset=Provincia.objects.all(), widget=Select(attrs={
        'class': 'select2'
    }))

    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('user', 'avatar')
