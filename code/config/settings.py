"""
Configurações do projeto Django — Pré-Vestibular Social ONG Crias.

Valores secretos ou que mudam entre o seu computador e o servidor ficam no
arquivo .env (copie .env.example para .env). O .env NUNCA vai para o GitHub.

Documentação: https://docs.djangoproject.com/pt-br/5.2/ref/settings/
"""
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Pasta "code/" (onde está o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------------------
# Leitura do arquivo .env (sem bibliotecas extras)
# Formato: uma linha por variável, CHAVE=valor. Linhas com # são comentários.
# ----------------------------------------------------------------------
def carregar_env(caminho):
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


carregar_env(BASE_DIR / ".env")


def env_bool(nome, padrao=False):
    return os.environ.get(nome, str(padrao)).strip().lower() in ("1", "true", "sim", "yes")


# ----------------------------------------------------------------------
# Segurança
# ----------------------------------------------------------------------
# DEBUG=1 só no seu computador. No servidor (Etapa 11) será DEBUG=0.
DEBUG = env_bool("DEBUG", False)

# Chave usada pelo Django para assinar sessões e formulários. Precisa ser secreta.
CHAVE_DE_DESENVOLVIMENTO = "chave-insegura-apenas-para-desenvolvimento-local"
SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = CHAVE_DE_DESENVOLVIMENTO
    else:
        raise ImproperlyConfigured("Defina SECRET_KEY no arquivo .env (veja .env.example).")

# Endereços que podem acessar o site. Ex.: "precrias.pythonanywhere.com"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


# ----------------------------------------------------------------------
# Aplicativos
# ----------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps do projeto
    "paginas",    # páginas públicas do site
    "conteudo",   # notícias, equipe, galeria e depoimentos + painel /admin/
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # templates/ na pasta code/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ----------------------------------------------------------------------
# Banco de dados: SQLite (um arquivo, db.sqlite3, fora do GitHub)
# ----------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ----------------------------------------------------------------------
# Senhas (regras para a conta da coordenação no Admin)
# ----------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ----------------------------------------------------------------------
# Idioma e fuso horário
# ----------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ----------------------------------------------------------------------
# Arquivos estáticos (CSS, JS, imagens do site) e de mídia (fotos enviadas)
# ----------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]   # onde você edita os arquivos
STATIC_ROOT = BASE_DIR / "staticfiles"     # onde o "collectstatic" junta tudo no servidor

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"            # fotos enviadas pelo painel /admin/

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
