"""
Modelos do conteúdo do site. Cada classe vira uma TABELA no banco SQLite.

    Noticia      -> tabela "noticias"
    Integrante   -> tabela "integrantes"   (equipe)
    FotoGaleria  -> tabela "galeria"
    Depoimento   -> tabela "depoimentos"

Depois de mudar este arquivo, rode:
    python manage.py makemigrations   (o Django escreve o "plano" da mudança)
    python manage.py migrate          (o Django aplica no banco)
O SQL gerado fica documentado em bd/schema.sql (python bd/bd.py).
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .uploads import upload_depoimento, upload_galeria, upload_integrante, upload_noticia
from .validators import VALIDADORES_IMAGEM

TEXTO_AUTORIZACAO = (
    "Confirmo que a pessoa (ou o responsável, se for menor de idade) autorizou a publicação."
)


# ======================================================================
# NOTÍCIAS
# ======================================================================
class NoticiaQuerySet(models.QuerySet):
    def publicadas(self):
        """Só o que o público pode ver: status 'publicada'."""
        return self.filter(status=Noticia.Status.PUBLICADA)


class Noticia(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        PUBLICADA = "publicada", "Publicada"

    titulo = models.CharField("título", max_length=200)
    slug = models.SlugField(
        "endereço (slug)", max_length=220, unique=True, blank=True,
        help_text="Parte do endereço da notícia (ex.: simulado-de-outubro). Preenchido automaticamente a partir do título.",
    )
    resumo = models.CharField("resumo", max_length=300, help_text="Uma ou duas frases. Aparece nos cards.")
    texto = models.TextField("texto completo", help_text="Deixe uma linha em branco entre os parágrafos.")
    capa = models.ImageField(
        "imagem de capa", upload_to=upload_noticia, blank=True, validators=VALIDADORES_IMAGEM,
        help_text="JPG, PNG ou WebP, até 3 MB.",
    )
    capa_descricao = models.CharField(
        "descrição da capa", max_length=200, blank=True,
        help_text="O que a imagem mostra (para quem usa leitor de tela). Obrigatória se houver capa.",
    )
    autor = models.CharField("autor(a)", max_length=120, blank=True)
    status = models.CharField("status", max_length=10, choices=Status.choices, default=Status.RASCUNHO)
    publicada_em = models.DateTimeField(
        "publicada em", null=True, blank=True,
        help_text="Preenchida automaticamente na primeira publicação. Edições posteriores não mudam esta data.",
    )
    criada_em = models.DateTimeField("criada em", auto_now_add=True)
    atualizada_em = models.DateTimeField("atualizada em", auto_now=True)

    objects = NoticiaQuerySet.as_manager()

    class Meta:
        db_table = "noticias"
        verbose_name = "notícia"
        verbose_name_plural = "notícias"
        ordering = ["-publicada_em", "-criada_em"]
        indexes = [models.Index(fields=["status", "-publicada_em"], name="noticias_status_data_idx")]

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.capa and not self.capa_descricao.strip():
            raise ValidationError({"capa_descricao": "Descreva a imagem de capa."})

    def save(self, *args, **kwargs):
        # Endereço único a partir do título (ex.: "simulado", "simulado-2", ...)
        if not self.slug:
            base = slugify(self.titulo)[:200] or "noticia"
            slug, n = base, 2
            while Noticia.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        # Data de publicação: só na PRIMEIRA vez que vira "publicada"
        if self.status == self.Status.PUBLICADA and self.publicada_em is None:
            self.publicada_em = timezone.now()
        super().save(*args, **kwargs)


# ======================================================================
# EQUIPE
# ======================================================================
class Integrante(models.Model):
    class Grupo(models.TextChoices):
        COORDENACAO = "coordenacao", "Coordenação"
        PROFESSORES = "professores", "Professores"
        APOIO = "apoio", "Equipe de apoio"

    nome = models.CharField("nome", max_length=120)
    funcao = models.CharField("função", max_length=120, help_text="Ex.: Professor(a), Coordenadora pedagógica.")
    disciplina = models.CharField("disciplina", max_length=80, blank=True, help_text="Ex.: Matemática (se houver).")
    biografia = models.TextField("descrição curta", blank=True)
    grupo = models.CharField("grupo", max_length=12, choices=Grupo.choices, default=Grupo.PROFESSORES)
    foto = models.ImageField(
        "foto", upload_to=upload_integrante, blank=True, validators=VALIDADORES_IMAGEM,
        help_text="Somente com autorização. JPG, PNG ou WebP, até 3 MB.",
    )
    foto_autorizada = models.BooleanField(TEXTO_AUTORIZACAO, default=False)
    ordem = models.PositiveIntegerField("ordem de exibição", default=0, help_text="Números menores aparecem primeiro.")
    ativo = models.BooleanField("aparece no site", default=True,
                                help_text="Desmarque para esconder do site sem apagar os dados.")
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        db_table = "integrantes"
        verbose_name = "integrante da equipe"
        verbose_name_plural = "equipe"
        ordering = ["ordem", "nome"]
        indexes = [models.Index(fields=["ativo", "grupo", "ordem"], name="integrantes_ativo_grupo_idx")]

    def __str__(self):
        return f"{self.nome} ({self.funcao})"

    def clean(self):
        if self.foto and not self.foto_autorizada:
            raise ValidationError({"foto_autorizada": "Confirme a autorização para publicar a foto."})


# ======================================================================
# GALERIA
# ======================================================================
class FotoGaleria(models.Model):
    class Categoria(models.TextChoices):
        AULAS = "aulas", "Aulas"
        PALESTRAS = "palestras", "Palestras"
        SIMULADOS = "simulados", "Simulados"
        CONVIVENCIA = "convivencia", "Convivência"
        PASSEIOS = "passeios", "Passeios"
        OUTROS = "outros", "Outros"

    titulo = models.CharField("título", max_length=150)
    imagem = models.ImageField("imagem", upload_to=upload_galeria, validators=VALIDADORES_IMAGEM,
                               help_text="JPG, PNG ou WebP, até 3 MB.")
    descricao = models.CharField(
        "descrição da imagem", max_length=200,
        help_text="O que a foto mostra (para quem usa leitor de tela). Ex.: Alunos fazendo simulado em sala.",
    )
    legenda = models.CharField("legenda", max_length=200, blank=True)
    categoria = models.CharField("categoria", max_length=12, choices=Categoria.choices, default=Categoria.AULAS)
    data_atividade = models.DateField("data da atividade", null=True, blank=True)
    uso_autorizado = models.BooleanField(
        "Confirmo que as pessoas identificáveis na foto (ou responsáveis) autorizaram a publicação.",
        default=False,
    )
    criada_em = models.DateTimeField("enviada em", auto_now_add=True)

    class Meta:
        db_table = "galeria"
        verbose_name = "foto da galeria"
        verbose_name_plural = "galeria"
        ordering = ["-data_atividade", "-criada_em"]

    def __str__(self):
        return self.titulo

    def clean(self):
        if not self.uso_autorizado:
            raise ValidationError({"uso_autorizado": "Confirme a autorização para publicar a foto."})


# ======================================================================
# DEPOIMENTOS
# ======================================================================
class Depoimento(models.Model):
    nome = models.CharField("nome", max_length=120)
    turma = models.CharField("turma / vínculo", max_length=120, blank=True,
                             help_text="Ex.: Ex-aluna, turma de 2024.")
    texto = models.TextField("depoimento", max_length=800)
    foto = models.ImageField(
        "foto", upload_to=upload_depoimento, blank=True, validators=VALIDADORES_IMAGEM,
        help_text="Opcional. Sem foto, aparece um ícone.",
    )
    autorizado = models.BooleanField(TEXTO_AUTORIZACAO, default=False)
    ativo = models.BooleanField("aparece no site", default=True)
    ordem = models.PositiveIntegerField("ordem de exibição", default=0)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        db_table = "depoimentos"
        verbose_name = "depoimento"
        verbose_name_plural = "depoimentos"
        ordering = ["ordem", "-criado_em"]

    def __str__(self):
        return f"{self.nome}: {self.texto[:40]}"

    def clean(self):
        if not self.autorizado:
            raise ValidationError({"autorizado": "Só publique depoimentos autorizados pela pessoa."})
