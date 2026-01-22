import re
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class FuelTypeEnum(str, Enum):
    GASOLINA = "GASOLINA"
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"


class RefuelingBase(BaseModel):
    id_posto: int
    data_hora: datetime
    tipo_combustivel: FuelTypeEnum
    preco_por_litro: float = Field(gt=0, description="Preço por litro deve ser positivo")
    volume_abastecido: float = Field(gt=0, description="Volume deve ser positivo")
    cpf_motorista: str

    @field_validator("cpf_motorista")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        # Verificação simples de regex para formato
        # Removendo não dígitos
        cpf_clean = re.sub(r"\D", "", v)
        if len(cpf_clean) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        # Poderia adicionar validação de checksum aqui para validade "real"
        return cpf_clean


class RefuelingCreate(RefuelingBase):
    pass


class RefuelingResponse(RefuelingBase):
    id: int
    improper_data: bool
    created_at: datetime

    class Config:
        from_attributes = True
