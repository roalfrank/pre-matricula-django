from django.urls import path
from .views import dashBoardPrincipal
app_name = "sitio"
urlpatterns = [
    path("", dashBoardPrincipal, name="listar"),
]
