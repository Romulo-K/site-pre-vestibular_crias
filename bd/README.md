# Banco de dados — Pré-Vestibular Social ONG Crias

O banco é **SQLite** (um único arquivo: `code/db.sqlite3`, que **não** vai para o GitHub).
Ele é criado e alterado pelo **Django** a partir dos modelos escritos em Python em
`code/conteudo/models.py`. O Django traduz esses modelos para **SQL** (as *migrations*).

```
models.py (Python)  ──makemigrations──►  migrations/0001_initial.py  ──migrate──►  db.sqlite3 (SQL)
                                                     │
                                         python bd/bd.py  ──►  bd/schema.sql (documentação do SQL)
```

## Arquivos desta pasta

| Arquivo | Para que serve |
|---|---|
| `bd.py` | Script Python que gera o `schema.sql`, lista as tabelas (`--resumo`) e conta os registros (`--contar`). |
| `schema.sql` | O SQL exato das tabelas do site, gerado a partir das migrations. **Não edite à mão.** |
| `README.md` | Este guia (dicionário de dados). |

## Comandos (na raiz do repositório, com o `.venv` ativo)

```bash
python bd/bd.py            # gera/atualiza bd/schema.sql
python bd/bd.py --resumo   # mostra tabelas e colunas
python bd/bd.py --contar   # quantos registros existem no seu banco local
```

Quando mudar `models.py`:
```bash
cd code
python manage.py makemigrations   # o Django escreve a mudança
python manage.py migrate          # aplica no banco
cd ..
python bd/bd.py                   # atualiza a documentação SQL
```

## Tabelas do site

### `noticias`
| Coluna | Tipo | Observação |
|---|---|---|
| `id` | inteiro | chave primária automática |
| `titulo` | texto (200) | obrigatório |
| `slug` | texto (220), único | parte do endereço (`/noticias/<slug>/`), gerado do título |
| `resumo` | texto (300) | obrigatório, aparece nos cards |
| `texto` | texto longo | obrigatório; parágrafos separados por linha em branco |
| `capa` | caminho do arquivo | opcional; a foto fica em `code/media/noticias/` |
| `capa_descricao` | texto (200) | descrição da imagem (acessibilidade); obrigatória se houver capa |
| `autor` | texto (120) | opcional |
| `status` | `rascunho` ou `publicada` | rascunhos **nunca** aparecem no site |
| `publicada_em` | data e hora | preenchida na **primeira** publicação; edições não mudam |
| `criada_em`, `atualizada_em` | data e hora | automáticas |

Índice: `(status, publicada_em)` para listar rápido as notícias publicadas mais recentes.

### `integrantes` (equipe)
| Coluna | Tipo | Observação |
|---|---|---|
| `id` | inteiro | chave primária |
| `nome`, `funcao` | texto (120) | obrigatórios |
| `disciplina` | texto (80) | opcional |
| `biografia` | texto longo | descrição curta, opcional |
| `grupo` | `coordenacao`, `professores` ou `apoio` | seção da página Equipe |
| `foto` | caminho do arquivo | opcional; `code/media/equipe/` |
| `foto_autorizada` | sim/não | obrigatório marcar se houver foto |
| `ordem` | inteiro ≥ 0 | menor aparece primeiro |
| `ativo` | sim/não | desmarcado = some do site sem apagar os dados |
| `criado_em`, `atualizado_em` | data e hora | automáticas |

Índice: `(ativo, grupo, ordem)`.

### `galeria`
| Coluna | Tipo | Observação |
|---|---|---|
| `id` | inteiro | chave primária |
| `titulo` | texto (150) | obrigatório |
| `imagem` | caminho do arquivo | obrigatório; `code/media/galeria/` |
| `descricao` | texto (200) | descrição da imagem (acessibilidade), obrigatória |
| `legenda` | texto (200) | opcional |
| `categoria` | `aulas`, `palestras`, `simulados`, `convivencia`, `passeios`, `outros` | |
| `data_atividade` | data | opcional |
| `uso_autorizado` | sim/não | obrigatório marcar |
| `criada_em` | data e hora | automática |

### `depoimentos`
| Coluna | Tipo | Observação |
|---|---|---|
| `id` | inteiro | chave primária |
| `nome` | texto (120) | obrigatório |
| `turma` | texto (120) | ex.: "Ex-aluna, turma de 2024" |
| `texto` | texto (até 800) | obrigatório |
| `foto` | caminho do arquivo | opcional; `code/media/depoimentos/` |
| `autorizado` | sim/não | obrigatório marcar |
| `ativo`, `ordem` | | exibição no site |
| `criado_em` | data e hora | automática |

## Regras importantes
- **Fotos não ficam dentro do banco**: o banco guarda só o caminho; o arquivo fica em `code/media/`.
- **Imagens**: só JPG, PNG ou WebP, até **3 MB**. O nome do arquivo é limpo e ganha um código aleatório
  (nunca sobrescreve outra foto).
- **Ao excluir** um registro, a foto dele é apagada. **Ao trocar** uma foto, a antiga só é apagada depois
  que a nova foi salva.
- **Login e senha** ficam nas tabelas do próprio Django (`auth_user`), com a senha guardada de forma
  criptografada (hash). O projeto usa **uma conta da coordenação**.

## Ver o banco por dentro (opcional)
- **DB Browser for SQLite** (procure na Pop!_Shop): abra o arquivo `code/db.sqlite3`.
- Ou no terminal: `sudo apt install sqlite3` e depois, dentro de `code/`, `python manage.py dbshell`.
