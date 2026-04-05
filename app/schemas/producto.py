from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class ProductoBase(BaseModel):
    id_original: str
    nombre: str
    id_categoria: int
    peso: str
    material: str
    precio_compra: Decimal
    precio_venta: Decimal
    stock: int
    imagen: Optional[str] = None  


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    id_original: Optional[str] = None
    nombre: Optional[str] = None
    id_categoria: Optional[int] = None
    peso: Optional[str] = None
    material: Optional[str] = None
    precio_compra: Optional[Decimal] = None
    precio_venta: Optional[Decimal] = None
    stock: Optional[int] = None
    imagen: Optional[str] = None  


class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True