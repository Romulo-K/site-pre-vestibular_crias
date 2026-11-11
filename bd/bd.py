#!/usr/bin/env python3
"""
bd.py — documentação do banco de dados do site (Python + SQL).

O banco é criado pelo Django a partir dos modelos em code/conteudo/models.py.
Este script mostra e registra o SQL que o Django usa:

    python bd/bd.py            gera bd/schema.sql (o SQL das tabelas do site)
    python bd/bd.py --resumo   mostra no terminal as tabelas e colunas
    python bd/bd.py --contar   mostra quantos registros há em cada tabela (banco local)

Rode na raiz do repositório, com o ambiente virtual ativo (source .venv/bin/activate).
Sempre que mudar os modelos: makemigrations, migrate e depois  python bd/bd.py.
"""
import io
import os
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_CODE = RAIZ / "code"
ARQUIVO_SQL = Path(__file__).resolve().parent / "schema.sql"
APP = "conteudo"

# Prepara o Django (sem servidor): o script só lê os modelos e as migrations.
sys.path.insert(0, str(PASTA_CODE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DEBUG", "1")
try:
    import django
except ImportError:
    sys.exit("Django não encontrado. Ative o ambiente virtual:  source .venv/bin/activate")
django.setup()

from django.apps import apps                                     # noqa: E402
from django.core.management import call_command                  # noqa: E402
from django.db import connection                                 # noqa: E402
from django.db.migrations.loader import MigrationLoader          # noqa: E402


def migrations_do_app():
    loader = MigrationLoader(connection, ignore_no_migrations=True)
    nomes = [nome for (app, nome) in loader.graph.leaf_nodes() if app == APP]
    if not nomes:
        return []
    plano = loader.graph.forwards_plan((APP, nomes[0]))
    return [nome for (app, nome) in plano if app == APP]


def gerar_sql():
    partes = []
    for nome in migrations_do_app():
        saida = io.StringIO()
        call_command("sqlmigrate", APP, nome, stdout=saida)
        partes.append(f"-- ---------------------------------------------------------------\n"
                      f"-- Migration {APP}.{nome}\n"
                      f"-- ---------------------------------------------------------------\n"
                      + saida.getvalue().strip() + "\n")
    cabecalho = (
        "-- =================================================================\n"
        "-- schema.sql — SQL das tabelas do site Pré-Vestibular Social ONG Crias\n"
        f"-- Gerado por bd/bd.py em {datetime.now():%d/%m/%Y %H:%M} (Django {django.get_version()}, "
        f"banco {connection.vendor}).\n"
        "-- NÃO edite à mão: mude code/conteudo/models.py e gere de novo.\n"
        "-- Tabelas: noticias, integrantes, galeria, depoimentos.\n"
        "-- (As tabelas de login/usuários são do próprio Django: auth_*, django_*.)\n"
        "-- =================================================================\n\n"
    )
    ARQUIVO_SQL.write_text(cabecalho + "\n".join(partes), encoding="utf-8")
    print(f"OK: {ARQUIVO_SQL.relative_to(RAIZ)} gerado com {len(partes)} migration(s).")


def resumo():
    for modelo in apps.get_app_config(APP).get_models():
        meta = modelo._meta
        print(f"\nTabela {meta.db_table}  ({meta.verbose_name_plural})")
        for campo in meta.concrete_fields:
            tipo = campo.db_type(connection) or "?"
            obrigatorio = "" if (campo.null or campo.blank) else "  obrigatório"
            print(f"  {campo.column:<18} {tipo:<16} {campo.verbose_name}{obrigatorio}")


def contar():
    from django.db.utils import OperationalError
    try:
        for modelo in apps.get_app_config(APP).get_models():
            print(f"  {modelo._meta.db_table:<12} {modelo.objects.count():>5} registro(s)")
    except OperationalError:
        sys.exit("Banco ainda não criado. Rode:  cd code && python manage.py migrate")


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    elif "--contar" in sys.argv:
        contar()
    else:
        gerar_sql()
