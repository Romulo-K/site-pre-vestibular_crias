from django.apps import AppConfig


class ConteudoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "conteudo"
    verbose_name = "Conteúdo do site"

    def ready(self):
        # liga o arquivo signals.py (que apaga as fotos que não são mais usadas)
        from . import signals  # noqa: F401
