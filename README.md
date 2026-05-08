# Market Management — Back-end

API REST para gerenciamento de mini mercados desenvolvida em Python com Flask. Permite que cada mercado gerencie seu catálogo de produtos, registre vendas com múltiplos itens, acompanhe indicadores no dashboard e receba código de ativação via WhatsApp. Conta com painel administrativo para gerenciar todos os mercados cadastrados.

---

## Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| **Python** | 3.14 | Linguagem principal |
| **Flask** | 3.x | Framework web / HTTP |
| **Flask-SQLAlchemy** | 3.x | ORM — mapeamento objeto-relacional |
| **Flask-JWT-Extended** | 4.x | Autenticação via token JWT |
| **Werkzeug** | 3.x | Hash de senhas |
| **Twilio** | 9.x | Envio de código de ativação via WhatsApp |
| **python-dotenv** | — | Leitura de variáveis de ambiente |
| **SQLite** | — | Banco de dados (arquivo local) |

---

## Arquitetura

O projeto segue uma arquitetura em camadas inspirada no padrão **DDD (Domain-Driven Design)**:

```
backend/
├── run.py                          # Ponto de entrada da aplicação
├── requirements.txt                # Dependências
├── .env                            # Variáveis de ambiente (não commitado)
└── src/
    ├── routes.py                   # Registro de todas as rotas HTTP
    ├── config/
    │   └── data_base.py            # Configuração do SQLAlchemy e JWT
    ├── Domain/                     # Entidades de domínio (objetos puros)
    │   ├── user.py                 # UserDomain
    │   ├── product.py              # ProductDomain
    │   └── sale.py                 # SaleDomain
    ├── Infrastructure/
    │   ├── Model/                  # Modelos do banco (SQLAlchemy)
    │   │   ├── user.py             # Tabela users
    │   │   ├── product.py          # Tabela products
    │   │   ├── sale.py             # Tabela sales (itens de venda)
    │   │   └── sale_order.py       # Tabela sale_orders (pedidos)
    │   └── http/
    │       └── whats_app.py        # Integração Twilio WhatsApp
    └── Application/
        ├── Controllers/            # Recebem requisições e retornam respostas JSON
        │   ├── auth_controller.py
        │   ├── user_controller.py
        │   ├── product_controller.py
        │   ├── sale_controller.py
        │   ├── dashboard_controller.py
        │   └── admin_controller.py
        └── Service/                # Regras de negócio
            ├── user_service.py
            ├── product_service.py
            └── sale_service.py
```

### Fluxo de uma requisição

```
HTTP Request → routes.py → Controller → Service → Model (SQLAlchemy) → SQLite
                                      ↓
                               Domain Object → Controller → JSON Response
```

---

## Modelos de Dados

### `users`
| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer | Chave primária |
| name | String | Nome do mercado |
| cnpj | String | CNPJ único |
| email | String | E-mail único |
| phone | String | Telefone (WhatsApp) |
| password | String | Senha com hash bcrypt |
| status | String | `ACTIVE` ou `INACTIVE` |
| activation_code | String | Código de 4 dígitos para ativação |
| role | String | `SELLER` ou `ADMIN` |

### `products`
| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer | Chave primária |
| seller_id | Integer | FK → users |
| name | String | Nome do produto |
| price | Float | Preço unitário |
| quantity | Integer | Quantidade em estoque |
| status | String | `ACTIVE` ou `INACTIVE` |
| img | String | URL da imagem |
| categoria | String | Categoria do produto |

### `sale_orders`
| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer | Chave primária (ID do pedido) |
| seller_id | Integer | FK → users |
| total | Float | Valor total do pedido |
| created_at | DateTime | Data e hora |

### `sales`
| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer | Chave primária |
| order_id | Integer | FK → sale_orders |
| product_id | Integer | FK → products |
| seller_id | Integer | FK → users |
| quantidade | Integer | Quantidade vendida |
| preco_unitario | Float | Preço no momento da venda |
| created_at | DateTime | Data e hora |

---

## Endpoints

### Health
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/api` | — | Status da API |

### Autenticação
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/api/auth/login` | — | Login (sellers e admins) |

### Mercados (Sellers)
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/api/sellers` | — | Cadastrar novo mercado |
| POST | `/api/sellers/activate` | — | Ativar conta com código WhatsApp |
| GET | `/api/sellers/:id` | JWT | Buscar dados do mercado |
| PUT | `/api/sellers/:id` | JWT | Atualizar dados do mercado |
| PATCH | `/api/sellers/:id/inactivate` | JWT | Inativar mercado |

### Produtos
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/api/products` | JWT | Listar produtos do mercado autenticado |
| POST | `/api/products` | JWT | Criar produto |
| GET | `/api/products/:id` | JWT | Buscar produto |
| PUT | `/api/products/:id` | JWT | Atualizar produto |
| PATCH | `/api/products/:id/activate` | JWT | Ativar produto |
| PATCH | `/api/products/:id/inactivate` | JWT | Inativar produto |
| DELETE | `/api/products/:id` | JWT | Deletar produto |

### Vendas
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/api/sales` | JWT | Registrar pedido com múltiplos produtos |
| GET | `/api/sales` | JWT | Listar pedidos do mercado |

**Body do POST `/api/sales`:**
```json
{
  "items": [
    { "product_id": 1, "quantity": 3 },
    { "product_id": 4, "quantity": 1 }
  ]
}
```

### Dashboard
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/api/dashboard` | JWT | Indicadores de estoque, vendas por dia, top produtos e por categoria |

**Resposta do GET `/api/dashboard`:**
```json
{
  "total_produtos": 10,
  "total_estoque": 350,
  "total_vendido": 1250.00,
  "num_vendas": 42,
  "baixo_estoque": 2,
  "vendas_por_dia": [{ "dia": "2026-05-01", "total": 150.00 }],
  "top_produtos": [{ "nome": "Água", "quantidade": 50 }],
  "vendas_por_categoria": [{ "categoria": "Bebidas", "total": 300.00 }]
}
```

### Admin
| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/api/admin/register` | Secret key | Cadastrar administrador |
| GET | `/api/admin/sellers` | JWT Admin | Listar todos os mercados |
| DELETE | `/api/admin/sellers/:id` | JWT Admin | Deletar mercado |
| PATCH | `/api/admin/sellers/:id/toggle` | JWT Admin | Ativar/desativar mercado |

**Body do POST `/api/admin/register`:**
```json
{
  "secret": "valor-do-ADMIN_SECRET-no-.env",
  "name": "Admin",
  "email": "admin@email.com",
  "password": "senha123"
}
```

---

## Categorias de Produtos

`Bebidas` · `Alimentos` · `Laticínios` · `Higiene` · `Limpeza` · `Hortifruti` · `Cereais e Grãos` · `Outros`

---

## Fluxo de Cadastro e Ativação

```
1. POST /api/sellers        → cria conta com status INACTIVE
                            → gera código de 4 dígitos
                            → envia código via WhatsApp (Twilio Sandbox)

2. POST /api/sellers/activate → valida telefone + código
                               → status passa para ACTIVE

3. POST /api/auth/login     → retorna token JWT válido por 1h
```

---

## Como rodar

### Pré-requisitos

- Python 3.10+
- Conta no [Twilio](https://www.twilio.com) com sandbox WhatsApp configurado

### Instalação

```bash
git clone https://github.com/Gesoaress/market-backend.git
cd market-backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
.venv/bin/python -m pip install -r requirements.txt
```

Crie o arquivo `.env` na raiz do projeto:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=+14155238886
ADMIN_SECRET=sua-chave-secreta-admin
JWT_SECRET_KEY=sua-chave-jwt-secreta
```

### Executar

```bash
.venv/bin/python run.py
```

API disponível em `http://localhost:5000`.  
O banco de dados SQLite (`market_management.db`) é criado automaticamente na primeira execução.

### Criar o primeiro administrador

```bash
curl -X POST http://localhost:5000/api/admin/register \
  -H "Content-Type: application/json" \
  -d '{"secret":"sua-chave-secreta-admin","name":"Admin","email":"admin@email.com","password":"senha123"}'
```

---

## Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `TWILIO_ACCOUNT_SID` | SID da conta Twilio |
| `TWILIO_AUTH_TOKEN` | Token de autenticação Twilio |
| `TWILIO_WHATSAPP_NUMBER` | Número do sandbox WhatsApp (`+14155238886`) |
| `ADMIN_SECRET` | Chave secreta para criar administradores |
| `JWT_SECRET_KEY` | Chave para assinar tokens JWT |

---

## Projeto relacionado

- **Front-end:** [market-frontend](https://github.com/Gesoaress/market-frontend)
