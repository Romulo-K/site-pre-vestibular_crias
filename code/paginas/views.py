"""
Views das páginas públicas.

Cada função recebe o pedido do navegador (request), busca no banco o que for
preciso e devolve a página pronta (render). O público só vê:
  - notícias PUBLICADAS (rascunhos nunca aparecem);
  - integrantes e depoimentos marcados como "aparece no site".
"""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from conteudo.models import Depoimento, FotoGaleria, Integrante, Noticia

NOTICIAS_POR_PAGINA = 9
FOTOS_POR_PAGINA = 24

# As 5 atividades do projeto (cards da Home). O texto oficial entra na Etapa 9.
ATIVIDADES = [
    {"tipo": "aulas", "titulo": "Aulas", "descricao": "[DESCRIÇÃO OFICIAL DAS AULAS]",
     "alt": "Imagem ilustrativa de aula (substituir por foto real da ONG)"},
    {"tipo": "palestras", "titulo": "Palestras", "descricao": "[DESCRIÇÃO OFICIAL DAS PALESTRAS]",
     "alt": "Imagem ilustrativa de palestra (substituir por foto real da ONG)"},
    {"tipo": "simulados", "titulo": "Simulados", "descricao": "[DESCRIÇÃO OFICIAL DOS SIMULADOS]",
     "alt": "Imagem ilustrativa de simulado (substituir por foto real da ONG)"},
    {"tipo": "convivencia", "titulo": "Convivência", "descricao": "[DESCRIÇÃO OFICIAL DOS MOMENTOS DE CONVIVÊNCIA]",
     "alt": "Imagem ilustrativa de momento de convivência (substituir por foto real da ONG)"},
    {"tipo": "passeios", "titulo": "Passeios", "descricao": "[DESCRIÇÃO OFICIAL DOS PASSEIOS]",
     "alt": "Imagem ilustrativa de passeio (substituir por foto real da ONG)"},
]

# Ordem dos grupos da equipe na Home: coordenação primeiro
ORDEM_GRUPOS = [Integrante.Grupo.COORDENACAO, Integrante.Grupo.PROFESSORES, Integrante.Grupo.APOIO]


def equipe_visivel():
    return Integrante.objects.filter(ativo=True)


def depoimentos_visiveis():
    return Depoimento.objects.filter(ativo=True, autorizado=True)


def inicio(request):
    equipe = sorted(equipe_visivel(), key=lambda i: (ORDEM_GRUPOS.index(i.grupo), i.ordem, i.nome))
    contexto = {
        "noticias": Noticia.objects.publicadas()[:3],
        "depoimentos": depoimentos_visiveis()[:4],
        "equipe": equipe[:4],
        "atividades": ATIVIDADES,
    }
    return render(request, "paginas/inicio.html", contexto)


def projeto(request):
    return render(request, "paginas/projeto.html")


def atividades(request):
    fotos = Paginator(FotoGaleria.objects.all(), FOTOS_POR_PAGINA).get_page(request.GET.get("pagina"))
    return render(request, "paginas/atividades.html", {"fotos": fotos})


def equipe(request):
    grupos = [
        {"id": valor, "titulo": rotulo, "pessoas": equipe_visivel().filter(grupo=valor)}
        for valor, rotulo in Integrante.Grupo.choices
    ]
    return render(request, "paginas/equipe.html", {"grupos": grupos})


def alunos(request):
    return render(request, "paginas/alunos.html")


def voluntarios(request):
    return render(request, "paginas/voluntarios.html")


def noticias(request):
    pagina = Paginator(Noticia.objects.publicadas(), NOTICIAS_POR_PAGINA).get_page(request.GET.get("pagina"))
    return render(request, "paginas/noticias.html", {"noticias": pagina})


def noticia_detalhe(request, slug):
    # Visitantes: só publicadas (rascunho dá "página não encontrada").
    # A coordenação logada no painel pode pré-visualizar rascunhos.
    if request.user.is_staff:
        noticia = get_object_or_404(Noticia, slug=slug)
    else:
        noticia = get_object_or_404(Noticia.objects.publicadas(), slug=slug)
    return render(request, "paginas/noticia_detalhe.html", {"noticia": noticia})


def contato(request):
    return render(request, "paginas/contato.html")
