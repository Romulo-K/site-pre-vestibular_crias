# testes do conteúdo (models e regras das fotos)
# rodar com: python manage.py test

import io
import shutil
import tempfile

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from .models import FotoGaleria, Integrante, Noticia
from .validators import validar_tamanho

# as fotos dos testes vão pra uma pasta temporária, pra não sujar a media/
PASTA_TESTE = tempfile.mkdtemp()


def criar_imagem(nome="foto.png"):
    # cria uma imagem verde de 10x10 só pra testar
    arquivo = io.BytesIO()
    Image.new("RGB", (10, 10), "green").save(arquivo, "PNG")
    return SimpleUploadedFile(nome, arquivo.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=PASTA_TESTE)
class TestesConteudo(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_slug_nao_repete(self):
        a = Noticia.objects.create(titulo="Simulado de Outubro", resumo="r", texto="t")
        b = Noticia.objects.create(titulo="Simulado de Outubro", resumo="r", texto="t")
        self.assertEqual(a.slug, "simulado-de-outubro")
        self.assertEqual(b.slug, "simulado-de-outubro-2")

    def test_data_de_publicacao_so_na_primeira_vez(self):
        noticia = Noticia.objects.create(titulo="N", resumo="r", texto="t")
        self.assertIsNone(noticia.publicada_em)  # rascunho não tem data

        noticia.status = "publicada"
        noticia.save()
        data = noticia.publicada_em
        self.assertIsNotNone(data)

        noticia.resumo = "editado"
        noticia.save()
        self.assertEqual(noticia.publicada_em, data)  # editar não muda a data

    def test_capa_precisa_de_descricao(self):
        noticia = Noticia(titulo="N", resumo="r", texto="t", capa=criar_imagem())
        with self.assertRaises(ValidationError):
            noticia.full_clean()

    def test_foto_precisa_de_autorizacao(self):
        pessoa = Integrante(nome="Ana", funcao="Professora", foto=criar_imagem())
        with self.assertRaises(ValidationError):
            pessoa.full_clean()
        pessoa.foto_autorizada = True
        pessoa.full_clean()  # agora passa

    def test_foto_maior_que_3mb(self):
        foto_grande = SimpleUploadedFile("g.jpg", b"0" * (3 * 1024 * 1024 + 1))
        with self.assertRaises(ValidationError):
            validar_tamanho(foto_grande)

    def test_excluir_apaga_a_foto(self):
        foto = FotoGaleria.objects.create(titulo="A", descricao="d", imagem=criar_imagem(), uso_autorizado=True)
        caminho = foto.imagem.name
        self.assertTrue(foto.imagem.storage.exists(caminho))
        foto.delete()
        self.assertFalse(foto.imagem.storage.exists(caminho))

    def test_trocar_foto_apaga_a_antiga(self):
        pessoa = Integrante.objects.create(nome="A", funcao="B", foto=criar_imagem("a.png"), foto_autorizada=True)
        antiga = pessoa.foto.name
        pessoa.foto = criar_imagem("b.png")
        pessoa.save()
        self.assertFalse(pessoa.foto.storage.exists(antiga))
        self.assertTrue(pessoa.foto.storage.exists(pessoa.foto.name))
