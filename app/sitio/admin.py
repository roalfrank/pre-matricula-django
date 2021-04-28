from django.contrib import admin
from .models import Modulo, TipoModulo, Sitio_Web
# Register your models here.
admin.site.register(Sitio_Web)
admin.site.register(TipoModulo)
admin.site.register(Modulo)

