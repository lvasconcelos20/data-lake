from typing import List, Optional
from datetime import date as py_date
from datetime import datetime

from sqlalchemy import Date, cast, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refueling import FuelType, Refueling
from app.schemas.refueling import RefuelingCreate


class RefuelingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, refueling_in: RefuelingCreate, improper_data: bool = False
    ) -> Refueling:
        db_refueling = Refueling(
            id_posto=refueling_in.id_posto,
            data_hora=refueling_in.data_hora,
            tipo_combustivel=refueling_in.tipo_combustivel,
            preco_por_litro=refueling_in.preco_por_litro,
            volume_abastecido=refueling_in.volume_abastecido,
            cpf_motorista=refueling_in.cpf_motorista,
            improper_data=improper_data,
        )
        self.session.add(db_refueling)
        await self.session.commit()
        await self.session.refresh(db_refueling)
        return db_refueling

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        fuel_type: Optional[FuelType] = None,
        date: Optional[str] = None,
    ) -> List[Refueling]:
        query = (
            select(Refueling)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Refueling.data_hora))
        )

        if fuel_type:
            query = query.where(Refueling.tipo_combustivel == fuel_type)

        if date:
            # Analisa a string de entrada para um objeto de data para lidar com vários formatos ISO
            # e evitar incompatibilidade de tipo no PostgreSQL (DATE = VARCHAR)
            try:
                # Tenta YYYY-MM-DD simples primeiro
                filter_date = py_date.fromisoformat(date)
            except ValueError:
                try:
                    # Tenta ISO 8601 completo (como 2024-02-20T10:35:00Z)
                    filter_date = datetime.fromisoformat(date.replace("Z", "+00:00")).date()
                except ValueError:
                    # Se inválido, poderíamos lançar um erro ou apenas ignorar.
                    # Por enquanto, vamos deixar passar ou usar uma comparação segura.
                    filter_date = None

            if filter_date:
                from datetime import time
                # Cria intervalo para o dia inteiro: 00:00:00 até 23:59:59.999999
                start_dt = datetime.combine(filter_date, time.min)
                end_dt = datetime.combine(filter_date, time.max)
                
                query = query.where(
                    Refueling.data_hora >= start_dt, 
                    Refueling.data_hora <= end_dt
                )

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_by_driver(self, cpf: str) -> List[Refueling]:
        result = await self.session.execute(
            select(Refueling)
            .where(Refueling.cpf_motorista == cpf)
            .order_by(desc(Refueling.data_hora))
        )
        return result.scalars().all()

    async def get_average_price_by_fuel_type(
        self, fuel_type: FuelType
    ) -> Optional[float]:
        # Calcula a média puramente a partir do banco de dados
        result = await self.session.execute(
            select(func.avg(Refueling.preco_por_litro)).where(
                Refueling.tipo_combustivel == fuel_type
            )
        )
        avg_price = result.scalar()
        return avg_price
