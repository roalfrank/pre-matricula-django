from django.urls import path
from .views import dashBoardEstudiante, dashBoardAdmin,dashBoardGestor,index

app_name = "sitio"

urlpatterns = [
    path("", index, name="inicio"),
    path("panel-estudiante", dashBoardEstudiante, name="panel-estudiante"),
    path("panel-gestor", dashBoardGestor, name="panel-gestor"),
    path("panel-admin", dashBoardAdmin, name="panel-admin"),
]
