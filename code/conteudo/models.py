# models = as tabelas do banco
# cada classe vira uma tabela no sqlite:
#   Noticia -> noticias | Integrante -> integrantes | FotoGaleria -> galeria | Depoimento -> depoimentos
#
# mexeu aqui? rodar:
#   python manage.py makemigrations
#   python manage.py migrate

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .validators import validar_foto

TEXTO_AUTORIZACAO = "Confirmo que a pessoa (ou o responsável, se for menor de idade) autorizou a publicação."


# ---------------- notícias ----------------

class Noticia(models.Model):
    STATUS = [
        ("rascunho", "Rascunho"),
        ("publicada", "Publicada"),
    ]

    titulo = models.CharField("título", max_length=200)
    slug = models.SlugField(
        "endereço (slug)", max_length=220, unique=True, blank=True,
        help_text="Parte do endereço da notícia (ex.: simulado-de-outubro). Preenchido automaticamente a partir do título.",
    )
    resumo = models.CharField("resumo", max_length=300, help_text="Uma ou duas frases. Aparece nos cards.")
    texto = models.TextField("texto completo", help_text="Deixe uma linha em branco entre os parágrafos.")
    capa = models.ImageField("imagem de capa", upload_to="noticias/", blank=True, validators=validar_foto,
                             help_text="JPG, PNG ou WebP, até 3 MB.")
    capa_descricao = models.CharField(
        "descrição da capa", max_length=200, blank=True,
        help_text="O que a imagem mostra (para quem usa leitor de tela). Obrigatória se houver capa.",
    )
    autor = models.CharField("autor(a)", max_length=120, blank=True)
    status = models.CharField("status", max_length=10, choices=STATUS, default="rascunho")
    publicada_em = models.DateTimeField(
        "publicada em", null=True, blank=True,
        help_text="Preenchida automaticamente na primeira publicação. Edições posteriores não mudam esta data.",
    )
    criada_em = models.DateTimeField("criada em", auto_now_add=True)
    atualizada_em = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        db_table = "noticias"
        verbose_name = "notícia"
        verbose_name_plural = "notícias"
        ordering = ["-publicada_em", "-criada_em"]  # mais nova primeiro
        indexes = [models.Index(fields=["status", "-publicada_em"], name="noticias_status_data_idx")]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        # endereço da notícia no site (é o que o botão "Ver no site" do painel usa)
        return reverse("paginas:noticia", args=[self.slug])

    def clean(self):
        # se tem foto de capa, tem que ter a descrição dela
        if self.capa and not self.capa_descricao.strip():
            raise ValidationError({"capa_descricao": "Descreva a imagem de capa."})

    def save(self, *args, **kwargs):
        # cria o endereço a partir do título. se já existir, coloca -2, -3...
        if not self.slug:
            base = slugify(self.titulo)[:200] or "noticia"
            slug = base
            numero = 2
            while Noticia.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{numero}"
                numero += 1
            self.slug = slug

        # a data de publicação só é colocada na primeira vez que publica
        if self.status == "publicada" and self.publicada_em is None:
            self.publicada_em = timezone.now()

        super().save(*args, **kwargs)


# ---------------- equipe ----------------

class Integrante(models.Model):
    GRUPOS = [
        ("coordenacao", "Coordenação"),
        ("professores", "Professores"),
        ("apoio", "Equipe de apoio"),
    ]

    nome = models.CharField("nome", max_length=120)
    funcao = models.CharField("função", max_length=120, help_text="Ex.: Professor(a), Coordenadora pedagógica.")
    disciplina = models.CharField("disciplina", max_length=80, blank=True, help_text="Ex.: Matemática (se houver).")
    biografia = models.TextField("descrição curta", blank=True)
    grupo = models.CharField("grupo", max_length=12, choices=GRUPOS, default="professores")
    foto = models.ImageField("foto", upload_to="equipe/", blank=True, validators=validar_foto,
                             help_text="Somente com autorização. JPG, PNG ou WebP, até 3 MB.")
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
        # não deixa salvar foto sem marcar a autorização
        if self.foto and not self.foto_autorizada:
            raise ValidationError({"foto_autorizada": "Confirme a autorização para publicar a foto."})


# ---------------- galeria ----------------

class FotoGaleria(models.Model):
    CATEGORIAS = [
        ("aulas", "Aulas"),
        ("palestras", "Palestras"),
        ("simulados", "Simulados"),
        ("convivencia", "Convivência"),
        ("passeios", "Passeios"),
        ("outros", "Outros"),
    ]

    titulo = models.CharField("título", max_length=150)
    imagem = models.ImageField("imagem", upload_to="galeria/", validators=validar_foto,
                               help_text="JPG, PNG ou WebP, até 3 MB.")
    descricao = models.CharField(
        "descrição da imagem", max_length=200,
        help_text="O que a foto mostra (para quem usa leitor de tela). Ex.: Alunos fazendo simulado em sala.",
    )
    legenda = models.CharField("legenda", max_length=200, blank=True)
    categoria = models.CharField("categoria", max_length=12, choices=CATEGORIAS, default="aulas")
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


# ---------------- depoimentos ----------------

class Depoimento(models.Model):
    nome = models.CharField("nome", max_length=120)
    turma = models.CharField("turma / vínculo", max_length=120, blank=True, help_text="Ex.: Ex-aluna, turma de 2024.")
    texto = models.TextField("depoimento", max_length=800)
    foto = models.ImageField("foto", upload_to="depoimentos/", blank=True, validators=validar_foto,
                             help_text="Opcional. Sem foto, aparece um ícone.")
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
