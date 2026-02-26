from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoResponse)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):

    nuevo = Producto(**datos.dict())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=List[ProductoResponse])
def obtener_productos(db: Session = Depends(get_db)):

    return db.query(Producto).all()


@router.get("/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):

    producto = db.query(Producto).filter(Producto.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto


@router.put("/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):

    producto = db.query(Producto).filter(Producto.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(producto, key, value)

    db.commit()
    db.refresh(producto)

    return producto


@router.delete("/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):

    producto = db.query(Producto).filter(Producto.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

    return {"mensaje": "Producto eliminado"}