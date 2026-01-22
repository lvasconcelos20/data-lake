import enum

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func

from app.db.base import Base


class FuelType(str, enum.Enum):
    GASOLINA = "GASOLINA"
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"


class Refueling(Base):
    __tablename__ = "refuelings"

    id = Column(Integer, primary_key=True, index=True)
    id_posto = Column(Integer, nullable=False)
    data_hora = Column(DateTime(timezone=True), nullable=False)
    tipo_combustivel = Column(SAEnum(FuelType), nullable=False)
    preco_por_litro = Column(Float, nullable=False)
    volume_abastecido = Column(Float, nullable=False)
    cpf_motorista = Column(String, index=True, nullable=False)
    improper_data = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
