from django.contrib import admin

# Register your models here.
from .models import User, Etiqueta_Domina, Perfil
admin.site.register(User)
admin.site.register(Etiqueta_Domina)
admin.site.register(Perfil)
