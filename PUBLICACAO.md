# Publicação do site no PythonAnywhere

Guia para colocar o site no ar (e para atualizar depois). Tudo é feito pelo navegador, no site do
PythonAnywhere: o seu computador **não** vira servidor. O banco (`db.sqlite3`) e as fotos (`media/`)
ficam no servidor do PythonAnywhere.

Nos comandos abaixo, troque **`SEUUSUARIO`** pelo nome de usuário da conta do PythonAnywhere.
O endereço do site será `https://SEUUSUARIO.pythonanywhere.com`.

---

## Parte 1 — No seu computador: enviar a versão final para a branch `main`

O PythonAnywhere vai baixar o código da `main` do GitHub.

```bash
cd ~/site-pre-vestibular_crias
git switch main
git pull
git merge django
git push
```

A partir daqui você pode trabalhar direto na `main` (`git switch main`).

---

## Parte 2 — No PythonAnywhere: instalar o site (uma vez só)

### 2.1 Abrir um terminal
Entre em <https://www.pythonanywhere.com>, aba **Consoles** → **Bash**. Abre um terminal no navegador.

### 2.2 Baixar o código do GitHub
```bash
git clone https://github.com/Romulo-K/site-pre-vestibular_crias.git
cd site-pre-vestibular_crias
```

### 2.3 Ver as versões de Python disponíveis
```bash
ls /usr/bin/python3.1*
```
Use a **maior versão entre 3.10 e 3.13** que aparecer (ex.: `python3.13`). Nos próximos passos, troque
`3.13` pela versão escolhida, **sempre a mesma**.

### 2.4 Criar o ambiente virtual e instalar o Django
```bash
mkvirtualenv --python=/usr/bin/python3.13 precrias
pip install -r code/requirements.txt
```
O terminal passa a mostrar `(precrias)`. Se fechar e abrir outro terminal, ative de novo com `workon precrias`.

### 2.5 Criar o arquivo de configuração `.env` do servidor
Um comando cria o arquivo já com uma chave secreta nova (troque `SEUUSUARIO`):
```bash
cd ~/site-pre-vestibular_crias/code
python -c "from django.core.management.utils import get_random_secret_key as g; print('DEBUG=0\nSECRET_KEY=' + g() + '\nALLOWED_HOSTS=SEUUSUARIO.pythonanywhere.com\nSITE_EM_TESTE=1')" > .env
cat .env
```
Confira que aparecem 4 linhas. **Não compartilhe** a `SECRET_KEY` com ninguém.

### 2.6 Criar o banco, juntar os arquivos estáticos e criar a sua conta do painel
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```
No `createsuperuser`, a senha não aparece enquanto você digita (é normal). Use 10+ caracteres com letras e
números. *(As contas oficiais da coordenação serão criadas na entrega, Etapa 12.)*

### 2.7 Criar o "web app"
1. Aba **Web** → **Add a new web app** → **Next**.
2. Escolha **Manual configuration** (**não** escolha "Django").
3. Escolha a **mesma versão de Python** do passo 2.3 → **Next**.

### 2.8 Configurar o web app (ainda na aba Web)
Na seção **Code**:
- **Source code:** `/home/SEUUSUARIO/site-pre-vestibular_crias/code`
- **Working directory:** `/home/SEUUSUARIO/site-pre-vestibular_crias/code`

Na seção **Virtualenv**: digite `precrias` e confirme (vira `/home/SEUUSUARIO/.virtualenvs/precrias`).

Na seção **Static files**, adicione duas linhas:

| URL | Directory |
|---|---|
| `/static/` | `/home/SEUUSUARIO/site-pre-vestibular_crias/code/staticfiles` |
| `/media/` | `/home/SEUUSUARIO/site-pre-vestibular_crias/code/media` |

Na seção **Security**: ligue **Force HTTPS**.

### 2.9 Editar o arquivo WSGI
Na seção **Code**, clique no link do **WSGI configuration file**
(`/var/www/SEUUSUARIO_pythonanywhere_com_wsgi.py`). **Apague tudo** e cole (troque `SEUUSUARIO`):

```python
import os
import sys

caminho = "/home/SEUUSUARIO/site-pre-vestibular_crias/code"
if caminho not in sys.path:
    sys.path.insert(0, caminho)

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Clique em **Save**.

### 2.10 Ligar o site
Volte para a aba **Web** e clique no botão verde **Reload**. Abra `https://SEUUSUARIO.pythonanywhere.com`.
O site deve aparecer com a faixa amarela **"Versão de teste"**. O painel fica em `/admin/`.

---

## Parte 3 — Atualizar o site depois de uma mudança

No seu computador: `git add -A`, `git commit -m "..."`, `git push` (na `main`). Depois, no
PythonAnywhere (aba **Consoles** → Bash):

```bash
cd ~/site-pre-vestibular_crias
git pull
workon precrias
pip install -r code/requirements.txt
cd code
python manage.py migrate
python manage.py collectstatic --noinput
```
E na aba **Web**, clique em **Reload**. O banco e as fotos do servidor **não** são apagados por isso.

---

## Parte 4 — Manutenção mínima

- **Renovação mensal (plano gratuito):** na aba **Web**, clique no botão para estender o prazo do site
  (algo como "Run until 1 month from today"). O PythonAnywhere manda e-mail antes de vencer. Se esquecer,
  o site sai do ar, mas os dados continuam lá: é só clicar no botão e depois em **Reload**.
- **Lançamento oficial:** troque `SITE_EM_TESTE=1` por `SITE_EM_TESTE=0` no arquivo
  `/home/SEUUSUARIO/site-pre-vestibular_crias/code/.env` (aba **Files**, abre num editor) e clique em
  **Reload**. A faixa "Versão de teste" some e o Google passa a poder mostrar o site.
- **Esqueci a senha do painel:** outra conta da coordenação troca em **/admin/ → Usuários**. Sem nenhuma
  conta disponível, no terminal do PythonAnywhere: `workon precrias`, `cd ~/site-pre-vestibular_crias/code`,
  `python manage.py changepassword NOME_DO_USUARIO`.

## Se der erro
- Aba **Web** → seção **Log files** → abra o **Error log**: a última linha costuma dizer o problema.
- `DisallowedHost`: o `ALLOWED_HOSTS` do `.env` está diferente do endereço do site.
- Site sem estilo (sem cores): confira os caminhos de **Static files** e rode `collectstatic` de novo.
- `ImproperlyConfigured: Defina SECRET_KEY`: o `.env` não está em `code/` ou está vazio.
- Depois de qualquer correção, clique em **Reload**.
