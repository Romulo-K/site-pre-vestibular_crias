# configuração do painel da coordenação (/admin/)
# aqui eu escolho o que aparece em cada lista: colunas, filtros, busca e a prévia das fotos
# os formulários o django monta sozinho a partir do models.py

from django.contrib import admin
from django.utils.html import format_html

from .models import Depoimento, FotoGaleria, Integrante, Noticia

# títulos que aparecem no topo do painel
admin.site.site_header = "Painel — Pré-Vestibular Social ONG Crias"
admin.site.site_title = "Painel ONG Crias"
admin.site.index_title = "O que você quer atualizar no site?"


# mostra uma miniatura da foto no painel (ou um traço se não tiver foto)
def miniatura(foto, altura=60):
    if not foto:
        return "—"
    return format_html('<img src="{}" style="height:{}px;border-radius:8px">', foto.url, altura)


# ---------------- notícias ----------------

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "status", "publicada_em", "autor"]
    list_filter = ["status"]
    search_fields = ["titulo", "resumo"]
    prepopulated_fields = {"slug": ["titulo"]}  # vai preenchendo o slug enquanto digita o título
    readonly_fields = ["previa_capa"]
    fields = ["titulo", "slug", "resumo", "texto", "autor", "capa", "previa_capa", "capa_descricao",
              "status", "publicada_em"]
    actions = ["publicar", "voltar_para_rascunho"]

    @admin.display(description="prévia")
    def previa_capa(self, noticia):
        return miniatura(noticia.capa, 160)

    # ações do menu "Ação" da lista
    @admin.action(description="Publicar as notícias selecionadas")
    def publicar(self, request, selecionadas):
        for noticia in selecionadas:
            noticia.status = "publicada"
            noticia.save()  # o save() coloca a data de publicação
        self.message_user(request, "Notícias publicadas.")

    @admin.action(description="Voltar as notícias selecionadas para rascunho")
    def voltar_para_rascunho(self, request, selecionadas):
        selecionadas.update(status="rascunho")
        self.message_user(request, "Notícias voltaram para rascunho (não aparecem no site).")


# ---------------- equipe ----------------

@admin.register(Integrante)
class IntegranteAdmin(admin.ModelAdmin):
    list_display = ["nome", "funcao", "grupo", "ordem", "ativo"]
    list_editable = ["ordem", "ativo"]  # dá pra mudar direto na lista
    list_filter = ["grupo", "ativo"]
    search_fields = ["nome", "funcao", "disciplina"]
    readonly_fields = ["previa_foto"]
    fields = ["nome", "funcao", "disciplina", "grupo", "biografia", "foto", "previa_foto", "foto_autorizada",
              "ordem", "ativo"]

    @admin.display(description="prévia")
    def previa_foto(self, pessoa):
        return miniatura(pessoa.foto, 180)


# ---------------- galeria ----------------

@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "categoria", "data_atividade"]
    list_filter = ["categoria"]
    search_fields = ["titulo", "legenda", "descricao"]
    readonly_fields = ["previa_imagem"]
    fields = ["imagem", "previa_imagem", "titulo", "descricao", "legenda", "categoria", "data_atividade",
              "uso_autorizado"]

    @admin.display(description="prévia")
    def previa_imagem(self, foto):
        return miniatura(foto.imagem, 220)


# ---------------- depoimentos ----------------

@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ["nome", "turma", "ordem", "ativo"]
    list_editable = ["ordem", "ativo"]
    list_filter = ["ativo"]
    search_fields = ["nome", "turma", "texto"]
    fields = ["nome", "turma", "texto", "foto", "autorizado", "ordem", "ativo"]
