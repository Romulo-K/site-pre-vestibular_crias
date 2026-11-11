# views = funções que montam cada página
# cada uma pega o que precisa no banco e manda pro template

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from conteudo.models import Depoimento, FotoGaleria, Integrante, Noticia

NOTICIAS_POR_PAGINA = 9
FOTOS_POR_PAGINA = 24

# as 5 atividades dos cards da home
ATIVIDADES = [
    {"tipo": "aulas", "titulo": "Aulas", "descricao": "Conteúdos do ENEM e dos vestibulares, com materiais de apoio.",
     "alt": "Imagem ilustrativa de aula (substituir por foto real da ONG)"},
    {"tipo": "palestras", "titulo": "Palestras", "descricao": "Temas que ajudam na escolha do futuro e da carreira.",
     "alt": "Imagem ilustrativa de palestra (substituir por foto real da ONG)"},
    {"tipo": "simulados", "titulo": "Simulados", "descricao": "Provas no formato do ENEM para treinar e acompanhar a evolução.",
     "alt": "Imagem ilustrativa de simulado (substituir por foto real da ONG)"},
    {"tipo": "convivencia", "titulo": "Convivência", "descricao": "Integração entre a turma, os professores e a equipe.",
     "alt": "Imagem ilustrativa de momento de convivência (substituir por foto real da ONG)"},
    {"tipo": "passeios", "titulo": "Passeios", "descricao": "Novos lugares e experiências que ampliam o repertório.",
     "alt": "Imagem ilustrativa de passeio (substituir por foto real da ONG)"},
]


# ---------------- páginas com dados do banco ----------------

def inicio(request):
    # na home a equipe aparece com a coordenação primeiro, depois professores e apoio
    ordem_grupos = ["coordenacao", "professores", "apoio"]
    equipe = Integrante.objects.filter(ativo=True)
    equipe = sorted(equipe, key=lambda pessoa: (ordem_grupos.index(pessoa.grupo), pessoa.ordem, pessoa.nome))

    contexto = {
        "noticias": Noticia.objects.filter(status="publicada")[:3],  # só as 3 mais recentes
        "depoimentos": Depoimento.objects.filter(ativo=True, autorizado=True)[:4],
        "equipe": equipe[:4],
        "atividades": ATIVIDADES,
    }
    return render(request, "paginas/inicio.html", contexto)


def atividades(request):
    # galeria dividida em páginas de 24 fotos (?pagina=2 na url)
    fotos = Paginator(FotoGaleria.objects.all(), FOTOS_POR_PAGINA).get_page(request.GET.get("pagina"))
    return render(request, "paginas/atividades.html", {"fotos": fotos})


def equipe(request):
    # uma lista pra cada grupo (coordenação, professores, apoio)
    grupos = []
    for valor, nome in Integrante.GRUPOS:
        pessoas = Integrante.objects.filter(ativo=True, grupo=valor)
        grupos.append({"id": valor, "titulo": nome, "pessoas": pessoas})
    return render(request, "paginas/equipe.html", {"grupos": grupos})


def noticias(request):
    publicadas = Noticia.objects.filter(status="publicada")
    pagina = Paginator(publicadas, NOTICIAS_POR_PAGINA).get_page(request.GET.get("pagina"))
    return render(request, "paginas/noticias.html", {"noticias": pagina})


def noticia_detalhe(request, slug):
    # visitante só vê notícia publicada (rascunho dá erro 404)
    # quem tá logado no painel consegue ver o rascunho pra conferir antes de publicar
    if request.user.is_staff:
        noticia = get_object_or_404(Noticia, slug=slug)
    else:
        noticia = get_object_or_404(Noticia, slug=slug, status="publicada")
    return render(request, "paginas/noticia_detalhe.html", {"noticia": noticia})


# ---------------- páginas só com texto fixo ----------------

def projeto(request):
    return render(request, "paginas/projeto.html")


def alunos(request):
    return render(request, "paginas/alunos.html")


def voluntarios(request):
    return render(request, "paginas/voluntarios.html")


def contato(request):
    return render(request, "paginas/contato.html")


def robots_txt(request):
    # avisa o google se pode ou não mostrar o site nas buscas
    if settings.SITE_EM_TESTE:
        texto = "User-agent: *\nDisallow: /\n"
    else:
        texto = "User-agent: *\nDisallow: /admin/\n"
    return HttpResponse(texto, content_type="text/plain")
