from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Modulo, TipoModulo, Sitio_Web

# Register your models here.
admin.site.register(Sitio_Web)
admin.site.register(TipoModulo)
admin.site.register(Modulo)
admin.site.register(Permission)

