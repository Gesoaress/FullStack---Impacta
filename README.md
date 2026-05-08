# Market Management — Back-end

API REST para gerenciamento de mini mercados, desenvolvida em Python com Flask. Controla vendedores, produtos e vendas, com autenticação JWT e notificações via WhatsApp pelo Twilio.

---

## Tecnologias

- **Python 3** + **Flask**
- **SQLAlchemy** — ORM para banco de dados
- **Flask-JWT-Extended** — autenticação via token JWT
- **Twilio** — envio de código de ativação via WhatsApp
- **MySQL 8** — banco de dados relacional
- **Docker** + **Docker Compose**

---

## Arquitetura

```
src/
├── Domain/          # Entidades (User, Product, Sale)
├── Application/
│   ├── Controllers/ # Recebem as requisições HTTP
│   └── Service/     # Regras de negócio
├── Infrastructure/  # Integrações externas (WhatsApp)
├── config/          # Configurações da aplicação
└── routes.py        # Definição das rotas
```

---

## Endpoints

### Health
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api` | Status da API |

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/auth/login` | Login do vendedor |

### Vendedores
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/sellers` | Cadastrar vendedor |
| POST | `/api/sellers/activate` | Ativar conta via código WhatsApp |
| GET | `/api/sellers/:id` | Buscar vendedor |
| PUT | `/api/sellers/:id` | Atualizar vendedor |
| PATCH | `/api/sellers/:id/inactivate` | Inativar vendedor |

### Produtos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/products` | Listar produtos |
| POST | `/api/products` | Criar produto |
| GET | `/api/products/:id` | Buscar produto |
| PUT | `/api/products/:id` | Atualizar produto |
| PATCH | `/api/products/:id/activate` | Ativar produto |
| PATCH | `/api/products/:id/inactivate` | Inativar produto |
| DELETE | `/api/products/:id` | Deletar produto |

### Vendas
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/sales` | Registrar venda |
| GET | `/api/sales` | Listar vendas |
| GET | `/api/sales/:id` | Buscar venda |

### Dashboard
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/dashboard` | Indicadores gerais de vendas e estoque |

---

## Como rodar

### Com Docker (recomendado)

```bash
git clone https://github.com/Gesoaress/FullStack---Impacta.git
cd FullStack---Impacta
```

Crie o arquivo `.env`:

```env
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

Suba os containers:

```bash
docker-compose up --build
```

API disponível em `http://localhost:5000`.

### Sem Docker

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

---

## Projeto relacionado

- **Front-end:** [market-frontend](https://github.com/Gesoaress/market-frontend)
