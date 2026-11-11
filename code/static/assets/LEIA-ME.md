# Como trocar as imagens do site

Todas as imagens atuais são **provisórias** (arquivos `.svg` em `assets/placeholders/` com o aviso "IMAGEM ILUSTRATIVA").
Use somente fotos **reais e autorizadas** pela ONG e pelas pessoas fotografadas.

## Onde cada foto aparece

| Lugar no site | Onde trocar | Tamanho sugerido |
|---|---|---|
| Foto principal (topo da Home) | `templates/paginas/inicio.html`, no `<img>` do bloco `<!-- IMAGEM: hero -->` | 1200 × 900 px |
| Foto "Sobre o projeto" (Home) | `templates/paginas/inicio.html`, no `<img>` do bloco `<!-- IMAGEM: sobre -->` | 1200 × 900 px |
| Fotos de "História" e "Educação social" (O Projeto) | `templates/paginas/projeto.html`, nos `<img>` dos blocos `<!-- IMAGEM: ... -->` | 1200 × 900 px |
| Atividades (Aulas, Palestras…) | `templates/paginas/atividades.html`, nos `<img>` de cada seção | 1200 × 750 px |
| Equipe e depoimentos | **Painel /admin/** → Equipe / Depoimentos (campo foto) | 800 × 1000 px (equipe) |
| Notícias | **Painel /admin/** → Notícias (imagem de capa + descrição) | 1200 × 750 px |
| Galeria | **Painel /admin/** → Galeria | 1200 × 900 px |

## Passo a passo

1. Reduza a foto antes de enviar (ideal: até 300 KB, formato `.jpg` ou `.webp`). Sites como squoosh.app fazem isso de graça.
2. Coloque o arquivo na pasta certa (dentro de `code/static/`): `assets/imagens/`, `assets/equipe/`, `assets/atividades/` ou `assets/noticias/`.
3. Troque o caminho (`src` ou `imagem`/`foto`) para o novo arquivo.
4. **Troque também o texto `alt`**: descreva o que a foto mostra (ex.: "Professora explicando matemática para uma turma de alunos").

> Nos templates, use sempre `{% static 'assets/...' %}` no `src`.
> Fotos enviadas pelo painel ficam em `code/media/` (fora do GitHub) e aparecem no site automaticamente.
