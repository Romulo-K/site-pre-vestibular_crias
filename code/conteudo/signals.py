# apaga o arquivo da foto quando não precisa mais dele
# (o django apaga o registro do banco, mas a foto ficava esquecida na pasta media/
#  e o espaço no pythonanywhere é pequeno, só 512 MB)

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Depoimento, FotoGaleria, Integrante, Noticia

# qual é o campo de foto de cada tabela
CAMPO_FOTO = {
    Noticia: "capa",
    Integrante: "foto",
    FotoGaleria: "imagem",
    Depoimento: "foto",
}


# quando um registro é excluído, apaga a foto dele
@receiver(post_delete)
def apagar_foto_excluida(sender, instance, **kwargs):
    if sender not in CAMPO_FOTO:
        return
    foto = getattr(instance, CAMPO_FOTO[sender])
    if foto:
        foto.delete(save=False)


# quando trocam a foto de um registro, apaga a foto antiga
@receiver(pre_save)
def apagar_foto_trocada(sender, instance, **kwargs):
    if sender not in CAMPO_FOTO or not instance.pk:
        return  # registro novo, não tem foto antiga

    campo = CAMPO_FOTO[sender]
    antigo = sender.objects.filter(pk=instance.pk).first()
    if antigo is None:
        return

    foto_antiga = getattr(antigo, campo)
    foto_nova = getattr(instance, campo)
    if foto_antiga and foto_antiga.name != foto_nova.name:
        foto_antiga.delete(save=False)
