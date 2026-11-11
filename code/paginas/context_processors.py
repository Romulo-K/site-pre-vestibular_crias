# variáveis que ficam disponíveis em todos os templates (registrado no settings.py)

from django.conf import settings


def site(request):
    return {"site_em_teste": settings.SITE_EM_TESTE}
