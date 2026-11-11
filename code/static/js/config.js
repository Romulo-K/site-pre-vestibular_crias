// config.js - links e contatos do site num lugar só
// trocando aqui, todos os botões do site mudam juntos
// se deixar "" (vazio), o botão fica desativado avisando que o link ainda não foi configurado
// formulário: usar o link de RESPOSTA do google forms (termina em /viewform), nunca o de edição
const SITE_CONFIG = {
    // Inscrições (Google Forms)
    formularioAluno: "",        // ex.: "https://forms.gle/..."
    formularioVoluntario: "",   // ex.: "https://forms.gle/..."

    // Área do aluno
    classroom: "",              // link da turma no Google Classroom
    drive: "",                  // pasta de materiais no Google Drive
    meet: "",                   // link de encontros no Google Meet

    // Contato oficial (fornecido pela ONG)
    email: "",                  // ex.: "contato@exemplo.org" (sem "mailto:")
    whatsapp: "",               // ex.: "https://wa.me/55DDDNUMERO"
    telefone: "",               // ex.: "(00) 00000-0000" (apenas texto)
    endereco: "",               // ex.: "Rua Exemplo, 123 — Bairro, Cidade/UF" (só se a ONG autorizar divulgar)
    horario: "",                // ex.: "Segunda a sexta, das 14h às 18h"
    mapa: "",                   // link do Google Maps (opcional: se vazio, o botão "Ver no mapa" some)

    // Redes sociais (opcionais: se vazio, o link é escondido)
    instagram: "",
    facebook: "",
    youtube: ""
};
