from django.contrib import admin

# Register your models here.
from .models import User,Perfil
admin.site.register(User)

admin.site.register(Perfil)
