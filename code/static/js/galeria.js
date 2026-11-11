/* =====================================================================
   galeria.js — foto ampliada da galeria (página Atividades)
   ---------------------------------------------------------------------
   Clique (ou Enter) em uma foto da galeria: ela abre ampliada, com fundo escuro.
   Fechar: botão "Fechar", tecla Esc ou clique fora da foto.
   Com mais de uma foto: botões Anterior/Próxima e setas ← → do teclado.
   Usa o elemento <dialog>, que já cuida do foco e do Esc. Sem bibliotecas.
   ===================================================================== */
(function () {
    "use strict";

    var dialogo = null, imgGrande, legenda, contador, btnAnterior, btnProxima, lista = [], indice = 0, origem = null;

    function criar() {
        dialogo = document.createElement("dialog");
        dialogo.className = "lightbox";
        dialogo.setAttribute("aria-label", "Foto ampliada");
        dialogo.innerHTML =
            '<div class="lightbox__conteudo">' +
            '<button type="button" class="lightbox__fechar">Fechar</button>' +
            '<figure class="lightbox__figura"><img class="lightbox__img" alt=""><figcaption class="lightbox__legenda"></figcaption></figure>' +
            '<div class="lightbox__nav">' +
            '<button type="button" class="lightbox__anterior">← Anterior</button>' +
            '<span class="lightbox__contador" aria-live="polite"></span>' +
            '<button type="button" class="lightbox__proxima">Próxima →</button>' +
            '</div></div>';
        document.body.appendChild(dialogo);

        imgGrande = dialogo.querySelector(".lightbox__img");
        legenda = dialogo.querySelector(".lightbox__legenda");
        contador = dialogo.querySelector(".lightbox__contador");
        btnAnterior = dialogo.querySelector(".lightbox__anterior");
        btnProxima = dialogo.querySelector(".lightbox__proxima");

        dialogo.querySelector(".lightbox__fechar").addEventListener("click", fechar);
        btnAnterior.addEventListener("click", function () { ir(-1); });
        btnProxima.addEventListener("click", function () { ir(1); });

        // Clique no fundo escuro (fora do conteúdo) fecha
        dialogo.addEventListener("click", function (e) {
            if (e.target === dialogo) fechar();
        });
        dialogo.addEventListener("keydown", function (e) {
            if (e.key === "ArrowLeft") ir(-1);
            if (e.key === "ArrowRight") ir(1);
        });
        // Esc (nativo) também dispara "close": devolve o foco à foto clicada
        dialogo.addEventListener("close", function () {
            document.documentElement.classList.remove("lightbox-aberto");
            if (origem) origem.focus();
        });
    }

    function mostrar() {
        var foto = lista[indice];
        imgGrande.src = foto.src;
        imgGrande.alt = foto.alt;
        legenda.textContent = foto.legenda;
        var varias = lista.length > 1;
        btnAnterior.hidden = btnProxima.hidden = contador.hidden = !varias;
        contador.textContent = (indice + 1) + " de " + lista.length;
    }

    function ir(passo) {
        if (lista.length < 2) return;
        indice = (indice + passo + lista.length) % lista.length;
        mostrar();
    }

    function abrir(botao) {
        if (!dialogo) criar();
        lista = Array.prototype.map.call(document.querySelectorAll(".galeria__item img"), function (i) {
            return { src: i.currentSrc || i.src, alt: i.alt || "", legenda: i.getAttribute("data-legenda") || i.alt || "" };
        });
        var imgs = document.querySelectorAll(".galeria__item img");
        indice = Array.prototype.indexOf.call(imgs, botao.querySelector("img"));
        if (indice < 0) indice = 0;
        origem = botao;
        mostrar();
        document.documentElement.classList.add("lightbox-aberto");
        if (typeof dialogo.showModal === "function") dialogo.showModal();
        else dialogo.setAttribute("open", "");
    }

    function fechar() {
        if (typeof dialogo.close === "function") dialogo.close();
        else { dialogo.removeAttribute("open"); document.documentElement.classList.remove("lightbox-aberto"); if (origem) origem.focus(); }
    }

    // Um único "ouvinte" na página serve para todas as fotos da galeria (delegação de eventos).
    document.addEventListener("click", function (e) {
        var botao = e.target.closest(".galeria__abrir");
        if (botao) abrir(botao);
    });
})();
