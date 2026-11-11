# Banco de dados

O banco é **SQLite**, ou seja, é um arquivo só (`code/db.sqlite3`). Esse arquivo não vai pro GitHub.

Eu não criei as tabelas escrevendo SQL na mão: elas são escritas em Python no
`code/conteudo/models.py` e o Django transforma isso em SQL (são as *migrations*).

```
models.py (python) → makemigrations → migrations/0001_initial.py → migrate → db.sqlite3
```

## Arquivos

- `bd.py` → script em Python que gera o `schema.sql` e conta quantos registros tem em cada tabela (usando SQL direto)
- `schema.sql` → o SQL que o Django usa pra criar as tabelas (gerado pelo `bd.py`)

Como usar (na pasta do projeto, com o `.venv` ativado):

```bash
python bd/bd.py          # gera o schema.sql
python bd/bd.py contar   # mostra quantos registros tem no banco
```

## As tabelas

**noticias**
- `titulo`, `resumo`, `texto`, `autor`
- `slug` → o endereço da notícia (`/noticias/<slug>/`), feito a partir do título
- `capa` e `capa_descricao` → foto de capa e a descrição dela (pra acessibilidade)
- `status` → `rascunho` ou `publicada` (rascunho não aparece no site)
- `publicada_em` → preenchida sozinha na primeira vez que publica

**integrantes** (equipe)
- `nome`, `funcao`, `disciplina`, `biografia`
- `grupo` → `coordenacao`, `professores` ou `apoio`
- `foto` e `foto_autorizada` → só aceita foto se marcar a autorização
- `ordem` → menor aparece primeiro
- `ativo` → desmarcado some do site, mas continua no banco

**galeria**
- `titulo`, `imagem`, `descricao` (o que a foto mostra), `legenda`
- `categoria` → aulas, palestras, simulados, convivência, passeios ou outros
- `data_atividade`, `uso_autorizado`

**depoimentos**
- `nome`, `turma`, `texto`, `foto`
- `autorizado` e `ativo` → só aparece no site se os dois estiverem marcados

**configuracao_site** (links e contatos)
- tabela com uma linha só, editada no painel em "Links e contatos do site"
- links: `formulario_aluno`, `formulario_voluntario`, `classroom`, `drive`, `meet`
- contatos: `email`, `telefone`, `whatsapp` (só números, o site monta o link), `endereco`, `horario`, `mapa`
- redes: `instagram`, `facebook`, `youtube`

Toda tabela tem um `id` e as datas de criação, que o Django preenche sozinho.
O login e as senhas do painel ficam nas tabelas do próprio Django (`auth_user`), com a senha criptografada.

## Observações

- As fotos não ficam dentro do banco, só o caminho delas. O arquivo fica em `code/media/`.
- Fotos só em JPG, PNG ou WebP, até 3 MB.
- Quando um registro é apagado (ou a foto é trocada), a foto antiga é apagada também (`code/conteudo/signals.py`).
- Pra ver o banco por dentro dá pra usar o **DB Browser for SQLite** (tem na Pop!_Shop).
