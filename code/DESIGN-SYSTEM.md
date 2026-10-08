# Design system — Pré-Vestibular Social ONG Crias

Guia rápido de como usar a identidade visual. A versão visual (com amostras) está em `docs/design-system.html`: abra no navegador. Esse arquivo é só da equipe e pode ser apagado antes da entrega final.

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

## Acessibilidade já embutida

- Contraste mínimo 4,5:1 em textos pequenos (conferido nos pares da tabela acima).
- Foco visível em todos os links e botões; botões com no mínimo 48px de altura.
- Âncoras não ficam escondidas sob o cabeçalho fixo (`scroll-padding-top`).
- Animações são desativadas para quem pede menos movimento no sistema.
