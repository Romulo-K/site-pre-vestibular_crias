# variáveis que ficam disponíveis em todos os templates (registrado no settings.py)

from django.conf import settings

from conteudo.models import ConfiguracaoSite


def site(request):
    config = ConfiguracaoSite.carregar()
    return {
        "site_em_teste": settings.SITE_EM_TESTE,
        "config": config,                             # links e contatos (usados nos templates)
        "config_js": config.para_javascript(),        # os mesmos links, pro javascript dos botões
    }
