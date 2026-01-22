# 🌐 API (`app/api`)

Esta camada contém os **Endpoints** (Rotas) da aplicação.
Ela usa o **FastAPI** para expor a lógica de negócio via HTTP.

## Estrutura
- **`v1/`**: Versionamento da API. Isso permite lançar uma v2 no futuro sem quebrar quem usa a v1.
- **`api.py`**: Agregador de rotas. Junta todos os roteadores (`routers`) em um só `api_router`.

## Rotas (`v1/routers`)

### `refueling.py`
- Define os verbos HTTP (`@router.post`, `@router.get`).
- **Injeção de Dependência**: Usa `Depends(get_refueling_service)` para obter uma instância pronta do Service.
- **API Key**: A rota POST exige `api_key: str = Depends(get_api_key)`.
- **Status Codes**: Define explicitamente `status_code=201` para criação, seguindo boas práticas REST.

### `health.py`
- Rota simples para monitoramento. Verifica se a conexão com o banco está viva (`SELECT 1`). Útil para orquestradores como Kubernetes.
