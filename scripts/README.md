# Script de Teste de Carga (Load Test)

Este script (`load_data.py`) gera dados aleatórios e válidos (CPFs, datas, etc) utilizando a biblioteca `Faker` e envia requisições `POST` para a API de Abastecimentos.

## Pré-requisitos

Certifique-se de que o ambiente virtual está ativo e as dependências instaladas:

```bash
pip install -r requirements.txt
```

A API deve estar rodando localmente (ex: via Docker Compose):
```bash
docker-compose up
```

## Como usar

Execute o script a partir da raiz do projeto:

```bash
python scripts/load_data.py --count 50
```

### Argumentos

- `--count N`: Define o número de requisições a serem enviadas (padrão: 50).
- `--dry-run`: Gera os dados e imprime no terminal, mas **não** envia para a API. Útil para validar o formato dos dados.

## Verificando os Resultados

### 1. No Terminal
O script imprimirá o ID de cada registro criado com sucesso:
```text
Starting load test with 5 records...
Target: http://localhost:8000/api/v1/abastecimentos
[1/5] SUCCESS: 118
[2/5] SUCCESS: 119
[3/5] SUCCESS: 120
...
--- Load Test Summary ---
Total Requests: 5
Success: 5
Failed: 0
```

### 2. Na API (Swagger UI)
Acesse [http://localhost:8000/docs](http://localhost:8000/docs) e utilize o endpoint `GET /api/v1/abastecimentos` para listar os últimos registros inseridos.

### 3. Via Curl/Terminal
Você pode verificar os últimos 5 registros inseridos com o comando:

```bash
curl -s "http://localhost:8000/api/v1/abastecimentos?limit=5"
```
