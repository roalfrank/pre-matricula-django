from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.sitio.urls")),
    path('login/', include("core.login.urls")),
    path('user/', include("core.user.urls")),
    path('sistema/', include("core.preMatricula.urls")),
    path('estudiante/', include("core.estudiante.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
