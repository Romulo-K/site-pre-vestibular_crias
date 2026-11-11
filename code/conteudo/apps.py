from django.apps import AppConfig


class ConteudoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "conteudo"
    verbose_name = "Conteúdo do site"

    def ready(self):
        from . import signals  # noqa: F401  (liga a limpeza automática de fotos)
