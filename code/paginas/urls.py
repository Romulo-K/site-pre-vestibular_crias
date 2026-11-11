"""
URLs das páginas públicas.

Nos templates, use o nome da rota em vez do endereço escrito à mão:
    <a href="{% url 'paginas:projeto' %}">O Projeto</a>
Assim, se um endereço mudar, basta mudar aqui.
"""
from django.urls import path

from . import views

app_name = "paginas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("projeto/", views.projeto, name="projeto"),
    path("atividades/", views.atividades, name="atividades"),
    path("equipe/", views.equipe, name="equipe"),
    path("alunos/", views.alunos, name="alunos"),
    path("voluntarios/", views.voluntarios, name="voluntarios"),
    path("noticias/", views.noticias, name="noticias"),
    path("noticias/<slug:slug>/", views.noticia_detalhe, name="noticia"),
    path("contato/", views.contato, name="contato"),
]
