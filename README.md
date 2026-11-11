# Pré-Vestibular Social ONG Crias — Site institucional

Projeto de extensão universitária. Site feito em Django.

## Tecnologias

- **Django 5.2** (Python) — páginas montadas no servidor e painel da coordenação (Django Admin)
- **SQLite** — banco de dados (um arquivo, `code/db.sqlite3`, fora do GitHub)
- HTML, CSS e JavaScript — visual e interações (menu, galeria)
- Google Forms, Classroom, Drive e Meet — serviços externos (links em `code/static/js/config.js`)
- Hospedagem prevista: PythonAnywhere

## Estrutura

```
site-pre-vestibular_crias/
├── bd/                      Banco de dados: bd.py (Python), schema.sql (SQL) e dicionário de dados
├── code/                    Projeto Django
│   ├── manage.py            Comandos do Django (rodar, migrar, testar)
│   ├── requirements.txt     Bibliotecas (Django e Pillow)
│   ├── .env.example         Modelo das configurações locais/secretas
│   ├── config/              Configurações do projeto (settings.py, urls.py)
│   ├── paginas/             App das páginas públicas (urls.py, views.py, tests.py)
│   ├── conteudo/            App do conteúdo: modelos (tabelas), painel /admin/, testes
│   ├── templates/
│   │   ├── base.html        Cabeçalho, menu, rodapé e scripts (comum a todas as páginas)
│   │   ├── includes/        Pedaços reaproveitados (ícones, chamada "Quer fazer parte?")
│   │   ├── admin/           Cores da ONG no painel /admin/
│   │   └── paginas/         inicio, projeto, atividades, equipe, alunos, voluntarios, noticias, contato
│   └── static/
│       ├── css/style.css    Estilos + design system (variáveis no topo)
│       ├── js/              config.js (links), main.js (menu), render.js (cards), galeria.js
│       ├── data/            Conteúdo provisório (até a Etapa 8 trazer do banco)
│       └── assets/          logo, fontes, imagens
└── evidences/
```

## Como rodar no seu computador (Linux)

Na primeira vez:

```bash
cd ~/site-pre-vestibular_crias
python3 -m venv .venv               # cria o ambiente virtual
source .venv/bin/activate           # ativa (aparece "(.venv)" no terminal)
pip install -r code/requirements.txt
cd code
cp .env.example .env                # configurações locais
python manage.py migrate            # cria o banco SQLite
python manage.py runserver          # abre o site em http://127.0.0.1:8000
```

Nas próximas vezes:

```bash
cd ~/site-pre-vestibular_crias
source .venv/bin/activate
cd code
python manage.py runserver
```

Para parar o servidor: `Ctrl + C`. Para rodar os testes: `python manage.py test`.

## Onde está o Python

| Arquivo | O que faz |
|---|---|
| `code/config/settings.py` | Configurações (banco, idioma, segurança, arquivos) |
| `code/config/urls.py`, `code/paginas/urls.py` | Endereços do site |
| `code/paginas/views.py` | Monta cada página |
| `code/conteudo/models.py` | Tabelas do banco (notícias, equipe, galeria, depoimentos) |
| `code/conteudo/admin.py` | Painel da coordenação |
| `code/conteudo/validators.py`, `uploads.py`, `signals.py` | Regras das fotos (formato, tamanho, nome, limpeza) |
| `code/*/tests.py` | Testes automáticos (`python manage.py test`) |
| `bd/bd.py` | Gera o SQL do banco em `bd/schema.sql` |

## Painel da coordenação (/admin/)

Criar a conta da coordenação (uma vez, dentro de `code/`):

```bash
python manage.py createsuperuser
```

Depois, com o servidor rodando, acesse `http://127.0.0.1:8000/admin/`. Pelo painel dá para criar,
editar e excluir **notícias** (rascunho ou publicada), **equipe**, **galeria** e **depoimentos**, com fotos.
A senha é guardada criptografada pelo Django e **nunca** vai para o código ou para o GitHub.

## Endereços do site

| Página | Endereço |
|---|---|
| Início | `/` |
| O Projeto | `/projeto/` |
| Atividades | `/atividades/` |
| Equipe | `/equipe/` |
| Alunos | `/alunos/` |
| Voluntários | `/voluntarios/` |
| Notícias | `/noticias/` |
| Contato | `/contato/` |
| Painel da coordenação | `/admin/` |

## Conteúdo pendente da ONG

- [ ] História da instituição
- [ ] Missão
- [ ] Texto oficial sobre a ONG CRIAS e a parceria
- [ ] Texto oficial sobre o CPOP
- [ ] Lista de professores, funções e fotos autorizadas
- [ ] Fotos das atividades
- [ ] Notícias e depoimentos reais autorizados
- [ ] Link público do formulário de aluno
- [ ] Link público do formulário de voluntário
- [ ] Links do Google Classroom, Drive e Meet
- [ ] Redes sociais e contatos oficiais
- [ ] Banco de dados
