from django.urls import path
from core.preMatricula.consumers.matricula_cs import LikeMatricula, MatriculaUpdate

ws_urlpatterns = [
    # websocket de matricula..
    path('ws/like-matricula/<int:matricula>/', LikeMatricula.as_asgi()),
    path('ws/update-matricula/<int:matricula>/', MatriculaUpdate.as_asgi())
]
