# Pré-Vestibular Social ONG Crias — Site institucional

Projeto de extensão universitária. Site estático (HTML5, CSS3 e JavaScript), sem backend, sem banco de dados e sem login.

Repositório: https://github.com/Romulo-K/site-pre-vestibular_crias

## Como visualizar

Abra `index.html` no navegador. Não há instalação nem build.

## Estrutura

```
site-pre-vestibular_crias/
├── index.html          Início
├── projeto.html        O Projeto
├── atividades.html     Atividades
├── equipe.html         Equipe
├── alunos.html         Alunos + Área do aluno
├── voluntarios.html    Voluntários
├── noticias.html       Notícias
├── contato.html        Contato
├── css/style.css       Estilos
├── js/
│   ├── config.js       Links centralizados (formulários, Classroom, Drive, Meet, contatos)
│   └── main.js         Menu mobile e ligação dos links
├── data/               Conteúdo que se repete (notícias, depoimentos, equipe, atividades)
└── assets/             logo, imagens, equipe, atividades, noticias, icones
```

## Como atualizar links

Edite apenas `js/config.js`. Enquanto um link estiver vazio, o botão correspondente aparece desativado (não existe link falso).

## Como atualizar conteúdo

Edite os arquivos de `data/` seguindo o modelo comentado em cada um, salve e faça `git push`.

## Regras do projeto

- Sem frameworks, backend, banco de dados, login ou painel administrativo no MVP.
- Não inventar informações institucionais: textos como `[TEXTO OFICIAL DA ONG ...]` devem ser substituídos pelos textos aprovados pela ONG.
- Imagens geradas por IA são apenas temporárias; usar fotos reais somente com autorização.
- Todo `<img>` precisa de `alt` descritivo.
- Usar apenas caminhos relativos, para o site funcionar em qualquer hospedagem estática (ex.: GitHub Pages).

## Conteúdo pendente da ONG

- [ ] História da instituição
- [ ] Missão
- [ ] Texto oficial sobre a ONG CRIAS e a parceria
- [ ] Texto oficial sobre o CPOP
- [ ] Textos sobre BNCC e ENEM
- [ ] Lista de professores, funções e fotos autorizadas
- [ ] Fotos das atividades
- [ ] Notícias e depoimentos reais autorizados
- [ ] Link público do formulário de aluno
- [ ] Link público do formulário de voluntário
- [ ] Links do Google Classroom, Drive e Meet
- [ ] Redes sociais e contatos oficiais
- [ ] Endereço, se a ONG quiser divulgar

## Etapas de desenvolvimento

1. Estrutura (concluída)
2. Design system
3. Home
4. Páginas internas
5. JavaScript e interações
6. Conteúdo real
7. Responsividade e acessibilidade
8. Auditoria final
