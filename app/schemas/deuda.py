from pydantic import BaseModel
from decimal import Decimal


class DeudaBase(BaseModel):
    id_cliente: int
    id_venta: int
    total: Decimal
    pendiente: Decimal
    estado: int


class DeudaCreate(DeudaBase):
    pass


class DeudaUpdate(BaseModel):
    pendiente: Decimal | None = None
    estado: int | None = None


class DeudaResponse(DeudaBase):
    id: int

    class Config:
        from_attributes = True