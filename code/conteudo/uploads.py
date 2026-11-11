"""
Onde e com que nome as fotos enviadas são guardadas (dentro de code/media/).

O nome original é "limpo" (sem acentos e espaços) e recebe um código aleatório
no final, para nunca sobrescrever outra foto com o mesmo nome.
Ex.: "Aula de Física.JPG" -> media/galeria/2026/aula-de-fisica-3f9a1c2b.jpg
"""
import uuid
from pathlib import Path

from django.utils import timezone
from django.utils.text import slugify


def _nome_seguro(pasta, nome_original):
    caminho = Path(nome_original)
    base = slugify(caminho.stem)[:60] or "imagem"
    extensao = caminho.suffix.lower() or ".jpg"
    return f"{pasta}/{base}-{uuid.uuid4().hex[:8]}{extensao}"


def upload_noticia(instancia, nome):
    return _nome_seguro(f"noticias/{timezone.now():%Y}", nome)


def upload_integrante(instancia, nome):
    return _nome_seguro("equipe", nome)


def upload_galeria(instancia, nome):
    return _nome_seguro(f"galeria/{timezone.now():%Y}", nome)


def upload_depoimento(instancia, nome):
    return _nome_seguro("depoimentos", nome)
