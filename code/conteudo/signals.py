"""
Limpeza automática de arquivos de imagem.

O Django apaga o REGISTRO do banco, mas não o ARQUIVO da foto. Estas funções
cuidam disso:
- ao excluir um registro, a foto dele é apagada do disco;
- ao trocar uma foto, a antiga só é apagada DEPOIS que a nova foi salva
  com sucesso (transaction.on_commit), para nunca ficar sem nenhuma.
"""
from django.db import transaction
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Depoimento, FotoGaleria, Integrante, Noticia

CAMPOS_DE_IMAGEM = {
    Noticia: "capa",
    Integrante: "foto",
    FotoGaleria: "imagem",
    Depoimento: "foto",
}


def _apagar_arquivo(arquivo):
    if arquivo and arquivo.name:
        arquivo.storage.delete(arquivo.name)


@receiver(post_delete)
def apagar_foto_ao_excluir(sender, instance, **kwargs):
    campo = CAMPOS_DE_IMAGEM.get(sender)
    if campo:
        arquivo = getattr(instance, campo)
        transaction.on_commit(lambda: _apagar_arquivo(arquivo))


@receiver(pre_save)
def apagar_foto_antiga_ao_trocar(sender, instance, **kwargs):
    campo = CAMPOS_DE_IMAGEM.get(sender)
    if not campo or not instance.pk:
        return
    try:
        antigo = getattr(sender.objects.get(pk=instance.pk), campo)
    except sender.DoesNotExist:
        return
    novo = getattr(instance, campo)
    if antigo and antigo.name and antigo.name != (novo.name if novo else None):
        transaction.on_commit(lambda: _apagar_arquivo(antigo))
