# Cantina Django

Um sistema web de gerenciamento de cantina escolar desenvolvido com Django e Python. O projeto tem como objetivo facilitar a organização dos produtos e das informações da cantina, reunindo as principais funcionalidades administrativas em uma interface simples e intuitiva.

A aplicação utiliza templates Django para renderizar as páginas, CSS para a estilização da interface e SQLite para armazenar os dados durante o desenvolvimento.

## Situação atual

**Objetivo:** desenvolver um sistema web para auxiliar no gerenciamento de uma cantina escolar.

**Funcionalidades do projeto:** interface de dashboard, gerenciamento de produtos e estrutura para organizar os dados da cantina.

**Desenvolvimento:** projeto acadêmico em evolução, utilizado para praticar desenvolvimento web com Python, Django, HTML, CSS e banco de dados.

As funcionalidades disponíveis dependem da implementação presente na versão atual do código-fonte.

## Conjunto de tecnologias

- **Framework:** Django
- **Linguagem:** Python
- **Banco de dados:** SQLite
- **Frontend:** HTML5, CSS3 e templates Django
- **Gerenciamento de dependências:** pip
- **Ambiente virtual:** Python `venv`
- **Controle de versão:** Git e GitHub
- **Editor recomendado:** Visual Studio Code

## Estrutura do projeto

Estrutura simplificada da aplicação:

```text
cantina-django/
├── cantina/                 # Configurações do projeto
│   ├── settings.py          # Configurações do Django
│   ├── urls.py              # Rotas principais
│   └── wsgi.py
├── produtos/                # Aplicação da cantina
│   ├── migrations/          # Migrações do banco de dados
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Lógica das páginas
│   ├── urls.py              # Rotas da aplicação, se existente
│   └── admin.py             # Configuração do painel administrativo
├── templates/               # Templates HTML, se existentes
├── static/                  # CSS, imagens e outros arquivos estáticos
├── manage.py                # Interface de comandos do Django
├── requirements.txt         # Dependências do projeto, se criado
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Documentação do projeto
```

A estrutura pode variar conforme a organização atual dos arquivos.

## Funcionalidades

### Dashboard
Página inicial do sistema, utilizada como ponto de acesso às áreas de gerenciamento da cantina.

### Produtos
Área destinada ao gerenciamento dos produtos cadastrados, de acordo com as operações implementadas no sistema.

### Interface
Páginas desenvolvidas com HTML e CSS, utilizando templates Django para integrar a interface à aplicação Python.

### Banco de dados
Utilização do SQLite para persistir os dados da aplicação durante o desenvolvimento local.

> Funcionalidades como vendas, controle financeiro, relatórios, autenticação e gerenciamento de pessoas devem ser documentadas como implementadas somente quando estiverem disponíveis no código do projeto.

## Desenvolvimento local

### Pré-requisitos

Antes de executar a aplicação, instale:

- Python 3.13 ou outra versão compatível com as dependências do projeto.
- Visual Studio Code, recomendado para editar o código.
- Git, caso queira clonar o repositório.

Verifique a instalação do Python:

```powershell
python --version
```

Verifique o pip:

```powershell
python -m pip --version
```

### 1. Obter o projeto

Caso já tenha os arquivos, abra a pasta do projeto no terminal.

Para clonar o repositório, utilize:

```powershell
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```powershell
cd cantina-django
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório. Se o projeto estiver em outro diretório, utilize o caminho correspondente.

### 2. Criar o ambiente virtual

O ambiente virtual isola as bibliotecas utilizadas pelo projeto, evitando conflitos com outros projetos Python instalados no computador.

```powershell
python -m venv .venv
```

Esse comando cria o diretório `.venv` na raiz do projeto.

### 3. Ativar o ambiente virtual

No Windows, utilizando PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Prompt de Comando (CMD):

```cmd
.venv\Scripts\activate.bat
```

Após a ativação, o terminal normalmente exibirá `(.venv)` no início da linha.

Se o PowerShell bloquear a execução do script, execute o comando abaixo na sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, tente ativar o ambiente novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

Atualize o gerenciador de pacotes:

```powershell
python -m pip install --upgrade pip
```

Se o repositório possuir um arquivo `requirements.txt`, instale as dependências registradas nele:

```powershell
python -m pip install -r requirements.txt
```

Caso o arquivo ainda não exista, instale o Django:

```powershell
python -m pip install django
```

Verifique a versão instalada:

```powershell
python -m django --version
```

### 5. Configurar o banco de dados

Execute as migrações do projeto:

```powershell
python manage.py migrate
```

Se você tiver alterado os modelos e precisar criar novas migrações, execute primeiro:

```powershell
python manage.py makemigrations
```

Em seguida:

```powershell
python manage.py migrate
```

O Django utilizará o banco configurado em `settings.py`. Em uma configuração padrão, o SQLite é utilizado para armazenar os dados localmente.

### 6. Iniciar o servidor

Execute:

```powershell
python manage.py runserver
```

Acesse a aplicação pelo navegador:

http://127.0.0.1:8000/

Para encerrar o servidor, pressione `Ctrl + C` no terminal.

## Comandos úteis

| Comando | Descrição |
|---|---|
| `python manage.py runserver` | Inicia o servidor de desenvolvimento. |
| `python manage.py check` | Verifica problemas na configuração do projeto. |
| `python manage.py makemigrations` | Cria migrações para alterações nos modelos. |
| `python manage.py migrate` | Aplica as migrações no banco de dados. |
| `python manage.py showmigrations` | Lista as migrações e seus estados. |
| `python manage.py createsuperuser` | Cria um superusuário para o Django Admin. |
| `python manage.py test` | Executa os testes automatizados disponíveis. |
| `deactivate` | Desativa o ambiente virtual. |

## Gerenciamento das dependências

Para registrar as dependências instaladas no ambiente virtual, execute:

```powershell
python -m pip freeze > requirements.txt
```

Em uma nova instalação, crie e ative o ambiente virtual e execute:

```powershell
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` facilita a reprodução do ambiente de desenvolvimento em outro computador.

## Banco de dados

O SQLite é adequado para o desenvolvimento local e não exige a instalação de um servidor de banco de dados separado.

Os dados ficam armazenados no arquivo definido pela configuração do Django, geralmente `db.sqlite3`.

O arquivo do banco de dados pode conter registros cadastrados durante a utilização do sistema. Antes de publicá-lo no GitHub, verifique se ele contém informações pessoais ou dados que não devem ser compartilhados.

## Boas práticas

- Mantenha o ambiente virtual `.venv` fora do repositório.
- Utilize `requirements.txt` para documentar as dependências.
- Preserve os arquivos de migração existentes.
- Não publique senhas, chaves secretas ou outras credenciais.
- Utilize Git para registrar as alterações realizadas no projeto.
- Não utilize o servidor `runserver` como servidor de produção.

Exemplo de `.gitignore`:

```gitignore
.venv/
venv/
__pycache__/
*.py[cod]
db.sqlite3
.env
```

A inclusão de `db.sqlite3` no `.gitignore` é apropriada quando o banco local não deve ser versionado. Se houver necessidade de distribuir um banco de demonstração, essa decisão deve ser feita separadamente.

## Testes e verificações

Para verificar a configuração do projeto:

```powershell
python manage.py check
```

Para executar os testes automatizados disponíveis:

```powershell
python manage.py test
```

Esses comandos devem ser executados na pasta que contém o arquivo `manage.py`, com o ambiente virtual ativado.

## Objetivo educacional

O Cantina Django foi desenvolvido com o propósito de aplicar conhecimentos de desenvolvimento web, incluindo:

- Desenvolvimento de aplicações com Django.
- Organização de projetos Python.
- Criação de páginas com HTML e CSS.
- Integração entre views, templates e modelos.
- Persistência de dados com SQLite.
- Criação e utilização de ambientes virtuais.
- Versionamento de código com Git e GitHub.


## Licença

A licença do projeto deve ser definida conforme os objetivos de distribuição e utilização do código. Caso ainda não exista um arquivo de licença no repositório, nenhuma licença específica deve ser presumida.

---

Desenvolvido para fins educacionais com Python e Django.
