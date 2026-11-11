"""
Regras para as imagens enviadas pelo painel.

- Formatos aceitos: JPG, PNG e WebP.
- Tamanho máximo: 3 MB por foto (fotos de celular costumam ser maiores:
  reduza antes em https://squoosh.app, por exemplo).
O Django (com a biblioteca Pillow) também confere se o arquivo é mesmo uma imagem.
"""
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

TAMANHO_MAXIMO_MB = 3

validar_formato_imagem = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png", "webp"],
    message="Formato não aceito. Envie uma imagem JPG, PNG ou WebP.",
)


def validar_tamanho_imagem(arquivo):
    if arquivo.size > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ValidationError(
            f"A imagem tem {arquivo.size / 1024 / 1024:.1f} MB. O máximo é {TAMANHO_MAXIMO_MB} MB: "
            "reduza a foto antes de enviar."
        )


VALIDADORES_IMAGEM = [validar_formato_imagem, validar_tamanho_imagem]
