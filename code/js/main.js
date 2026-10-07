/* =====================================================================
   main.js — comportamentos básicos compartilhados por todas as páginas
   1) Menu mobile (abrir/fechar)
   2) Links externos configurados em SITE_CONFIG (js/config.js)
   3) Ano atual no rodapé
   Etapa 1: apenas o essencial. Galeria e renderização de dados vêm depois.
   ===================================================================== */

(function () {
    "use strict";

    /* ---------- 1) Menu mobile ---------- */
    function iniciarMenu() {
        var botao = document.querySelector(".nav-toggle");
        var menu = document.getElementById("menu-principal");
        if (!botao || !menu) return;

        function abrir(abrirMenu) {
            botao.setAttribute("aria-expanded", String(abrirMenu));
            menu.classList.toggle("is-open", abrirMenu);
        }

        botao.addEventListener("click", function () {
            abrir(botao.getAttribute("aria-expanded") !== "true");
        });

        // Fecha ao clicar em um link do menu
        menu.addEventListener("click", function (e) {
            if (e.target.closest("a")) abrir(false);
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

        // Telefone: apenas texto
        document.querySelectorAll("[data-text]").forEach(function (el) {
            var valor = (SITE_CONFIG[el.getAttribute("data-text")] || "").trim();
            if (valor) {
                el.textContent = valor;
                el.classList.remove("placeholder");
            }
        });
    }

    /* ---------- 3) Ano no rodapé ---------- */
    function iniciarAno() {
        document.querySelectorAll("[data-ano]").forEach(function (el) {
            el.textContent = new Date().getFullYear();
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        iniciarMenu();
        iniciarLinks();
        iniciarAno();
    });
})();
