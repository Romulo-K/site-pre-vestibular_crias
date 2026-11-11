"""
Testes automáticos das páginas públicas.
Rodar:  python manage.py test
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from conteudo.models import Depoimento, Integrante, Noticia

PAGINAS = ["inicio", "projeto", "atividades", "equipe", "alunos", "voluntarios", "noticias", "contato"]


def nova_noticia(titulo, publicada=True):
    status = Noticia.Status.PUBLICADA if publicada else Noticia.Status.RASCUNHO
    return Noticia.objects.create(titulo=titulo, resumo=f"Resumo de {titulo}", texto="Parágrafo 1\n\nParágrafo 2", status=status)


class PaginasPublicasTest(TestCase):
    def test_todas_as_paginas_abrem_com_banco_vazio(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                self.assertEqual(self.client.get(reverse(f"paginas:{nome}")).status_code, 200)

    def test_menu_marca_a_pagina_atual(self):
        resposta = self.client.get(reverse("paginas:equipe"))
        self.assertContains(resposta, f'href="{reverse("paginas:equipe")}" aria-current="page"')

    def test_pagina_inexistente_da_404(self):
        self.assertEqual(self.client.get("/pagina-que-nao-existe/").status_code, 404)

    def test_estados_vazios(self):
        self.assertContains(self.client.get(reverse("paginas:inicio")), "Nenhuma notícia publicada ainda.")
        self.assertContains(self.client.get(reverse("paginas:noticias")), "Nenhuma notícia publicada ainda.")


class NoticiasPublicasTest(TestCase):
    def test_home_mostra_so_as_3_publicadas_mais_recentes(self):
        for i in range(4):
            nova_noticia(f"Publicada {i}")
        nova_noticia("Rascunho secreto", publicada=False)
        html = self.client.get(reverse("paginas:inicio")).content.decode()
        self.assertNotIn("Rascunho secreto", html)
        self.assertEqual(html.count('class="card card--noticia'), 3)

    def test_rascunho_nao_abre_para_visitante(self):
        n = nova_noticia("Rascunho", publicada=False)
        self.assertEqual(self.client.get(n.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse("paginas:noticias")), "Rascunho")

    def test_coordenacao_pode_pre_visualizar_rascunho(self):
        n = nova_noticia("Rascunho", publicada=False)
        User.objects.create_user("coord", password="SenhaDeTeste2026", is_staff=True)
        self.client.login(username="coord", password="SenhaDeTeste2026")
        resposta = self.client.get(n.get_absolute_url())
        self.assertContains(resposta, "Rascunho:")

    def test_pagina_da_noticia_e_texto_seguro(self):
        n = Noticia.objects.create(titulo="Teste", resumo="r", texto="<script>alert(1)</script>",
                                   status=Noticia.Status.PUBLICADA)
        resposta = self.client.get(n.get_absolute_url())
        self.assertContains(resposta, "&lt;script&gt;")      # aparece como texto
        self.assertNotContains(resposta, "<script>alert(1)")  # não é executado

    def test_paginacao(self):
        for i in range(11):
            nova_noticia(f"N{i}")
        self.assertContains(self.client.get(reverse("paginas:noticias")), "Página 1 de 2")
        self.assertEqual(self.client.get(reverse("paginas:noticias") + "?pagina=2").status_code, 200)
        self.assertEqual(self.client.get(reverse("paginas:noticias") + "?pagina=abc").status_code, 200)


class EquipeEDepoimentosTest(TestCase):
    def test_integrante_inativo_nao_aparece(self):
        Integrante.objects.create(nome="Ana Ativa", funcao="Professora", grupo="professores")
        Integrante.objects.create(nome="Bruno Inativo", funcao="Professor", grupo="professores", ativo=False)
        for nome in ("inicio", "equipe"):
            html = self.client.get(reverse(f"paginas:{nome}")).content.decode()
            self.assertIn("Ana Ativa", html)
            self.assertNotIn("Bruno Inativo", html)

    def test_home_mostra_coordenacao_primeiro(self):
        Integrante.objects.create(nome="Prof", funcao="Professor", grupo="professores", ordem=0)
        Integrante.objects.create(nome="Coord", funcao="Coordenadora", grupo="coordenacao", ordem=5)
        html = self.client.get(reverse("paginas:inicio")).content.decode()
        self.assertLess(html.index("Coord"), html.index("Prof"))

    def test_depoimento_so_aparece_se_ativo_e_autorizado(self):
        Depoimento.objects.create(nome="Visivel", texto="Ótimo", autorizado=True)
        Depoimento.objects.create(nome="Sem autorizacao", texto="x", autorizado=False)
        Depoimento.objects.create(nome="Inativo", texto="x", autorizado=True, ativo=False)
        html = self.client.get(reverse("paginas:inicio")).content.decode()
        self.assertIn("Visivel", html)
        self.assertNotIn("Sem autorizacao", html)
        self.assertNotIn("Inativo", html)
