
# 📦 Sistema de Gerenciamento de Estoque Fullstack

Projeto completo com frontend em Vue.js e backend em FastAPI, com integração a banco de dados MySQL, autenticação via JWT e comunicação em tempo real via WebSocket.

---

## 🧰 Tecnologias Utilizadas

### 🔹 Front-End

- **Vue.js 3** — Framework progressivo para construção de interfaces web reativas  
- **Vue Router** — Gerenciamento de rotas SPA (Single Page Application)  
- **Tailwind CSS** — Framework utilitário para estilização com classes CSS  
- **Heroicons** — Biblioteca de ícones SVG compatível com Tailwind  
- **Vite** — Ferramenta de build e bundler moderna para Vue.js  
- **Axios** — Cliente HTTP usado para comunicação com o backend  
- **EventBus (Vue)** — Comunicação entre componentes independentes  

### 🔸 Back-End

- **Python 3.x** — Linguagem principal do servidor  
- **FastAPI** — Framework web assíncrono e rápido para criação de APIs REST e WebSocket  
- **Uvicorn** — Servidor ASGI usado para executar a aplicação FastAPI  
- **Starlette** — Toolkit assíncrono que serve de base para o FastAPI (middlewares, WebSockets, etc.)  
- **MySQL** — Banco de dados relacional usado para persistência dos dados  
- **MySQL Connector (mysql-connector-python)** — Driver oficial para conectar Python ao MySQL  

### 🔐 Autenticação e Segurança

- **python-jose** — Geração e verificação de tokens JWT  
- **PyJWT** — Manipulação de JWTs (token de autenticação)  
- **itsdangerous** — Geração de tokens seguros para sessão e validação  
- **email-validator** — Validação de e-mails no backend  
- **cryptography / rsa / ecdsa** — Suporte para operações criptográficas  

### 🧾 Manipulação de PDFs

- **pdfplumber** — Leitura e extração de texto de arquivos PDF  
- **pdfminer.six** — Biblioteca base usada para interpretar PDFs  
- **pypdfium2** — Renderização e manipulação de arquivos PDF  
- **Pillow** — Manipulação de imagens (usado em conjunto com PDFs)  

### 🔄 Comunicação em Tempo Real

- **websockets** — Comunicação via WebSocket (dashboard, atualizações em tempo real)  
- **FastAPI WebSocket** — Rotas específicas para conexões WebSocket  

### ⚙️ Utilitários e Outros

- **python-dotenv** — Leitura de variáveis de ambiente do arquivo `.env`  
- **Pydantic** — Validação de dados e criação de modelos (base do FastAPI)  
- **Watchfiles** — Recarga automática da aplicação durante desenvolvimento  
- **SessionMiddleware** — Controle de sessão no backend com cookies  
- **CORS Middleware** — Liberação de requisições do frontend (`localhost:5173`)  

---

## 📁 Estrutura do Projeto

### Frontend (`/frontend`)

```
frontend/
└── src/
    ├── main.js                 # Arquivo principal da aplicação (ponto de entrada)
    ├── App.vue                 # Componente raiz
    ├── assets/                 # Arquivos estáticos (imagens, ícones, etc.)
    │
    ├── components/             # Componentes reutilizáveis
    │   ├── layout/             # Componentes de layout (Nav-bar, Sidebar)
    │   └── ui/                 # Componentes de interface (botões, inputs, etc.)
    │
    ├── composables/            # Composables (lógica reutilizável com Composition API)
    ├── pages/                  # Páginas da aplicação (Cadastro.vue, Login.vue, etc.)
    ├── router/                 # Configuração de rotas com Vue Router
    └── services/               # Serviços responsáveis por comunicação e lógica externa
        ├── api.js              # Configuração e funções de chamadas HTTP (Axios) para o backend
        └── eventBus.js         # Canal de comunicação entre componentes usando Event Bus (Vue.js)
```

### Backend (`/backend`)

```
backend/
├── main.py                     # Ponto de entrada da aplicação FastAPI
├── requirements.txt            # Dependências do projeto
│
├── controller/                 # Lógica de controle das rotas
│   ├── produtos_controller.py  # Controlador para produtos
│   └── usuarios_controller.py  # Controlador para usuários
│
├── database/                   # Configurações e scripts de banco de dados
│   ├── db_model.py             # Carregamento de variáveis de ambiente (.env)
│   ├── db_mysql.py             # Conexão com o banco de dados MySQL
│   ├── test_db.py              # Script de teste de conexão ao banco
│   ├── sql/                    # Scripts SQL (procedures, criação de tabelas)
│   └── .env                    # Variáveis de ambiente (credenciais, etc.)
│
├── model/                      # Definições dos modelos de dados
│   ├── produtos_model.py       # Modelo de dados para produtos
│   └── usuarios_model.py       # Modelo de dados para usuários
│
├── router/                     # Arquivos com rotas expostas pela API
│   ├── produto_route.py        # Rotas relacionadas a produtos
│   ├── usuarios_router.py      # Rotas relacionadas a usuários
│   └── ws_router.py            # Rota de WebSocket (comunicação em tempo real)
│
├── utils/                      # Utilitários e funções auxiliares
│   ├── pdf_data.py             # Funções para geração/manipulação de PDFs
│   └── auth.py                 # Funções de autenticação/autorização
│
└── db_setup.py                 # Script para criação inicial do banco de dados
```

## 🚀 Instalação do Projeto

Este projeto possui backend (FastAPI + Python) e frontend (Vue.js + Vite) integrados e configurados para rodar juntos com um único comando via `setup.bat`.

### Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/)
- [Node.js + NPM](https://nodejs.org/)
- [Git](https://git-scm.com/)
- [MySQL](https://dev.mysql.com/downloads/installer/)

---

### 🔧 Passos para Executar

1. Clone o repositório:

```bash
git clone https://github.com/DSM2SEM2025/TimeGabrielPI.git
```

2. Acesse a pasta do projeto:

```bash
cd TimeGabriel-Front
```

3. Execute o script de setup:

```bash
.\setup.bat
```

Esse script realiza automaticamente:

- Criação e ativação de ambiente virtual do Python
- Instalação de dependências do backend (`requirements.txt`)
- Instalação de dependências do frontend (`npm install`)
- Inicialização simultânea do backend e do frontend

---

## 🖥️ Acesso à Aplicação

- Frontend: [http://localhost:5173](http://localhost:5173)  
- Backend (API): [http://localhost:8000](http://localhost:8000)

---

## 📦 Gerar Build de Produção

Se desejar gerar a versão de produção do frontend:

```bash
cd frontend
npm run build
npm run preview
```

---

## 👥 Autores

- Allan Martins Silva (https://github.com/allanmsilva23) — Desenvolvedor Back-end  
- Gabriel Marques da Silva (https://github.com/the-gabriel-marques) — Desenvolvedor Back-end
- Heitor Augusto de Carvalho Silva (https://github.com/HeitorAugustoC) — Desenvolvedor Back-end
- Jhon Deyvid Quispe Mamani (https://github.com/d-Jhon-b) - Desenvolvedor Back-end
- Pedro Henrique de Carvalho Silva (https://github.com/Bruxx092) - Desenvolvedor Front-end
- Roberto Tadashi Miura (https://github.com/RobertoFATEC24) - Desenvolvedor Front-end
- Vitor Luiz Soares da Silva (https://github.com/VitorVraal) - Desenvolvedor Front-end
