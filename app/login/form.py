from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from user.models import User, Perfil


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields =('username','email','first_name','last_name','password1','password2')


class UserPerfilRegistrationForm(ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
