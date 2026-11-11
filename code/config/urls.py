# endereços principais do site
#   /        -> páginas do site (app paginas)
#   /admin/  -> painel da coordenação

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paginas.urls")),
]

# no meu pc o próprio django mostra as fotos enviadas
# no servidor quem faz isso é o pythonanywhere (configurado na aba Web)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
