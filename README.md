# Pré-Vestibular Social ONG Crias — Site

Site feito para o Pré-Vestibular Social ONG Crias, como projeto de extensão da faculdade.

🔗 **Site no ar:** https://prevestibularcrias.pythonanywhere.com

## O que foi usado

- **Python + Django 5.2** → o site e o painel da coordenação (`/admin/`)
- **SQLite** → o banco de dados (um arquivo só, `code/db.sqlite3`)
- **HTML, CSS e JavaScript** → visual, menu do celular e galeria de fotos
- **PythonAnywhere** → onde o site fica hospedado
- **Google Forms, Classroom, Drive e Meet** → inscrições e área do aluno (o site só leva até eles)

## O que o site tem

- 8 páginas: Início, O Projeto, Atividades, Equipe, Alunos, Voluntários, Notícias e Contato
- Painel em `/admin/` onde a coordenação publica notícias, equipe, fotos da galeria e depoimentos sem mexer no código
- Os links dos formulários, do Classroom, Drive e Meet e os contatos também são trocados pelo painel ("Links e contatos do site")
- Notícia em rascunho não aparece no site, só depois de publicada
- Funciona no celular

## Como está organizado

```
bd/            banco de dados: bd.py (script em python) e schema.sql (o SQL das tabelas)
code/          o projeto django
  config/      configurações (settings.py) e endereços principais (urls.py)
  paginas/     as páginas do site (views.py e urls.py)
  conteudo/    as tabelas do banco (models.py) e o painel (admin.py)
  templates/   o HTML das páginas (base.html tem o cabeçalho e o rodapé)
  static/      css, javascript e imagens
PUBLICACAO.md  passo a passo de como coloquei o site no PythonAnywhere
```

## Como rodar no computador

Primeira vez:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
cd code
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser   # cria o login do painel
python manage.py runserver
```

Depois é só abrir http://127.0.0.1:8000 (e o painel em http://127.0.0.1:8000/admin/).

Nas outras vezes:

```bash
source .venv/bin/activate
cd code
python manage.py runserver
```

Testes: `python manage.py test` (dentro da pasta `code`).

## Banco de dados

As tabelas são criadas pelo Django a partir do `code/conteudo/models.py`.
O SQL delas fica salvo em `bd/schema.sql`. Mais detalhes em [`bd/README.md`](bd/README.md).
