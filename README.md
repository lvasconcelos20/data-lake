# Data Lake Challenge

## Sobre o Projeto
Este projeto é uma API Backend desenvolvida para o setor de transportes da V-Lab. O objetivo central é gerenciar a ingestão de dados de abastecimento de uma frota nacional ("Data Lake"), garantindo validação de dados, persistência segura e detecção de anomalias em tempo real.

A aplicação foi construída visando robustez, escalabilidade e facilidade de manutenção, utilizando tecnologias modernas e práticas de Clean Code.

## Tecnologias Utilizadas (Stack)
*   **Linguagem**: Python 3.11+
*   **Framework Web**: FastAPI (Alta performance, suporte nativo a async/await)
*   **Banco de Dados**: PostgreSQL (Relacional)
*   **ORM**: SQLAlchemy (Async)
*   **Migrações**: Alembic
*   **Containerização**: Docker e Docker Compose
*   **Testes**: Pytest (com `httpx` e `aiosqlite`)
*   **Qualidade de Código**: Ruff e Black

## Arquitetura
O projeto segue o padrão **Service-Repository** para garantir a separação de responsabilidades:

1.  **Routers/Controllers (`app/api/v1`)**: Responsáveis apenas por receber as requisições HTTP, validar os schemas de entrada (Pydantic) e chamar a camada de serviço.
2.  **Services (`app/services`)**: Contém a lógica de negócio. Ex:
    *   Verificação de anomalia de preço (Regra dos 25%).
    *   Orquestração de chamadas ao banco de dados.
3.  **Repositories (`app/repositories`)**: Abstração da camada de dados. Executa as queries SQL puras ou via ORM, isolando o banco do resto da aplicação.
4.  **Models (`app/models`)**: Definição das tabelas do banco de dados.
5.  **Schemas (`app/schemas`)**: Contratos de dados (DTOs) para validação de entrada e saída.

## Funcionalidades Implementadas
*   **Ingestão de Abastecimentos (`POST /api/v1/abastecimentos`)**:
    *   Recebe dados do abastecimento.
    *   **Regra de Anomalia**: Verifica se o preço informado é 25% superior à média histórica do combustível. Se sim, marca `improper_data = True`.
*   **Lista de Abastecimentos (`GET /api/v1/abastecimentos`)**:
    *   Paginação suportada (`skip`, `limit`).
    *   **Filtros**: Permite filtrar por `tipo_combustivel` e `data`.
*   **Histórico do Motorista (`GET /api/v1/motoristas/{cpf}/historico`)**:
    *   Retorna todos os abastecimentos de um motorista específico.
*   **Autenticação**:
    *   Proteção via API Key (Header `x-api-key`).
*   **Testes Automatizados**:
    *   Cobertura de testes para ingestão, detecção de anomalia e filtros.

## Como Executar

### Pré-requisitos
*   Docker e Docker Compose instalados.

### Passo a Passo
1.  **Subir a aplicação**:
    ```bash
    docker-compose up --build
    ```
    Isso iniciará a API (porta 8000) e o banco de dados PostgreSQL (porta 5432).

2.  **Executar Migrações** (Na primeira execução):
    Com o container rodando:
    ```bash
    docker-compose exec app alembic upgrade head
    ```

3.  **Acessar a Documentação**:
    Abra o navegador em: [http://localhost:8000/docs](http://localhost:8000/docs)

### Testes
Para rodar os testes automatizados (necessário ambiente local com python configurado ou via docker):

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Executar testes
python -m pytest tests/
```

### Qualidade de Código (Linting)
Para formatar e verificar o código:
```bash
python -m black .
python -m ruff check . --fix
```
