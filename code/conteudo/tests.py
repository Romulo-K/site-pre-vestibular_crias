"""
Testes automáticos do conteúdo (modelos e regras).
Rodar:  python manage.py test
As fotos de teste são criadas numa pasta temporária e apagadas no fim.
"""
import io
import shutil
import tempfile

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from .models import Depoimento, FotoGaleria, Integrante, Noticia
from .validators import validar_tamanho_imagem

PASTA_TEMP = tempfile.mkdtemp()


def imagem_teste(nome="foto.png"):
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), "green").save(buffer, "PNG")
    return SimpleUploadedFile(nome, buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=PASTA_TEMP)
class NoticiaTest(TestCase):
    def test_slug_unico_a_partir_do_titulo(self):
        a = Noticia.objects.create(titulo="Simulado de Outubro", resumo="r", texto="t")
        b = Noticia.objects.create(titulo="Simulado de Outubro", resumo="r", texto="t")
        self.assertEqual(a.slug, "simulado-de-outubro")
        self.assertEqual(b.slug, "simulado-de-outubro-2")

    def test_data_de_publicacao_so_na_primeira_vez(self):
        n = Noticia.objects.create(titulo="N", resumo="r", texto="t")
        self.assertIsNone(n.publicada_em)                     # rascunho: sem data
        n.status = Noticia.Status.PUBLICADA
        n.save()
        data = n.publicada_em
        self.assertIsNotNone(data)
        n.resumo = "editado"
        n.save()
        self.assertEqual(n.publicada_em, data)                # edição não muda a data
        n.status = Noticia.Status.RASCUNHO
        n.save()
        n.status = Noticia.Status.PUBLICADA
        n.save()
        self.assertEqual(n.publicada_em, data)                # republicar também não

    def test_publicadas_nao_inclui_rascunhos(self):
        Noticia.objects.create(titulo="Rascunho", resumo="r", texto="t")
        Noticia.objects.create(titulo="Publicada", resumo="r", texto="t", status=Noticia.Status.PUBLICADA)
        self.assertEqual([n.titulo for n in Noticia.objects.publicadas()], ["Publicada"])

    def test_capa_exige_descricao(self):
        n = Noticia(titulo="N", resumo="r", texto="t", capa=imagem_teste())
        with self.assertRaises(ValidationError):
            n.full_clean()


@override_settings(MEDIA_ROOT=PASTA_TEMP)
class AutorizacaoTest(TestCase):
    def test_foto_de_integrante_exige_autorizacao(self):
        i = Integrante(nome="Ana", funcao="Professora", foto=imagem_teste())
        with self.assertRaises(ValidationError):
            i.full_clean()
        i.foto_autorizada = True
        i.full_clean()  # agora passa

    def test_galeria_exige_autorizacao(self):
        f = FotoGaleria(titulo="Aula", descricao="Alunos em aula", imagem=imagem_teste())
        with self.assertRaises(ValidationError):
            f.full_clean()

    def test_depoimento_exige_autorizacao(self):
        d = Depoimento(nome="Ex-aluno", texto="Muito bom")
        with self.assertRaises(ValidationError):
            d.full_clean()


class ImagemTest(TestCase):
    def test_limite_de_tamanho(self):
        grande = SimpleUploadedFile("g.jpg", b"0" * (3 * 1024 * 1024 + 1))
        with self.assertRaises(ValidationError):
            validar_tamanho_imagem(grande)

    def test_formato_nao_aceito(self):
        i = Integrante(nome="A", funcao="B", foto=SimpleUploadedFile("arquivo.gif", b"GIF89a"), foto_autorizada=True)
        with self.assertRaises(ValidationError):
            i.full_clean()


@override_settings(MEDIA_ROOT=PASTA_TEMP)
class LimpezaDeArquivosTest(TestCase):
    def test_excluir_registro_apaga_a_foto(self):
        with self.captureOnCommitCallbacks(execute=True):
            f = FotoGaleria.objects.create(titulo="A", descricao="d", imagem=imagem_teste(), uso_autorizado=True)
        caminho = f.imagem.name
        self.assertTrue(f.imagem.storage.exists(caminho))
        with self.captureOnCommitCallbacks(execute=True):
            f.delete()
        self.assertFalse(f.imagem.storage.exists(caminho))

    def test_trocar_foto_apaga_a_antiga_depois_de_salvar(self):
        with self.captureOnCommitCallbacks(execute=True):
            i = Integrante.objects.create(nome="A", funcao="B", foto=imagem_teste("a.png"), foto_autorizada=True)
        antiga = i.foto.name
        with self.captureOnCommitCallbacks(execute=True):
            i.foto = imagem_teste("b.png")
            i.save()
        self.assertFalse(i.foto.storage.exists(antiga))
        self.assertTrue(i.foto.storage.exists(i.foto.name))

    def test_nome_do_arquivo_e_seguro(self):
        with self.captureOnCommitCallbacks(execute=True):
            i = Integrante.objects.create(nome="A", funcao="B", foto=imagem_teste("Aula de Física.PNG"), foto_autorizada=True)
        self.assertRegex(i.foto.name, r"^equipe/aula-de-fisica-[0-9a-f]{8}\.png$")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(PASTA_TEMP, ignore_errors=True)
