from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class PagoBase(BaseModel):
    id_deuda: int
    cantidad: Decimal
    tipo_pago: int


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    cantidad: Decimal | None = None
    tipo_pago: int | None = None


class PagoResponse(PagoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True