from pydantic import BaseModel
from decimal import Decimal


class DetalleVentaBase(BaseModel):
    id_producto: int
    id_venta: int
    precio: Decimal
    cantidad: int


class DetalleVentaCreate(DetalleVentaBase):
    pass


class DetalleVentaUpdate(BaseModel):
    id_producto: int | None = None
    id_venta: int | None = None
    precio: Decimal | None = None
    cantidad: int | None = None


class DetalleVentaResponse(DetalleVentaBase):
    id: int

    class Config:
        from_attributes = True