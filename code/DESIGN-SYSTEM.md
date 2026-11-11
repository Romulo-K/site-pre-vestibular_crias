# Design system — Pré-Vestibular Social ONG Crias

Guia rápido de como usar a identidade visual. Os arquivos citados ficam em `code/static/` (CSS, JS, dados) e `code/templates/` (HTML).

Toda a identidade está em **`css/style.css`, seção 2 (TOKENS)**. Para mudar uma cor, fonte ou espaçamento, altere a variável: todo o site acompanha.

## Cores

As duas cores de identidade vêm da logo: verde `#069762` e amarelo `#FCC601`.

| Papel | Variável | Cor | Uso |
|---|---|---|---|
| Verde da logo | `--verde-500` | `#069762` | Decoração, formas e textos grandes. **Não use em texto pequeno** (contraste 3,7:1) |
| Primária | `--verde-600` | `#057A4F` | Botões (texto branco 5,4:1) |
| Títulos e links | `--verde-700` | `#046A45` | Títulos e links sobre fundo claro (6,7:1) |
| Institucional | `--verde-800` | `#04523A` | Seções e cards verde escuro (9,2:1 com branco) |
| Rodapé | `--verde-900` | `#034A31` | Rodapé (10,4:1 com branco) |
| Verde claro | `--verde-50` / `--verde-100` | `#E8F7F0` / `#C9ECDA` | Ícones, selos, texto sobre verde escuro |
| Amarelo da logo | `--amarelo-500` | `#FCC601` | Botão de destaque, etiquetas, card de destaque. Sempre com texto escuro (9,4:1) |
| Amarelo suave | `--amarelo-50` | `#FFF7D6` | Avisos de conteúdo pendente |
| Lilás | `--lilas-100` | `#F0EAFA` | Fundo de seções alternadas |
| Lilás de apoio | `--lilas-700` | `#5A4A80` | Texto sobre lilás (6,8:1) |
| Texto | `--texto` / `--texto-suave` | `#1B2A22` / `#4B5A52` | Texto principal (15:1) e secundário (7,3:1) |

**Regra de uso:** fundo branco e lilás se alternam; verde escuro marca as áreas institucionais (depoimentos, benefícios, rodapé); amarelo é para destaque pontual (no máximo um card ou botão amarelo por seção).

## Tipografia

- **Títulos:** Outfit, pesos 700 e 800.
- **Textos:** Inter, peso 400 (500/600 para ênfase).
- Fontes hospedadas em `assets/fonts/` (não dependem do Google Fonts; licenças OFL incluídas).

| Elemento | Variável | Tamanho (celular → desktop) |
|---|---|---|
| `h1` | `--titulo-1` | 36 → 64px |
| `h2` | `--titulo-2` | 28 → 44px |
| `h3` | `--titulo-3` | 20 → 26px |
| `h4` (títulos de cards) | `--titulo-4` | 18 → 21px |
| `.lead` (introdução) | `--texto-lg` | 17 → 20px |
| Texto | `--texto-md` | 16px |
| Apoio / rodapé | `--texto-sm` | 15px |
| Rótulos | `--texto-xs` | 13px |

## Espaçamento, bordas e sombras

- Espaçamento em escala de 4px: `--espaco-1` (4px) até `--espaco-9` (96px). Entre seções: `--espaco-secao` (56 a 104px).
- Bordas: `--raio-sm` 10px, `--raio-md` 16px, `--raio-lg` 24px (cards), `--raio-xl` 36px (fotos), `--raio-pill` (botões e selos).
- Sombras: `--sombra-sm` (cards), `--sombra-md` (hover e destaque), `--sombra-lg` (fotos de destaque).

## Componentes prontos (classes)

| Componente | Classes |
|---|---|
| Botões | `.btn` (primário), `.btn--destaque` (amarelo), `.btn--contorno`, `.btn--claro` e `.btn--contorno-claro` (fundo escuro), `.btn--sm`, `.btn--lg` |
| Aviso de link externo | `<span class="btn__externo">` dentro do botão |
| Link com seta | `.link-seta` |
| Cards | `.card`, `.card--link` (hover), `.card--destaque` (amarelo), `.card--verde`, `.card--depoimento`, `.card--pessoa`, `.card--noticia` |
| Ícone de card | `.icon-box` |
| Selos | `.selo`, `.selo--verde`, `.selo--lilas` |
| Rótulo de seção | `.eyebrow` (o "● SOBRE O PROJETO" acima do título) |
| Seções | `.section`, `.section--suave` (lilás), `.section--institucional` (verde escuro), `.section-head` |
| Grades | `.grid`, `.grid--2`, `.grid--4`, `.split` (texto + imagem) |
| Foto de destaque | `.foto-destaque` + `.foto-destaque__etiqueta` |
| Decoração | `.decor-circulo` |
| Pendências | `.placeholder`, `.img-placeholder` (avisos de conteúdo que a ONG ainda vai fornecer) |
| Cards de acesso (Home) | `.acesso-card` (card inteiro clicável, com `data-link` para o Google Forms) |
| Painel verde de benefícios | `.card.card--verde.beneficios` |
| Card clicável por um só link | `.card--link` + `<a class="link-card">` no título (o link cobre o card todo) |
| Cards com foto | `.card--noticia`, `.card--atividade`, `.card--pessoa` (desenhados por `js/render.js`) |
| Chamada final | `.cta-final` |
| Ícones | `<svg class="icone"><use href="#i-nome"/></svg>` (lista no sprite no topo de cada página) |
| Grades extras | `.grid--5` (atividades), `.grid--pessoas` (equipe; 2 colunas no celular) |

## Acessibilidade já embutida

- Contraste mínimo 4,5:1 em textos pequenos (conferido nos pares da tabela acima).
- Foco visível em todos os links e botões; botões com no mínimo 48px de altura.
- Âncoras não ficam escondidas sob o cabeçalho fixo (`scroll-padding-top`).
- Animações são desativadas para quem pede menos movimento no sistema.

## Componentes das páginas internas (Etapa 4)
- `.page-header__acoes` — botões logo abaixo do título da página (Alunos, Voluntários).
- `.indice-pagina` — chips de navegação por âncoras no topo da página.
- `.missao` — bloco verde de destaque (O Projeto → Missão).
- `.passos` / `.passo` — passos numerados (como se inscrever / como participar).
- `.atividade` + `.atividade__card` — foto + card de texto, alternando os lados.
- `.card--plataforma` — atalho para Google Classroom/Drive/Meet.
- `.contato-card` e `.lista-links` — canais de contato.
- `.noticia`, `.link-voltar` — leitura completa de notícia (`/noticias/?noticia=ID`).
- `.mt-6` — utilitário de espaçamento.

Textos e links vêm de `js/config.js` (links, contatos) e `data/*.js` (equipe, atividades, notícias).

## JavaScript (Etapa 5)
- `js/config.js` — todos os links e contatos (formulários, Classroom, Drive, Meet, WhatsApp, e-mail, redes). Único arquivo a editar para trocar links.
- `js/main.js` — menu mobile (abre/fecha, Esc, clique fora), links do config, ano do rodapé.
- `js/render.js` — desenha notícias, depoimentos, equipe, atividades e galeria a partir de `data/*.js`.
- `js/galeria.js` — foto ampliada da galeria (`<dialog>`): fechar com botão, Esc ou clique fora; setas para navegar.

## Templates Django (Etapa 6)
- `templates/base.html` — estrutura comum: `<head>`, cabeçalho, menu (o item ativo é marcado pelo Django), rodapé e scripts.
- `templates/includes/icones.html` — os ícones SVG. `templates/includes/cta_participe.html` — chamada "Quer fazer parte?".
- `templates/paginas/*.html` — uma página por arquivo. Cada uma começa com `{% extends "base.html" %}` e preenche os blocos
  `titulo`, `descricao`, `conteudo`, `dados` (arquivos de data/) e `scripts` (render.js, galeria.js).
- Links internos: `{% url 'paginas:equipe' %}`. Imagens/CSS/JS: `{% static 'assets/...' %}`.
