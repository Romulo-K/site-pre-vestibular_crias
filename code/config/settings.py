# configurações do projeto django
# as coisas secretas (chave, debug etc) ficam no arquivo .env, que não vai pro github
# (copiar o .env.example pra .env e preencher)

import os
from pathlib import Path

from dotenv import load_dotenv

# pasta code/ (onde fica o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# lê o arquivo .env e joga os valores nas variáveis de ambiente
load_dotenv(BASE_DIR / ".env")


# ---------------- parte 1: segurança ----------------

# DEBUG=1 só no meu pc, no servidor fica DEBUG=0
DEBUG = os.getenv("DEBUG", "0") == "1"

# chave secreta do django. no pc pode ficar vazia, no servidor é obrigatória
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "chave-so-pra-testar-no-pc"
    else:
        raise Exception("Faltou colocar a SECRET_KEY no arquivo .env")

# endereços que podem abrir o site (no servidor: prevestibularcrias.pythonanywhere.com)
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()]
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

# sem isso o login do painel dá erro de CSRF quando o site está em https
CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS if host not in ("127.0.0.1", "localhost")]

# no servidor os cookies de login só andam por https
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# enquanto o site está em teste aparece a faixa amarela e o google não indexa
# pra lançar de verdade: SITE_EM_TESTE=0 no .env do servidor
SITE_EM_TESTE = os.getenv("SITE_EM_TESTE", "1") == "1"


# ---------------- parte 2: apps ----------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps que eu criei
    "paginas",   # as páginas do site
    "conteudo",  # notícias, equipe, galeria e depoimentos (+ painel /admin/)
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
        "DIRS": [BASE_DIR / "templates"],  # minha pasta templates/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "paginas.context_processors.site",  # manda o site_em_teste pra todos os templates
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ---------------- parte 3: banco de dados ----------------

# sqlite = o banco é um arquivo só (db.sqlite3), não precisa instalar nada
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# regras pra senha das contas do painel
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------- parte 4: idioma e horário ----------------

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ---------------- parte 5: arquivos ----------------

# static = css, js e imagens fixas do site
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # onde eu edito
STATIC_ROOT = BASE_DIR / "staticfiles"    # onde o collectstatic junta tudo no servidor

# media = fotos que a coordenação manda pelo painel
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
