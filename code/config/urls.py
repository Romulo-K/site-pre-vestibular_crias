"""
Endereços (URLs) do projeto.

    /            → páginas públicas (app "paginas")
    /admin/      → painel da coordenação (Django Admin)
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paginas.urls")),
]

# No seu computador (DEBUG=1), o próprio Django entrega as fotos enviadas.
# No servidor, quem entrega é o PythonAnywhere (Etapa 11).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
