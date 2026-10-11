/* =====================================================================
   render.js — desenha na página o conteúdo que vem da pasta data/
   ---------------------------------------------------------------------
   Como funciona: no HTML, um bloco com  data-render="noticias"  (ou
   depoimentos, equipe, atividades, galeria) é preenchido com os itens
   do arquivo data/ correspondente.

   Também faz:
     - data-atividade="aulas"  (atividades.html) preenche texto e foto da atividade a partir de data/atividades.js
     - data-render="noticias-pagina" (noticias.html) lista todas as notícias e, com ?noticia=ID na
       URL, mostra a notícia completa

   Atributos opcionais do bloco:
     data-limite="3"          mostra só os 3 primeiros
     data-grupo="professores" (equipe) mostra só esse grupo

   Se a lista estiver vazia, o aviso que já está no HTML permanece.
   Todo texto é inserido com textContent (seguro: nada de HTML vindo dos dados).
   ===================================================================== */
(function () {
    "use strict";

    var SVG_NS = "http://www.w3.org/2000/svg";

    /* ---------- utilitários ---------- */
    function el(tag, classe, texto) {
        var e = document.createElement(tag);
        if (classe) e.className = classe;
        if (texto !== undefined && texto !== null) e.textContent = texto;
        return e;
    }

    function icone(nome) {
        var svg = document.createElementNS(SVG_NS, "svg");
        svg.setAttribute("class", "icone");
        svg.setAttribute("aria-hidden", "true");
        var uso = document.createElementNS(SVG_NS, "use");
        uso.setAttribute("href", "#i-" + nome);
        svg.appendChild(uso);
        return svg;
    }

    function imagem(src, alt, classe) {
        var img = el("img", classe);
        img.src = src;
        img.alt = alt || "";
        img.loading = "lazy";
        img.decoding = "async";
        return img;
    }

    function dataBR(iso) {
        if (!iso) return "[DATA]";
        var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
        return m ? m[3] + "/" + m[2] + "/" + m[1] : iso;
    }

    // Notícias mais novas primeiro (itens sem data ficam por último)
    function ordenarNoticias(lista) {
        return lista.slice().sort(function (a, b) {
            return (b.data || "").localeCompare(a.data || "");
        });
    }

    // Notícia com id e texto abre a leitura completa em noticias.html?noticia=ID
    function urlNoticia(item) {
        if (item.id && item.texto) return "noticias.html?noticia=" + encodeURIComponent(item.id);
        return item.link || "noticias.html";
    }

    function marcarPlaceholder(card, item) {
        if (item.placeholder) card.classList.add("is-placeholder");
    }

    /* ---------- um desenhista por tipo de conteúdo ---------- */
    var desenhistas = {

        depoimentos: function (item) {
            var card = el("figure", "card card--depoimento");
            var citacao = el("blockquote");
            citacao.appendChild(el("p", null, item.texto));
            card.appendChild(citacao);

            var legenda = el("figcaption");
            if (item.foto) {
                legenda.appendChild(imagem(item.foto, item.alt, "avatar"));
            } else {
                var caixa = el("span", "icon-box icon-box--redondo");
                caixa.appendChild(icone("usuario"));
                legenda.appendChild(caixa);
            }
            var quem = el("span");
            quem.appendChild(el("strong", null, item.nome));
            quem.appendChild(document.createTextNode(item.turma || ""));
            legenda.appendChild(quem);
            card.appendChild(legenda);
            marcarPlaceholder(card, item);
            return card;
        },

        equipe: function (item) {
            var card = el("article", "card card--pessoa");
            if (item.foto) card.appendChild(imagem(item.foto, item.alt, "foto"));
            var corpo = el("div", "card__corpo");
            corpo.appendChild(el("h3", null, item.nome));
            corpo.appendChild(el("p", "card__funcao", item.funcao));
            if (item.descricao) corpo.appendChild(el("p", "card__descricao", item.descricao));
            card.appendChild(corpo);
            marcarPlaceholder(card, item);
            return card;
        },

        noticias: function (item) {
            var card = el("article", "card card--noticia card--link");
            if (item.imagem) card.appendChild(imagem(item.imagem, item.alt, "foto"));
            var corpo = el("div", "card__corpo");
            var meta = el("div", "card__meta");
            meta.appendChild(el("span", null, item.categoria || ""));
            meta.appendChild(el("span", null, dataBR(item.data)));
            corpo.appendChild(meta);

            var titulo = el("h3");
            var link = el("a", "link-card", item.titulo);
            link.href = urlNoticia(item);
            titulo.appendChild(link);
            corpo.appendChild(titulo);

            if (item.resumo) corpo.appendChild(el("p", "card__descricao", item.resumo));
            var leia = el("span", "link-seta", "Ler notícia");
            corpo.appendChild(leia);
            card.appendChild(corpo);
            marcarPlaceholder(card, item);
            return card;
        },

        atividades: function (item) {
            var card = el("article", "card card--atividade card--link");
            if (item.imagem) card.appendChild(imagem(item.imagem, item.alt, "foto"));
            var corpo = el("div", "card__corpo");
            var titulo = el("h3");
            var link = el("a", "link-card", item.titulo);
            link.href = "atividades.html#" + item.tipo;
            titulo.appendChild(link);
            corpo.appendChild(titulo);
            if (item.descricao) corpo.appendChild(el("p", "card__descricao", item.descricao));
            corpo.appendChild(el("span", "link-seta", "Saiba mais"));
            card.appendChild(corpo);
            marcarPlaceholder(card, item);
            return card;
        },

        galeria: function (item) {
            var fig = el("figure", "galeria__item");
            fig.appendChild(imagem(item.imagem, item.alt, "foto"));
            return fig;
        }
    };

    /* ---------- lista de dados de cada tipo ---------- */
    function dados(tipo) {
        try {
            switch (tipo) {
                case "depoimentos": return typeof depoimentos !== "undefined" ? depoimentos : [];
                case "equipe":      return typeof equipe !== "undefined" ? equipe : [];
                case "noticias":    return ordenarNoticias(typeof noticias !== "undefined" ? noticias : []);
                case "atividades":  return typeof atividades !== "undefined" ? atividades : [];
                case "galeria":     return typeof galeria !== "undefined" ? galeria : [];
            }
        } catch (e) { /* sem dados: mantém o aviso do HTML */ }
        return [];
    }

    /* ---------- atividades.html: preenche as seções fixas com os dados ---------- */
    function preencherAtividades() {
        document.querySelectorAll("[data-atividade]").forEach(function (secao) {
            var tipo = secao.getAttribute("data-atividade");
            var item = dados("atividades").filter(function (i) { return i.tipo === tipo; })[0];
            if (!item || item.placeholder) return; // sem dados reais: mantém o texto provisório do HTML

            var titulo = secao.querySelector("[data-campo=titulo]");
            if (titulo && item.titulo) titulo.textContent = item.titulo;

            var foto = secao.querySelector("[data-campo=imagem]");
            if (foto && item.imagem) {
                foto.src = item.imagem;
                if (item.alt) foto.alt = item.alt;
            }

            var descricao = secao.querySelector("[data-campo=descricao]");
            if (descricao && item.descricao) {
                var bloco = el("div", "texto-longo");
                item.descricao.split(/\n\s*\n/).forEach(function (par) {
                    if (par.trim()) bloco.appendChild(el("p", null, par.trim()));
                });
                descricao.replaceWith(bloco);
            }
        });
    }

    /* ---------- noticias.html: lista e leitura completa ---------- */
    function mostrarNoticia(raiz, item) {
        raiz.textContent = "";
        var voltar = el("a", "link-voltar", "Todas as notícias");
        voltar.href = "noticias.html";
        raiz.appendChild(voltar);

        var meta = el("p", "noticia__meta");
        meta.appendChild(el("span", null, item.categoria || ""));
        meta.appendChild(el("span", null, dataBR(item.data)));
        raiz.appendChild(meta);

        raiz.appendChild(el("h2", "noticia__titulo", item.titulo));

        if (item.imagem) {
            var fig = el("figure", "noticia__imagem");
            fig.appendChild(imagem(item.imagem, item.alt, "foto"));
            raiz.appendChild(fig);
        }

        var texto = el("div", "noticia__texto");
        (item.texto || item.resumo || "").split(/\n\s*\n/).forEach(function (par) {
            if (par.trim()) texto.appendChild(el("p", null, par.trim()));
        });
        raiz.appendChild(texto);
    }

    function paginaNoticias(bloco) {
        var lista = dados("noticias");
        var id = new URLSearchParams(window.location.search).get("noticia");
        var item = id ? (lista.filter(function (i) { return i.id === id; })[0] || null) : null;
        var detalhe = document.getElementById("noticia-detalhe");

        if (item && detalhe) {
            mostrarNoticia(detalhe, item);
            detalhe.hidden = false;
            bloco.hidden = true;
            var cab = document.getElementById("noticias-cabecalho");
            if (cab) cab.hidden = true;
            document.title = item.titulo + " | Pré-Vestibular Social ONG Crias";
            return;
        }

        if (!lista.length) return; // mantém o aviso "nenhuma notícia" do HTML

        bloco.textContent = "";
        if (id) bloco.appendChild(el("p", "aviso-noticia", "Não encontramos essa notícia. Veja as mais recentes abaixo."));
        var grade = el("div", "grid");
        lista.forEach(function (i) { grade.appendChild(desenhistas.noticias(i)); });
        bloco.appendChild(grade);
    }

    /* ---------- varre a página ---------- */
    function renderizar() {
        preencherAtividades();

        document.querySelectorAll("[data-render]").forEach(function (bloco) {
            var tipo = bloco.getAttribute("data-render");
            if (tipo === "noticias-pagina") { paginaNoticias(bloco); return; }
            var desenhar = desenhistas[tipo];
            if (!desenhar) return;

            var lista = dados(tipo).slice();

            var grupo = bloco.getAttribute("data-grupo");
            if (grupo) lista = lista.filter(function (i) { return i.grupo === grupo; });

            var limite = parseInt(bloco.getAttribute("data-limite"), 10);
            if (limite > 0) lista = lista.slice(0, limite);

            if (!lista.length) return; // mantém o aviso que já está no HTML

            var grade = el("div", "grid " + (bloco.getAttribute("data-grade") || ""));
            lista.forEach(function (item) { grade.appendChild(desenhar(item)); });

            bloco.textContent = "";
            if (bloco.classList.contains("grid")) {
                // o próprio bloco já é a grade
                lista.forEach(function (item) { bloco.appendChild(desenhar(item)); });
            } else {
                bloco.appendChild(grade);
            }
        });
    }

    // Scripts "defer": a página já foi lida quando este código roda — desenha na hora.
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", renderizar);
    } else {
        renderizar();
    }
})();
