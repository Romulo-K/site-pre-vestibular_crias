# bd.py - script do banco de dados do site
#
# o banco é criado pelo django a partir do code/conteudo/models.py
# esse script faz duas coisas:
#   1) gera o bd/schema.sql com o SQL que o django usa pra criar as tabelas
#   2) mostra quantos registros tem em cada tabela (usando SQL direto no sqlite)
#
# como usar (na pasta do projeto, com o .venv ativado):
#   python bd/bd.py          -> gera o schema.sql
#   python bd/bd.py contar   -> mostra quantos registros tem no banco

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

PASTA_BD = Path(__file__).parent
PASTA_CODE = PASTA_BD.parent / "code"
ARQUIVO_BANCO = PASTA_CODE / "db.sqlite3"
ARQUIVO_SQL = PASTA_BD / "schema.sql"
TABELAS = ["noticias", "integrantes", "galeria", "depoimentos"]


# ---------------- parte 1: gerar o schema.sql ----------------

def gerar_schema():
    # pega o nome de cada migration (0001_initial, 0002_..., etc)
    pasta_migrations = PASTA_CODE / "conteudo" / "migrations"
    migrations = sorted(arquivo.stem for arquivo in pasta_migrations.glob("0*.py"))

    sql = "-- SQL das tabelas do site (gerado pelo bd/bd.py, não editar na mão)\n"
    sql += "-- tabelas: noticias, integrantes, galeria, depoimentos\n\n"

    for nome in migrations:
        # pede pro django mostrar o SQL da migration (comando sqlmigrate)
        resultado = subprocess.run(
            [sys.executable, "manage.py", "sqlmigrate", "conteudo", nome],
            cwd=PASTA_CODE, capture_output=True, text=True,
            env={**os.environ, "DEBUG": "1"},  # pra funcionar mesmo sem o .env
        )
        if resultado.returncode != 0:
            print("Deu erro ao gerar o SQL:")
            print(resultado.stderr)
            return
        sql += f"-- migration {nome}\n{resultado.stdout}\n"

    ARQUIVO_SQL.write_text(sql, encoding="utf-8")
    print(f"bd/schema.sql gerado ({len(migrations)} migration(s))")


# ---------------- parte 2: contar os registros ----------------

def contar():
    if not ARQUIVO_BANCO.exists():
        print("Não achei o banco. Rode antes, dentro da pasta code: python manage.py migrate")
        return

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    cursor = conexao.cursor()

    for tabela in TABELAS:
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        total = cursor.fetchone()[0]
        print(f"{tabela}: {total} registro(s)")

    cursor.execute("SELECT COUNT(*) FROM noticias WHERE status = 'publicada'")
    print(f"(notícias publicadas: {cursor.fetchone()[0]})")

    conexao.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "contar":
        contar()
    else:
        gerar_schema()
