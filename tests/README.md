# Testes Automatizados

Este diretório contém os testes automatizados da aplicação, desenvolvidos utilizando `pytest` e `pytest-asyncio`.

## Estrutura

- `conftest.py`: Configurações globais dos testes (fixtures), incluindo a criação do banco de dados de teste (SQLite em memória ou Postgres separado) e cliente HTTP assíncrono.
- `test_refueling.py`: Testes de integração para os endpoints de abastecimento (`/api/v1/abastecimentos`).

## Pré-requisitos

Certifique-se de que as dependências de desenvolvimento estão instaladas:

```bash
pip install -r requirements.txt
```

As principais bibliotecas utilizadas são:
- `pytest`
- `pytest-asyncio`
- `httpx` (para fazer requisições assíncronas nos testes)

## Como Rodar os Testes

Os testes devem ser executados **a partir da raiz do projeto** para garantir que as importações e configurações do `pytest.ini` funcionem corretamente.

### 1. Rodar todos os testes
```bash
pytest
```

### 2. Rodar testes com logs detalhados (stdout)
Para ver os prints e logs durante a execução:
```bash
pytest -s
```

### 3. Rodar um arquivo específico
```bash
pytest tests/test_refueling.py
```

### 4. Rodar uma função de teste específica
```bash
pytest tests/test_refueling.py::test_create_refueling_success
```

## Observações

- Os testes utilizam um banco de dados isolado (geralmente SQLite em memória ou um banco de teste configurado no `conftest.py`) para não interferir nos dados reais da aplicação.
- A configuração `asyncio_mode = auto` já está definida no arquivo `pytest.ini` na raiz do projeto.
