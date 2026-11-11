// config.js - links e contatos do site
// agora eles vêm do painel (/admin/ > Links e contatos do site)
// o base.html coloca os dados na página num <script id="site-config"> e aqui eu só leio
// se um link estiver vazio, o botão fica desativado avisando que ainda não foi configurado
const elementoConfig = document.getElementById("site-config");
const SITE_CONFIG = elementoConfig ? JSON.parse(elementoConfig.textContent) : {};
