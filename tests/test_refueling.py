import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_refueling(client: AsyncClient):
    payload = {
        "id_posto": 1,
        "data_hora": "2024-01-20T10:00:00",
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 5.50,
        "volume_abastecido": 40.0,
        "cpf_motorista": "12345678900",
    }
    response = await client.post("/api/v1/abastecimentos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["preco_por_litro"] == 5.50
    assert data["improper_data"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_anomaly_detection_logic(client: AsyncClient):
    # 1. Popula dados para estabelecer média
    # Média será 4.0
    setup_payloads = [
        {
            "id_posto": 1,
            "data_hora": "2024-01-10T10:00:00",
            "tipo_combustivel": "ETANOL",
            "preco_por_litro": 4.0,
            "volume_abastecido": 10,
            "cpf_motorista": "11111111111",
        },
        {
            "id_posto": 1,
            "data_hora": "2024-01-11T10:00:00",
            "tipo_combustivel": "ETANOL",
            "preco_por_litro": 4.0,
            "volume_abastecido": 10,
            "cpf_motorista": "11111111111",
        },
    ]
    for p in setup_payloads:
        await client.post("/api/v1/abastecimentos", json=p)

    # 2. Limite = 4.0 * 1.25 = 5.0

    # CASO A: Preço = 4.50 (Abaixo do limite) -> Adequado
    payload_ok = {
        "id_posto": 1,
        "data_hora": "2024-01-12T10:00:00",
        "tipo_combustivel": "ETANOL",
        "preco_por_litro": 4.50,
        "volume_abastecido": 10,
        "cpf_motorista": "11111111111",
    }
    resp_ok = await client.post("/api/v1/abastecimentos", json=payload_ok)
    assert resp_ok.status_code == 201
    assert resp_ok.json()["improper_data"] is False

    # CASO B: Preço = 6.00 (Acima do limite 5.0) -> Impróprio/Anomalia
    payload_anomaly = {
        "id_posto": 1,
        "data_hora": "2024-01-13T10:00:00",
        "tipo_combustivel": "ETANOL",
        "preco_por_litro": 6.00,
        "volume_abastecido": 10,
        "cpf_motorista": "11111111111",
    }
    resp_bad = await client.post("/api/v1/abastecimentos", json=payload_anomaly)
    assert resp_bad.status_code == 201
    assert resp_bad.json()["improper_data"] is True


@pytest.mark.asyncio
async def test_filter_refuelings(client: AsyncClient):
    # Popula dados mistos
    # 2 DIESEL, 1 GASOLINA do setup
    # Garante que temos dados distintos
    p_diesel = {
        "id_posto": 2,
        "data_hora": "2024-02-01T10:00:00",
        "tipo_combustivel": "DIESEL",
        "preco_por_litro": 6.0,
        "volume_abastecido": 100,
        "cpf_motorista": "22222222222",
    }
    await client.post("/api/v1/abastecimentos", json=p_diesel)

    p_gas = {
        "id_posto": 2,
        "data_hora": "2024-02-02T10:00:00",
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 5.0,
        "volume_abastecido": 50,
        "cpf_motorista": "22222222222",
    }
    await client.post("/api/v1/abastecimentos", json=p_gas)

    # Filtra por DIESEL
    resp = await client.get("/api/v1/abastecimentos?tipo_combustivel=DIESEL")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) >= 1
    for item in items:
        assert item["tipo_combustivel"] == "DIESEL"

    # Filtra por Data
    # "2024-02-01" -> Deve encontrar o de DIESEL
    resp_date = await client.get("/api/v1/abastecimentos?data=2024-02-01")
    assert resp_date.status_code == 200
    items_date = resp_date.json()
    assert len(items_date) >= 1
    for item in items_date:
        # Verifica se a parte da data corresponde
        assert item["data_hora"].startswith("2024-02-01")
