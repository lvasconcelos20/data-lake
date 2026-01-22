import argparse
import os
import random
import requests
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração
API_URL = "http://localhost:8000/api/v1/abastecimentos"
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
HEADERS = {
    "x-api-key": SECRET_KEY,
    "Content-Type": "application/json"
}

fake = Faker('pt_BR')

FUEL_TYPES = ["GASOLINA", "ETANOL", "DIESEL"]

def generate_refueling_data(force_anomaly: bool = False):
    """Gera dados de abastecimento aleatórios válidos."""
    # Gera uma data aleatória dentro dos últimos 30 dias
    date_obj = fake.date_time_between(start_date="-30d", end_date="now")
    
    fuel_type = random.choice(FUEL_TYPES)
    
    if force_anomaly:
        # Gera um preço que provavelmente será uma anomalia (ex: > 10.0)
        # Faixa normal é 4.0 - 7.0
        price = round(random.uniform(15.0, 20.0), 3)
    else:
        price = round(random.uniform(4.0, 7.0), 3)

    return {
        "id_posto": random.randint(1, 100),
        "data_hora": date_obj.isoformat(),
        "tipo_combustivel": fuel_type,
        "preco_por_litro": price,
        "volume_abastecido": round(random.uniform(10.0, 80.0), 2),
        "cpf_motorista": fake.cpf()
    }

def run_load_test(count: int, dry_run: bool = False, anomaly: bool = False):
    """
    Runs the load test.
    :param count: Número de requisições a enviar.
    :param dry_run: Se True, imprime dados sem enviar requisições.
    :param anomaly: Se True, gera dados anômalos (preços altos).
    """
    print(f"Starting load test with {count} records...")
    print(f"Target: {API_URL}")
    print(f"Dry Run: {dry_run}")
    print(f"Anomaly Mode: {anomaly}")
    
    success_count = 0
    error_count = 0

    for i in range(count):
        data = generate_refueling_data(force_anomaly=anomaly)
        
        if dry_run:
            print(f"[{i+1}/{count}] Generated: {data}")
            continue

        try:
            response = requests.post(API_URL, json=data, headers=HEADERS)
            if response.status_code == 201:
                success_count += 1
                resp_json = response.json()
                is_improper = resp_json.get('improper_data', False)
                print(f"[{i+1}/{count}] SUCCESS: ID={resp_json.get('id', 'N/A')} Improper={is_improper} Price={data['preco_por_litro']}")
            else:
                error_count += 1
                print(f"[{i+1}/{count}] FAILED ({response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"[{i+1}/{count}] ERROR: {str(e)}")

    print("\n--- Load Test Summary ---")
    print(f"Total Requests: {count}")
    print(f"Success: {success_count}")
    print(f"Failed: {error_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de teste de carga para API de Transporte")
    parser.add_argument("--count", type=int, default=50, help="Número de requisições a gerar")
    parser.add_argument("--dry-run", action="store_true", help="Gera dados mas não envia requisições")
    parser.add_argument("--anomaly", action="store_true", help="Força geração de dados anômalos (preços altos)")
    
    args = parser.parse_args()
    
    run_load_test(args.count, args.dry_run, args.anomaly)
