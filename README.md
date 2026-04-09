# SisGeOS — Sistema de Gestão de Ordens de Serviço

> **UNIVESP — Projeto Integrador I, II e III**
> DRP03-PJI110-SALA-002GRUPO-006 © 2025

Sistema web para abertura, acompanhamento e encerramento de ordens de serviço de TI em ambiente militar, com interface web e API REST.

---

## Funcionalidades

- Abertura de ordens de serviço (notebooks, microcomputadores e controle de acesso)
- Fluxo de status: **Aberta → Execução → Finalizada**
- Controle de compras e fornecedores
- Cadastro de empresas/fornecedores
- Controle de acesso por grupos de permissão
- API REST com autenticação por token
- Documentação interativa da API (Swagger / Redoc)
- Auto-logout por inatividade

## Grupos de Permissão

| Grupo | Permissões |
|---|---|
| **Administrador** | Acesso total — criar, executar, finalizar e excluir ordens; gerenciar usuários e empresas |
| **Usuario** | Abrir e visualizar ordens de serviço |
| **Tecnico** | Visualizar, executar e finalizar ordens de serviço |
| **Compras** | Visualizar ordens com material pendente; gerenciar fornecedores e status de compra |

> Os grupos são criados e gerenciados via painel administrativo (`/admin/`).

---

## Tecnologias

- **Python 3.12** / **Django 5.1**
- **Django REST Framework** + **drf-spectacular** (OpenAPI 3)
- **django-crispy-forms** + **crispy-bootstrap5**
- **django-auto-logout**
- **Gunicorn** (produção)
- **SQLite** (banco de dados)
- **Docker** / **Docker Compose**

---

## Como Executar

### Com Docker (recomendado)

```bash
git clone <url-do-repositorio>
cd ordemservico_project
docker-compose up --build
```

A aplicação ficará disponível em `http://localhost:8000`.

### Localmente

**Pré-requisitos:** Python 3.12+

```bash
git clone <url-do-repositorio>
cd ordemservico_project

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

A aplicação ficará disponível em `http://localhost:8000`.

---

## Configuração Inicial

1. Acesse `/admin/` com o superusuário criado.
2. Crie os grupos: **Administrador**, **Usuario**, **Tecnico**, **Compras**.
3. Atribua os usuários aos respectivos grupos.

---

## API REST

A API utiliza autenticação por **Token**.

### Obter token

```http
POST /api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Resposta:**
```json
{
  "token": "abc123...",
  "user_id": 1,
  "username": "seu_usuario",
  "grupos": ["Tecnico"]
}
```

### Usar o token nas requisições

```http
Authorization: Token abc123...
```

### Endpoints principais

| Método | Endpoint | Descrição | Grupos |
|---|---|---|---|
| `GET` | `/api/ordens/` | Listar ordens | Admin, Usuario, Tecnico |
| `POST` | `/api/ordens/` | Criar ordem | Admin, Usuario, Tecnico |
| `GET` | `/api/ordens/{id}/` | Detalhar ordem | Admin, Usuario, Tecnico |
| `PATCH` | `/api/ordens/{id}/executar/` | Registrar execução | Admin, Tecnico |
| `PATCH` | `/api/ordens/{id}/finalizar/` | Registrar finalização | Admin, Tecnico |
| `DELETE` | `/api/ordens/{id}/` | Excluir ordem | Administrador |
| `GET` | `/api/compras/` | Ordens com material pendente | Admin, Compras |
| `PATCH` | `/api/compras/{id}/` | Atualizar fornecedor/status | Admin, Compras |
| `GET` | `/api/empresas/` | Listar empresas | Admin, Compras |
| `POST` | `/api/empresas/` | Cadastrar empresa | Admin, Compras |

### Documentação interativa

| URL | Formato |
|---|---|
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | Redoc |
| `/api/schema/` | OpenAPI 3 (JSON/YAML) |

---

## Estrutura do Projeto

```
ordemservico_project/
├── ordemservico_project/   # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── middleware.py
├── ordens/                 # App principal
│   ├── models.py           # OrdemDeServico, Empresa
│   ├── views.py            # Views web (controle por grupos)
│   ├── api_views.py        # ViewSets da API REST
│   ├── serializers.py
│   ├── forms/
│   ├── templates/
│   ├── urls.py
│   └── api_urls.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## Licença

Projeto acadêmico desenvolvido para a disciplina **Projeto Integrador III** da [UNIVESP](https://univesp.br/).
