# Visual do site (design system)

Anotações de como o visual do site está organizado, pra eu não me perder.

## Cores e fontes

Tudo fica no começo do `static/css/style.css` (parte 2, as variáveis). Trocando uma variável lá, muda no site inteiro.

- Verde da logo `#069762` → só em detalhes e textos grandes (em texto pequeno não tem contraste suficiente)
- Verde dos botões `#057A4F`, verde dos títulos `#046A45`, verde escuro do rodapé `#034A31`
- Amarelo `#FCC601` → destaques e botão principal
- Lilás bem claro `#F0EAFA` → fundo de algumas seções
- Texto `#1B2A22`, texto mais fraco `#4B5A52`
- Fontes: **Outfit** nos títulos e **Inter** no resto (ficam em `static/assets/fonts/`)

## Peças que se repetem

- Botões: `.btn` + variações (`--destaque` amarelo, `--contorno`, `--claro`, `--sm`, `--lg`)
- Cards: `.card` + tipos (`--noticia`, `--pessoa`, `--depoimento`, `--atividade`, `--plataforma`)
- Seções: `.section` (branca), `.section--suave` (lilás), `.section--institucional` (verde escuro)
- Grades: `.grid`, `.grid--2`, `.grid--5`, `.grid--pessoas`
- Topo das páginas internas: `.page-header` com o caminho (`.breadcrumb`)
- Texto provisório: `.placeholder` (amarelinho com borda, pra lembrar que falta o texto oficial)
- Quando não tem conteúdo ainda: `.estado-vazio`
- Paginação das notícias e da galeria: `.paginacao`
- Faixa de versão de teste: `.aviso-teste`

## Templates

- `templates/base.html` → cabeçalho, menu, rodapé e scripts. Todas as páginas usam ele com `{% extends "base.html" %}`
- `templates/includes/` → pedaços reaproveitados: ícones, cards, paginação e a chamada "Quer fazer parte?"
- `templates/paginas/` → uma página por arquivo
- Links internos: `{% url 'paginas:equipe' %}` e imagens/css/js: `{% static 'assets/...' %}`

## JavaScript

- `static/js/config.js` → links dos formulários, classroom, drive, meet e contatos
- `static/js/main.js` → menu do celular, links do config, ano do rodapé, foto quebrada
- `static/js/galeria.js` → foto grande da galeria

## Acessibilidade (o que eu tentei garantir)

- Toda imagem tem `alt` (descrição)
- Dá pra navegar só com o teclado e o foco aparece
- Botões que levam pra fora do site avisam que abrem em nova aba
- Contraste dos textos dentro do recomendado
