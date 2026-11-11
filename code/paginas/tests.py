# testes das páginas do site
# rodar com: python manage.py test

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from conteudo.models import Depoimento, Integrante, Noticia

PAGINAS = ["inicio", "projeto", "atividades", "equipe", "alunos", "voluntarios", "noticias", "contato"]


def criar_noticia(titulo, status="publicada"):
    return Noticia.objects.create(titulo=titulo, resumo="resumo", texto="texto", status=status)


class TestesPaginas(TestCase):

    def test_todas_as_paginas_abrem(self):
        for nome in PAGINAS:
            resposta = self.client.get(reverse("paginas:" + nome))
            self.assertEqual(resposta.status_code, 200, nome)

    def test_pagina_que_nao_existe(self):
        self.assertEqual(self.client.get("/nao-existe/").status_code, 404)

    def test_menu_marca_a_pagina_atual(self):
        resposta = self.client.get(reverse("paginas:equipe"))
        self.assertContains(resposta, 'href="/equipe/" aria-current="page"')

    def test_banco_vazio_mostra_aviso(self):
        self.assertContains(self.client.get(reverse("paginas:noticias")), "Nenhuma notícia publicada ainda.")

    # ---------- notícias ----------

    def test_home_mostra_so_3_noticias_publicadas(self):
        for i in range(4):
            criar_noticia(f"Publicada {i}")
        criar_noticia("Rascunho secreto", status="rascunho")
        html = self.client.get(reverse("paginas:inicio")).content.decode()
        self.assertNotIn("Rascunho secreto", html)
        self.assertEqual(html.count('class="card card--noticia'), 3)

    def test_rascunho_nao_abre_pra_visitante(self):
        rascunho = criar_noticia("Rascunho", status="rascunho")
        self.assertEqual(self.client.get(rascunho.get_absolute_url()).status_code, 404)

    def test_coordenacao_ve_o_rascunho(self):
        rascunho = criar_noticia("Rascunho", status="rascunho")
        User.objects.create_user("coord", password="SenhaDeTeste2026", is_staff=True)
        self.client.login(username="coord", password="SenhaDeTeste2026")
        self.assertContains(self.client.get(rascunho.get_absolute_url()), "Rascunho:")

    def test_texto_da_noticia_nao_vira_codigo(self):
        # se alguém escrever <script> na notícia, tem que aparecer como texto e não rodar
        noticia = Noticia.objects.create(titulo="T", resumo="r", texto="<script>alert(1)</script>", status="publicada")
        resposta = self.client.get(noticia.get_absolute_url())
        self.assertContains(resposta, "&lt;script&gt;")
        self.assertNotContains(resposta, "<script>alert(1)")

    # ---------- equipe e depoimentos ----------

    def test_integrante_escondido_nao_aparece(self):
        Integrante.objects.create(nome="Ana Ativa", funcao="Professora")
        Integrante.objects.create(nome="Bruno Escondido", funcao="Professor", ativo=False)
        html = self.client.get(reverse("paginas:equipe")).content.decode()
        self.assertIn("Ana Ativa", html)
        self.assertNotIn("Bruno Escondido", html)

    def test_depoimento_sem_autorizacao_nao_aparece(self):
        Depoimento.objects.create(nome="Com autorizacao", texto="Ótimo", autorizado=True)
        Depoimento.objects.create(nome="Sem autorizacao", texto="x", autorizado=False)
        html = self.client.get(reverse("paginas:inicio")).content.decode()
        self.assertIn("Com autorizacao", html)
        self.assertNotIn("Sem autorizacao", html)

    # ---------- versão de teste ----------

    def test_faixa_de_versao_de_teste(self):
        with self.settings(SITE_EM_TESTE=True):
            self.assertContains(self.client.get("/"), "Versão de teste.")
            self.assertContains(self.client.get("/robots.txt"), "Disallow: /\n")
        with self.settings(SITE_EM_TESTE=False):
            self.assertNotContains(self.client.get("/"), "Versão de teste.")
