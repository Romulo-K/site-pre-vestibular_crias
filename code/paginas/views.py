"""
Views das páginas públicas.

Cada função recebe o pedido do navegador (request) e devolve a página pronta.
Nesta etapa elas só mostram o template. Na Etapa 8, as views de Início,
Equipe, Atividades e Notícias passam a buscar os dados no banco.
"""
from django.shortcuts import render


def inicio(request):
    return render(request, "paginas/inicio.html")


def projeto(request):
    return render(request, "paginas/projeto.html")


def atividades(request):
    return render(request, "paginas/atividades.html")


def equipe(request):
    return render(request, "paginas/equipe.html")


def alunos(request):
    return render(request, "paginas/alunos.html")


def voluntarios(request):
    return render(request, "paginas/voluntarios.html")


def noticias(request):
    return render(request, "paginas/noticias.html")


def contato(request):
    return render(request, "paginas/contato.html")
