"""
Variáveis disponíveis em TODOS os templates.
(Registrado em config/settings.py, TEMPLATES > context_processors.)
"""
from django.conf import settings


def site(request):
    return {"site_em_teste": settings.SITE_EM_TESTE}
