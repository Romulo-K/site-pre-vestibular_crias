/* =====================================================================
   NOTÍCIAS
   Use apenas notícias reais fornecidas pela ONG.

   COMO TROCAR: apague os itens de exemplo (placeholder: true) e cole as
   notícias reais usando o modelo abaixo (as mais novas primeiro).
   A Home mostra as 3 primeiras.

   Modelo:
   {
       titulo: "Título da notícia",
       data: "2026-10-06",              // formato AAAA-MM-DD
       categoria: "Eventos",
       imagem: "assets/noticias/arquivo.jpg",
       alt: "Descrição da imagem para leitores de tela",
       resumo: "Resumo curto.",
       texto: "Texto completo.",
       link: "noticias.html"            // opcional: para onde o botão "Ler notícia" leva
   }
   ===================================================================== */
const FOTO_NOTICIA_PROVISORIA = "assets/placeholders/foto-paisagem.svg";

const noticias = [
    {
        placeholder: true,
        titulo: "[TÍTULO DA NOTÍCIA]",
        data: "",
        categoria: "[CATEGORIA]",
        imagem: FOTO_NOTICIA_PROVISORIA,
        alt: "Imagem ilustrativa de notícia (substituir por foto real da ONG)",
        resumo: "[RESUMO DA NOTÍCIA]",
        texto: "",
        link: "noticias.html"
    },
    {
        placeholder: true,
        titulo: "[TÍTULO DA NOTÍCIA]",
        data: "",
        categoria: "[CATEGORIA]",
        imagem: FOTO_NOTICIA_PROVISORIA,
        alt: "Imagem ilustrativa de notícia (substituir por foto real da ONG)",
        resumo: "[RESUMO DA NOTÍCIA]",
        texto: "",
        link: "noticias.html"
    },
    {
        placeholder: true,
        titulo: "[TÍTULO DA NOTÍCIA]",
        data: "",
        categoria: "[CATEGORIA]",
        imagem: FOTO_NOTICIA_PROVISORIA,
        alt: "Imagem ilustrativa de notícia (substituir por foto real da ONG)",
        resumo: "[RESUMO DA NOTÍCIA]",
        texto: "",
        link: "noticias.html"
    }
];
