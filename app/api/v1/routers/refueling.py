from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_api_key
from app.db.session import get_db
from app.models.refueling import FuelType
from app.repositories.refueling import RefuelingRepository
from app.schemas.refueling import RefuelingCreate, RefuelingResponse
from app.services.refueling_service import RefuelingService

router = APIRouter()


async def get_refueling_service(db: AsyncSession = Depends(get_db)) -> RefuelingService:
    repository = RefuelingRepository(db)
    return RefuelingService(repository)


@router.post("/abastecimentos", response_model=RefuelingResponse, status_code=201)
async def create_refueling(
    refueling_in: RefuelingCreate,
    service: RefuelingService = Depends(get_refueling_service),
    api_key: str = Depends(get_api_key),
):
    """
    Recebe os dados do abastecimento.
    Verifica se o preço é 25% superior à média e marca flag de anomalia.
    """
    return await service.ingest_refueling(refueling_in)


@router.get("/abastecimentos", response_model=List[RefuelingResponse])
async def list_refuelings(
    skip: int = 0,
    limit: int = 100,
    tipo_combustivel: Optional[FuelType] = Query(
        None, description="Filtro por tipo de combustível"
    ),
    data: Optional[str] = Query(None, description="Filtro por data (YYYY-MM-DD)"),
    service: RefuelingService = Depends(get_refueling_service),
):
    """
    Lista os abastecimentos com paginação e filtros opcionais.
    """
    return await service.get_refuelings(
        skip=skip, limit=limit, fuel_type=tipo_combustivel, date=data
    )


@router.get("/motoristas/{cpf}/historico", response_model=List[RefuelingResponse])
async def get_driver_history(
    cpf: str, service: RefuelingService = Depends(get_refueling_service)
):
    """
    Retorna o histórico de abastecimentos de um motorista específico (por CPF).
    """
    return await service.get_driver_history(cpf)
