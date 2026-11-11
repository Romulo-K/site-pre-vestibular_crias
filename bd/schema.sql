-- =================================================================
-- schema.sql — SQL das tabelas do site Pré-Vestibular Social ONG Crias
-- Gerado por bd/bd.py em 10/11/2026 22:53 (Django 5.2.19, banco sqlite).
-- NÃO edite à mão: mude code/conteudo/models.py e gere de novo.
-- Tabelas: noticias, integrantes, galeria, depoimentos.
-- (As tabelas de login/usuários são do próprio Django: auth_*, django_*.)
-- =================================================================

-- ---------------------------------------------------------------
-- Migration conteudo.0001_initial
-- ---------------------------------------------------------------
BEGIN;
--
-- Create model Depoimento
--
CREATE TABLE "depoimentos" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome" varchar(120) NOT NULL, "turma" varchar(120) NOT NULL, "texto" text NOT NULL, "foto" varchar(100) NOT NULL, "autorizado" bool NOT NULL, "ativo" bool NOT NULL, "ordem" integer unsigned NOT NULL CHECK ("ordem" >= 0), "criado_em" datetime NOT NULL);
--
-- Create model FotoGaleria
--
CREATE TABLE "galeria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(150) NOT NULL, "imagem" varchar(100) NOT NULL, "descricao" varchar(200) NOT NULL, "legenda" varchar(200) NOT NULL, "categoria" varchar(12) NOT NULL, "data_atividade" date NULL, "uso_autorizado" bool NOT NULL, "criada_em" datetime NOT NULL);
--
-- Create model Integrante
--
CREATE TABLE "integrantes" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome" varchar(120) NOT NULL, "funcao" varchar(120) NOT NULL, "disciplina" varchar(80) NOT NULL, "biografia" text NOT NULL, "grupo" varchar(12) NOT NULL, "foto" varchar(100) NOT NULL, "foto_autorizada" bool NOT NULL, "ordem" integer unsigned NOT NULL CHECK ("ordem" >= 0), "ativo" bool NOT NULL, "criado_em" datetime NOT NULL, "atualizado_em" datetime NOT NULL);
--
-- Create model Noticia
--
CREATE TABLE "noticias" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(200) NOT NULL, "slug" varchar(220) NOT NULL UNIQUE, "resumo" varchar(300) NOT NULL, "texto" text NOT NULL, "capa" varchar(100) NOT NULL, "capa_descricao" varchar(200) NOT NULL, "autor" varchar(120) NOT NULL, "status" varchar(10) NOT NULL, "publicada_em" datetime NULL, "criada_em" datetime NOT NULL, "atualizada_em" datetime NOT NULL);
CREATE INDEX "integrantes_ativo_grupo_idx" ON "integrantes" ("ativo", "grupo", "ordem");
CREATE INDEX "noticias_status_data_idx" ON "noticias" ("status", "publicada_em" DESC);
COMMIT;
