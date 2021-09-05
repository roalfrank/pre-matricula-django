from django.urls import path
from.views import perfil,estaUsuario
app_name = "user"

urlpatterns = [
    path("perfil/", perfil, name="perfil"),
    path("chequear-name/", estaUsuario, name="chequearUserName"),
]
