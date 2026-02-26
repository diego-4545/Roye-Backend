from pydantic import BaseModel
from decimal import Decimal


class ProductoBase(BaseModel):
    id_original: str
    nombre: str
    id_categoria: int
    peso: str
    material: str
    precio_compra: Decimal
    precio_venta: Decimal
    stock: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    id_original: str | None = None
    nombre: str | None = None
    id_categoria: int | None = None
    peso: str | None = None
    material: str | None = None
    precio_compra: Decimal | None = None
    precio_venta: Decimal | None = None
    stock: int | None = None


class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True