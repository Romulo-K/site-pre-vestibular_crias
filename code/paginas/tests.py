"""
Testes automáticos das páginas públicas.
Rodar:  python manage.py test
"""
from django.test import TestCase
from django.urls import reverse

PAGINAS = ["inicio", "projeto", "atividades", "equipe", "alunos", "voluntarios", "noticias", "contato"]


class PaginasPublicasTest(TestCase):
    def test_todas_as_paginas_abrem(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                resposta = self.client.get(reverse(f"paginas:{nome}"))
                self.assertEqual(resposta.status_code, 200)

    def test_menu_marca_a_pagina_atual(self):
        resposta = self.client.get(reverse("paginas:equipe"))
        self.assertContains(resposta, f'href="{reverse("paginas:equipe")}" aria-current="page"')

    def test_pagina_inexistente_da_404(self):
        self.assertEqual(self.client.get("/pagina-que-nao-existe/").status_code, 404)
