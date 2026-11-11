# regras pras fotos que a coordenação manda pelo painel:
# só jpg, png ou webp e no máximo 3 MB
# (o django com o pillow também confere se o arquivo é imagem de verdade)

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

TAMANHO_MAXIMO_MB = 3


def validar_tamanho(arquivo):
    if arquivo.size > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ValidationError(f"A imagem passou de {TAMANHO_MAXIMO_MB} MB. Diminua a foto antes de enviar.")


validar_formato = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png", "webp"],
    message="Formato não aceito. Envie uma imagem JPG, PNG ou WebP.",
)

# lista usada nos campos de foto do models.py
validar_foto = [validar_formato, validar_tamanho]
