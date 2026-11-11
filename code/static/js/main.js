// main.js - coisas que todas as páginas usam
// parte 1: menu do celular (abrir e fechar)
// parte 2: links externos que vêm do config.js (formulários, classroom...)
// parte 3: ano atual no rodapé
// parte 4: se uma foto não carregar, esconde ela em vez de mostrar a imagem quebrada
// (o item do menu da página atual quem marca é o django, no base.html)

(function () {
    "use strict";

    /* ---------- 1) Menu mobile ---------- */
    function iniciarMenu() {
        var botao = document.querySelector(".nav-toggle");
        var menu = document.getElementById("menu-principal");
        if (!botao || !menu) return;

        function abrir(abrirMenu) {
            botao.setAttribute("aria-expanded", String(abrirMenu));
            botao.textContent = abrirMenu ? "Fechar" : "Menu";
            menu.classList.toggle("is-open", abrirMenu);
        }

        botao.addEventListener("click", function () {
            abrir(botao.getAttribute("aria-expanded") !== "true");
        });

        // Fecha ao clicar em um link do menu
        menu.addEventListener("click", function (e) {
            if (e.target.closest("a")) abrir(false);
        });

        // Fecha ao clicar fora do menu
        document.addEventListener("click", function (e) {
            if (botao.getAttribute("aria-expanded") === "true" && !e.target.closest(".site-header")) abrir(false);
        });

        // Se a janela ficar larga (menu horizontal), garante o menu fechado
        window.addEventListener("resize", function () {
            if (window.innerWidth >= 900 && botao.getAttribute("aria-expanded") === "true") abrir(false);
        });

        // Fecha com a tecla Esc e devolve o foco ao botão
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && botao.getAttribute("aria-expanded") === "true") {
                abrir(false);
                botao.focus();
            }
        });
    }

    /* ---------- 2) Links vindos do SITE_CONFIG ----------
       Uso no HTML:  <a data-link="formularioAluno">...</a>
       - data-link="email"    -> vira mailto:
       - data-optional        -> se não houver link, o elemento é escondido
       - data-fill-text       -> escreve o valor configurado dentro do elemento
       - sem valor configurado -> link desativado (sem href falso)       */
    function iniciarLinks() {
        if (typeof SITE_CONFIG === "undefined") {
            console.warn("SITE_CONFIG não encontrado. Verifique js/config.js.");
            return;
        }

        var elementos = document.querySelectorAll("[data-link]");
        elementos.forEach(function (el) {
            var chave = el.getAttribute("data-link");
            var valor = (SITE_CONFIG[chave] || "").trim();

            if (!valor) {
                if (el.hasAttribute("data-optional")) {
                    el.hidden = true;
                    return;
                }
                el.removeAttribute("href");
                el.removeAttribute("target");
                el.removeAttribute("rel");
                el.setAttribute("aria-disabled", "true");
                el.classList.add("is-pending");
                el.title = "Link ainda não configurado (js/config.js)";
                console.warn("Link pendente em SITE_CONFIG: " + chave);
                return;
            }

            el.href = chave === "email" ? "mailto:" + valor : valor;

            if (chave !== "email") {
                el.target = "_blank";
                el.rel = "noopener noreferrer";
            }

            if (el.hasAttribute("data-fill-text")) {
                el.textContent = valor;
            }
        });

        // Textos simples (telefone, endereço, horário): escreve o valor e tira o aviso de pendência
        document.querySelectorAll("[data-text]").forEach(function (el) {
            var valor = (SITE_CONFIG[el.getAttribute("data-text")] || "").trim();
            if (valor) {
                el.textContent = valor;
                el.classList.remove("placeholder");
            }
        });

        // Avisos que somem quando QUALQUER uma das chaves listadas estiver preenchida
        // Ex.: <p class="placeholder" data-placeholder-for="instagram facebook youtube">
        document.querySelectorAll("[data-placeholder-for]").forEach(function (el) {
            var chaves = el.getAttribute("data-placeholder-for").split(/\s+/);
            var algumPreenchido = chaves.some(function (k) {
                return (SITE_CONFIG[k] || "").trim() !== "";
            });
            if (algumPreenchido) el.hidden = true;
        });
    }

    /* ---------- 3) Ano no rodapé ---------- */
    function iniciarAno() {
        document.querySelectorAll("[data-ano]").forEach(function (el) {
            el.textContent = new Date().getFullYear();
        });
    }

    /* ---------- 4) Foto que não carregou ----------
       Se uma foto do banco sumir do servidor, o card continua de pé sem ela. */
    function esconderImagemQuebrada(img) {
        var itemGaleria = img.closest(".galeria__item");
        if (itemGaleria) { itemGaleria.hidden = true; return; }
        if (img.closest(".card, .noticia__imagem")) img.hidden = true;
    }

    function iniciarImagensQuebradas() {
        // Fotos que falharem daqui para frente...
        document.addEventListener("error", function (e) {
            if (e.target && e.target.tagName === "IMG") esconderImagemQuebrada(e.target);
        }, true);
        // ...e as que já falharam antes deste script rodar.
        document.querySelectorAll("img").forEach(function (img) {
            if (img.complete && img.naturalWidth === 0 && img.getAttribute("src")) esconderImagemQuebrada(img);
        });
    }

    function iniciar() {
        iniciarMenu();
        iniciarImagensQuebradas();
        iniciarLinks();
        iniciarAno();
    }

    // Os scripts usam "defer": quando rodam, a página já foi lida. Executar na hora evita
    // um "piscar" de conteúdo provisório e deixa os links com #âncora funcionarem.
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", iniciar);
    } else {
        iniciar();
    }
})();
