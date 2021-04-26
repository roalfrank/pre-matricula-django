from django.urls import path
from.views import perfil
app_name = "user"

urlpatterns = [
    path("", perfil, name="perfil")
]
