from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class VentaBase(BaseModel):
    id_cliente: int
    id_usuario: int
    total: Decimal
    tipo_pago: int


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    id_cliente: int | None = None
    id_usuario: int | None = None
    total: Decimal | None = None
    tipo_pago: int | None = None


class VentaResponse(VentaBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True