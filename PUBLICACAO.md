# Como coloquei o site no ar (PythonAnywhere)

Anotações do passo a passo que eu segui pra publicar o site no PythonAnywhere.
Serve pra mim e pra quem for mexer no site depois.

- Usuário do PythonAnywhere: **PreVestibularCrias**
- Endereço do site: **https://prevestibularcrias.pythonanywhere.com**
- O site, o banco (`db.sqlite3`) e as fotos (`media/`) ficam no servidor deles, não no meu computador.

---

## 1. No meu computador: mandar tudo pra branch main

O PythonAnywhere baixa o código da `main` do GitHub.

```bash
cd ~/site-pre-vestibular_crias
git switch main
git pull
git push
```

## 2. No PythonAnywhere: instalar o site (só uma vez)

Tudo pelo navegador, em https://www.pythonanywhere.com, aba **Consoles → Bash** (abre um terminal).

**2.1 Baixar o código**
```bash
git clone https://github.com/Romulo-K/site-pre-vestibular_crias.git
cd site-pre-vestibular_crias
```

**2.2 Ver quais versões do Python tem** e usar a maior entre 3.10 e 3.13 (aqui vou usar a 3.13 de exemplo)
```bash
ls /usr/bin/python3.1*
```

**2.3 Criar o ambiente virtual e instalar as bibliotecas**
```bash
mkvirtualenv --python=/usr/bin/python3.13 precrias
pip install -r code/requirements.txt
```
Se abrir outro terminal depois, ativa de novo com `workon precrias`.

**2.4 Criar o .env do servidor** (esse comando já gera uma chave secreta nova)
```bash
cd ~/site-pre-vestibular_crias/code
python -c "from django.core.management.utils import get_random_secret_key as g; print('DEBUG=0\nSECRET_KEY=' + g() + '\nALLOWED_HOSTS=prevestibularcrias.pythonanywhere.com\nSITE_EM_TESTE=1')" > .env
cat .env
```
Tem que aparecer 4 linhas. A SECRET_KEY não pode ser compartilhada.

**2.5 Criar o banco, juntar os arquivos estáticos e criar o login do painel**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

**2.6 Criar o web app**
Aba **Web** → **Add a new web app** → **Manual configuration** (NÃO escolher "Django") → mesma versão do Python do passo 2.2.

**2.7 Configurar o web app** (ainda na aba Web)

- Code → Source code: `/home/PreVestibularCrias/site-pre-vestibular_crias/code`
- Code → Working directory: `/home/PreVestibularCrias/site-pre-vestibular_crias/code`
- Virtualenv: `precrias`
- Static files:

| URL | Directory |
|---|---|
| `/static/` | `/home/PreVestibularCrias/site-pre-vestibular_crias/code/staticfiles` |
| `/media/` | `/home/PreVestibularCrias/site-pre-vestibular_crias/code/media` |

- Security → ligar **Force HTTPS**

**2.8 Arquivo WSGI**
Na parte Code, clicar no link do WSGI configuration file (algo como
`/var/www/prevestibularcrias_pythonanywhere_com_wsgi.py`), apagar tudo e colar:

```python
import os
import sys

caminho = "/home/PreVestibularCrias/site-pre-vestibular_crias/code"
if caminho not in sys.path:
    sys.path.insert(0, caminho)

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Salvar.

**2.9 Ligar o site**
Voltar na aba **Web** e clicar no botão verde **Reload**. Pronto, o site abre em
https://prevestibularcrias.pythonanywhere.com com a faixa amarela de "Versão de teste".

---

## 3. Atualizar o site depois de mudar alguma coisa

No meu computador: `git add -A`, `git commit -m "..."` e `git push`.

No PythonAnywhere (Consoles → Bash):
```bash
cd ~/site-pre-vestibular_crias
git pull
workon precrias
pip install -r code/requirements.txt
cd code
python manage.py migrate
python manage.py collectstatic --noinput
```
E depois **Reload** na aba Web. Isso não apaga o banco nem as fotos do servidor.

---

## 4. Manutenção

- **Todo mês:** na aba Web clicar no botão de estender o prazo ("Run until 1 month from today"), senão o site sai do ar. O PythonAnywhere manda e-mail avisando. Se esquecer, nada é perdido: é só clicar no botão e no Reload.
- **Lançar o site de verdade (tirar a faixa de teste):** na aba **Files**, abrir `/home/PreVestibularCrias/site-pre-vestibular_crias/code/.env`, trocar `SITE_EM_TESTE=1` por `SITE_EM_TESTE=0`, salvar e dar Reload.
- **Esqueceram a senha do painel:** no terminal do PythonAnywhere:
  ```bash
  workon precrias
  cd ~/site-pre-vestibular_crias/code
  python manage.py changepassword NOME_DO_USUARIO
  ```

## Se der erro

- Aba Web → Log files → **Error log**. A última linha normalmente diz o problema.
- `DisallowedHost` → o ALLOWED_HOSTS do .env tá diferente do endereço do site.
- Site sem cor nenhuma → conferir os caminhos do Static files e rodar o `collectstatic` de novo.
- Erro falando da `SECRET_KEY` → o .env não está na pasta `code/` ou está vazio.
- `No module named 'dotenv'` → faltou rodar o `pip install -r code/requirements.txt` com o `workon precrias` ativado.
- Depois de qualquer correção: **Reload**.
