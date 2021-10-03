from django.urls import path
from core.preMatricula.consumers.matricula_cs import LikeMatricula, MatriculaUpdate, ComentariosMatricula

ws_urlpatterns = [
    # websocket de matricula..
    path('ws/like-matricula/<int:matricula>/', LikeMatricula.as_asgi()),
    path('ws/update-matricula/<int:matricula>/', MatriculaUpdate.as_asgi()),
    # comentarios
    path('ws/comentario-matricula/<int:matricula>/',
         ComentariosMatricula.as_asgi()),  # comenatrios de una matricula

]
