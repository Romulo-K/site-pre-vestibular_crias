/* =====================================================================
   ATIVIDADES E GALERIA
   tipo deve ser: "aulas", "palestras", "simulados", "convivencia" ou "passeios"
   (é o mesmo nome das seções da página atividades.html).
   Use apenas fotos reais e autorizadas.

   COMO TROCAR: em cada atividade, escreva a descrição oficial fornecida
   pela ONG, troque "imagem" pelo caminho da foto real (ex.: "assets/atividades/aulas.jpg")
   e atualize o "alt" descrevendo o que a foto mostra. Depois remova placeholder: true.

   Modelo:
   {
       tipo: "aulas",
       titulo: "Aulas",
       descricao: "Texto oficial fornecido pela ONG.",
       imagem: "assets/atividades/arquivo.jpg",
       alt: "Descrição da imagem"
   }
   ===================================================================== */
const FOTO_PAISAGEM_PROVISORIA = "assets/placeholders/foto-paisagem.svg";

const atividades = [
    {
        placeholder: true,
        tipo: "aulas",
        titulo: "Aulas",
        descricao: "[DESCRIÇÃO OFICIAL DAS AULAS]",
        imagem: FOTO_PAISAGEM_PROVISORIA,
        alt: "Imagem ilustrativa de aula (substituir por foto real da ONG)"
    },
    {
        placeholder: true,
        tipo: "palestras",
        titulo: "Palestras",
        descricao: "[DESCRIÇÃO OFICIAL DAS PALESTRAS]",
        imagem: FOTO_PAISAGEM_PROVISORIA,
        alt: "Imagem ilustrativa de palestra (substituir por foto real da ONG)"
    },
    {
        placeholder: true,
        tipo: "simulados",
        titulo: "Simulados",
        descricao: "[DESCRIÇÃO OFICIAL DOS SIMULADOS]",
        imagem: FOTO_PAISAGEM_PROVISORIA,
        alt: "Imagem ilustrativa de simulado (substituir por foto real da ONG)"
    },
    {
        placeholder: true,
        tipo: "convivencia",
        titulo: "Convivência",
        descricao: "[DESCRIÇÃO OFICIAL DOS MOMENTOS DE CONVIVÊNCIA]",
        imagem: FOTO_PAISAGEM_PROVISORIA,
        alt: "Imagem ilustrativa de momento de convivência (substituir por foto real da ONG)"
    },
    {
        placeholder: true,
        tipo: "passeios",
        titulo: "Passeios",
        descricao: "[DESCRIÇÃO OFICIAL DOS PASSEIOS]",
        imagem: FOTO_PAISAGEM_PROVISORIA,
        alt: "Imagem ilustrativa de passeio (substituir por foto real da ONG)"
    }
];

/* Fotos da galeria (página atividades.html).
   Enquanto esta lista estiver vazia, a página mostra espaços reservados.
   Modelo: { imagem: "assets/atividades/foto.jpg", alt: "Descrição" } */
const galeria = [
    // [ADICIONAR FOTOS REAIS AQUI]
];
