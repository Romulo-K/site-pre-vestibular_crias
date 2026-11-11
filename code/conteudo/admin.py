"""
Painel da coordenação (Django Admin) — endereço /admin/.

Aqui definimos, para cada tipo de conteúdo, quais colunas aparecem na lista,
os filtros, a busca e a pré-visualização das fotos. Os formulários de edição
são gerados automaticamente pelo Django a partir dos modelos (models.py).
"""
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Depoimento, FotoGaleria, Integrante, Noticia

# Títulos do painel
admin.site.site_header = "Painel — Pré-Vestibular Social ONG Crias"
admin.site.site_title = "Painel ONG Crias"
admin.site.index_title = "O que você quer atualizar no site?"


def miniatura(arquivo, altura=60):
    """Mostra uma prévia pequena da foto (ou um traço se não houver)."""
    if not arquivo:
        return "—"
    return format_html(
        '<img src="{}" alt="" style="height:{}px;width:auto;max-width:120px;border-radius:8px;object-fit:cover">',
        arquivo.url, altura,
    )


# ----------------------------------------------------------------------
# Notícias
# ----------------------------------------------------------------------
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "status", "publicada_em", "autor", "previa_lista"]
    list_filter = ["status", "publicada_em"]
    search_fields = ["titulo", "resumo", "texto"]
    date_hierarchy = "publicada_em"
    prepopulated_fields = {"slug": ["titulo"]}
    readonly_fields = ["previa_capa", "criada_em", "atualizada_em"]
    actions = ["publicar", "voltar_para_rascunho"]
    fieldsets = [
        (None, {"fields": ["titulo", "slug", "resumo", "texto", "autor"]}),
        ("Imagem de capa", {"fields": ["capa", "previa_capa", "capa_descricao"]}),
        ("Publicação", {
            "fields": ["status", "publicada_em", "criada_em", "atualizada_em"],
            "description": "Rascunhos não aparecem no site. Ao publicar pela primeira vez, a data é preenchida sozinha.",
        }),
    ]

    @admin.display(description="capa")
    def previa_lista(self, obj):
        return miniatura(obj.capa, 40)

    @admin.display(description="prévia")
    def previa_capa(self, obj):
        return miniatura(obj.capa, 160)

    @admin.action(description="Publicar as notícias selecionadas")
    def publicar(self, request, queryset):
        total = 0
        for noticia in queryset.exclude(status=Noticia.Status.PUBLICADA):
            noticia.status = Noticia.Status.PUBLICADA
            noticia.save()  # save() preenche a data da primeira publicação
            total += 1
        self.message_user(request, f"{total} notícia(s) publicada(s).", messages.SUCCESS)

    @admin.action(description="Voltar as notícias selecionadas para rascunho")
    def voltar_para_rascunho(self, request, queryset):
        total = queryset.update(status=Noticia.Status.RASCUNHO)
        self.message_user(request, f"{total} notícia(s) agora em rascunho (não aparecem no site).", messages.SUCCESS)


# ----------------------------------------------------------------------
# Equipe
# ----------------------------------------------------------------------
@admin.register(Integrante)
class IntegranteAdmin(admin.ModelAdmin):
    list_display = ["previa_lista", "nome", "funcao", "grupo", "ordem", "ativo"]
    list_display_links = ["previa_lista", "nome"]
    list_editable = ["ordem", "ativo"]
    list_filter = ["grupo", "ativo"]
    search_fields = ["nome", "funcao", "disciplina"]
    readonly_fields = ["previa_foto"]
    fieldsets = [
        (None, {"fields": ["nome", "funcao", "disciplina", "grupo", "biografia"]}),
        ("Foto", {"fields": ["foto", "previa_foto", "foto_autorizada"]}),
        ("Exibição no site", {"fields": ["ordem", "ativo"]}),
    ]

    @admin.display(description="foto")
    def previa_lista(self, obj):
        return miniatura(obj.foto, 48)

    @admin.display(description="prévia")
    def previa_foto(self, obj):
        return miniatura(obj.foto, 180)


# ----------------------------------------------------------------------
# Galeria
# ----------------------------------------------------------------------
@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ["previa_lista", "titulo", "categoria", "data_atividade", "criada_em"]
    list_display_links = ["previa_lista", "titulo"]
    list_filter = ["categoria", "data_atividade"]
    search_fields = ["titulo", "legenda", "descricao"]
    readonly_fields = ["previa_imagem"]
    fields = ["imagem", "previa_imagem", "titulo", "descricao", "legenda", "categoria", "data_atividade", "uso_autorizado"]

    @admin.display(description="foto")
    def previa_lista(self, obj):
        return miniatura(obj.imagem, 48)

    @admin.display(description="prévia")
    def previa_imagem(self, obj):
        return miniatura(obj.imagem, 220)


# ----------------------------------------------------------------------
# Depoimentos
# ----------------------------------------------------------------------
@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ["nome", "turma", "resumo_texto", "ordem", "ativo"]
    list_editable = ["ordem", "ativo"]
    list_filter = ["ativo"]
    search_fields = ["nome", "turma", "texto"]
    readonly_fields = ["previa_foto"]
    fields = ["nome", "turma", "texto", "foto", "previa_foto", "autorizado", "ordem", "ativo"]

    @admin.display(description="depoimento")
    def resumo_texto(self, obj):
        return obj.texto[:80] + ("…" if len(obj.texto) > 80 else "")

    @admin.display(description="prévia")
    def previa_foto(self, obj):
        return miniatura(obj.foto, 120)
