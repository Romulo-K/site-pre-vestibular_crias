# Como trocar as imagens do site

Todas as imagens atuais são **provisórias** (arquivos `.svg` em `assets/placeholders/` com o aviso "IMAGEM ILUSTRATIVA").
Use somente fotos **reais e autorizadas** pela ONG e pelas pessoas fotografadas.

## Onde cada foto aparece

| Lugar no site | Onde trocar | Tamanho sugerido |
|---|---|---|
| Foto principal (topo da Home) | `index.html`, no `<img>` do bloco `<!-- IMAGEM: hero -->` | 1200 × 900 px |
| Foto "Sobre o projeto" (Home) | `index.html`, no `<img>` do bloco `<!-- IMAGEM: sobre -->` | 1200 × 900 px |
| Atividades (Aulas, Palestras…) | `data/atividades.js` → campo `imagem` e `alt` | 1200 × 750 px |
| Equipe e depoimentos | `data/equipe.js` e `data/depoimentos.js` → campo `foto` e `alt` | 800 × 1000 px (equipe) |
| Notícias | `data/noticias.js` → campo `imagem` e `alt` | 1200 × 750 px |
| Galeria | `data/atividades.js` → lista `galeria` | 1200 × 900 px |

## Passo a passo

1. Reduza a foto antes de enviar (ideal: até 300 KB, formato `.jpg` ou `.webp`). Sites como squoosh.app fazem isso de graça.
2. Coloque o arquivo na pasta certa: `assets/imagens/`, `assets/equipe/`, `assets/atividades/` ou `assets/noticias/`.
3. Troque o caminho (`src` ou `imagem`/`foto`) para o novo arquivo.
4. **Troque também o texto `alt`**: descreva o que a foto mostra (ex.: "Professora explicando matemática para uma turma de alunos").
