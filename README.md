# Vault API

API principal do projeto de carteira de investimentos. Responsável por autenticação (OAuth2 + JWT) e pelo CRUD dos ativos de cada usuário. Para calcular valor atual e rentabilidade, o Vault se comunica com a API **Ticker**, que consulta a Brapi.

## Pré-requisitos

- Python 3.12 ou superior
- [uv](https://docs.astral.sh/uv/) instalado
- A API **Ticker** rodando (necessária apenas para a rota `/portfolio/summary`)

## Instalação

Dentro da pasta `vault/`:

```bash
uv sync
```

Esse comando cria o ambiente virtual (`.venv/`) e instala todas as dependências listadas no `pyproject.toml`.

## Configuração

Copie o arquivo de exemplo e ajuste os valores:

```bash
cp .env.example .env
```

| Variável       | Descrição                                                            | Padrão                   |
| -------------- | -------------------------------------------------------------------- | ------------------------ |
| `DATABASE_URL` | String de conexão do banco (SQLite por padrão)                       | `sqlite:///./vault.db`   |
| `SECRET_KEY`   | Chave usada para assinar o JWT. **Troque em qualquer ambiente real** | `change-this-secret-key` |
| `TICKER_URL`   | Endereço onde a API Ticker está rodando                              | `http://localhost:8001`  |

## Executando

```bash
uv run uvicorn app.main:app --reload --port 8000
```

A documentação interativa (Swagger) fica disponível em:

```
http://localhost:8000/docs
```

O banco de dados e as tabelas são criados automaticamente na primeira execução.

## Rotas disponíveis

| Método | Rota                 | Autenticação | Descrição                                            |
| ------ | -------------------- | ------------ | ---------------------------------------------------- |
| POST   | `/auth/register`     | Não          | Cria um novo usuário                                 |
| POST   | `/auth/login`        | Não          | Autentica e devolve o token JWT                      |
| POST   | `/assets`            | Sim          | Cadastra um ativo na carteira do usuário logado      |
| GET    | `/assets`            | Sim          | Lista os ativos, com filtro, ordenação e paginação   |
| GET    | `/assets/{id}`       | Sim          | Detalha um ativo específico                          |
| PUT    | `/assets/{id}`       | Sim          | Atualiza quantidade e/ou preço médio                 |
| DELETE | `/assets/{id}`       | Sim          | Remove um ativo                                      |
| GET    | `/portfolio/summary` | Sim          | Calcula valor atual e rentabilidade (chama o Ticker) |

### Parâmetros de `GET /assets`

- `ticker` — filtra por um ticker específico (ex: `?ticker=PETR4`)
- `sort` — campo de ordenação: `ticker`, `quantity`, `average_price` ou `created_at`
- `order` — `asc` ou `desc`
- `page` — número da página (padrão: `1`)
- `limit` — itens por página (padrão: `10`, máximo `100`)

Exemplo:

```
GET /assets?ticker=PETR4&sort=quantity&order=desc&page=1&limit=10
```

## Como testar pelo Swagger

1. Abra `http://localhost:8000/docs`
2. Execute `POST /auth/register` para criar um usuário
3. Execute `POST /auth/login` com o mesmo email e senha, e copie o `access_token` retornado
4. Clique no botão **Authorize** (ícone de cadeado, no topo da página) e cole o token
5. A partir daí, todas as rotas protegidas ficam liberadas para teste na própria tela

## Executando com Docker

```bash
docker build -t vault .
docker run -p 8000:8000 --env-file .env vault
```

Se o Ticker também estiver rodando em um container separado, ajuste `TICKER_URL` no `.env` para `http://host.docker.internal:8001`.

## Estrutura do projeto

```
vault/
├── pyproject.toml
├── .env.example
├── Dockerfile
└── app/
    ├── main.py
    ├── database.py
    ├── models/         # Tabelas do banco (User, Asset)
    ├── schemas/         # Contratos de entrada/saída (Pydantic)
    ├── auth/            # Autenticação OAuth2 + JWT
    └── routes/          # Rotas de assets e portfolio
```

## Problemas comuns

**`ModuleNotFoundError`** — rode `uv sync` novamente dentro da pasta `vault/`.

**Pylance reclamando de import não encontrado no VS Code** — selecione o interpretador correto: `Ctrl+Shift+P` → "Python: Select Interpreter" → escolha o `.venv` da pasta `vault/`.

**`401 Unauthorized` em `/assets`** — confirme que clicou em "Authorize" no Swagger após o login, e que o token não expirou (validade padrão: 60 minutos).

**`503` ou `504` em `/portfolio/summary`** — confirme que a API Ticker está rodando e que `TICKER_URL` no `.env` aponta para o endereço correto.
