from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from user.models import User, Perfil



class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields =('username','password1','password2')



class UserPerfilRegistrationForm(ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude=('user','municipio','avatar')
