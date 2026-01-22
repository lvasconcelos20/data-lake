from typing import List, Optional

from app.models.refueling import FuelType, Refueling
from app.repositories.refueling import RefuelingRepository
from app.schemas.refueling import RefuelingCreate


class RefuelingService:
    def __init__(self, repository: RefuelingRepository):
        self.repository = repository

    async def ingest_refueling(self, data: RefuelingCreate) -> Refueling:
        """
        Ingere um novo registro de abastecimento.
        Verifica anomalia: se o preço > 25% da média histórica para aquele tipo de combustível.
        """
        # 1. Obter média histórica
        avg_price = await self.repository.get_average_price_by_fuel_type(
            data.tipo_combustivel
        )

        improper_data = False
        if avg_price is not None:
            # Lógica: O novo preço > avg_price * 1.25?
            threshold = avg_price * 1.25
            if data.preco_por_litro > threshold:
                improper_data = True

        # 2. Save
        return await self.repository.create(data, improper_data=improper_data)

    async def get_refuelings(
        self,
        skip: int = 0,
        limit: int = 100,
        fuel_type: Optional[FuelType] = None,
        date: Optional[str] = None,
    ) -> List[Refueling]:
        return await self.repository.get_all(
            skip=skip, limit=limit, fuel_type=fuel_type, date=date
        )

    async def get_driver_history(self, cpf: str) -> List[Refueling]:
        return await self.repository.get_by_driver(cpf)
