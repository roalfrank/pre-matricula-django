from django.urls import path
from.views import estaUsuario, PerfilDetailView, verperfil
app_name = "user"

urlpatterns = [
    path("perfil/<pk>/", PerfilDetailView.as_view(), name="perfil-detalle"),
    path("perfil/", verperfil, name="perfil"),
    path("chequear-name/", estaUsuario, name="chequearUserName"),
]
