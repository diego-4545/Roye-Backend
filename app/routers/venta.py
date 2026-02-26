from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.venta import Venta
from app.schemas.venta import VentaCreate, VentaUpdate, VentaResponse

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.post("/", response_model=VentaResponse)
def crear_venta(datos: VentaCreate, db: Session = Depends(get_db)):

    nueva = Venta(**datos.dict())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


@router.get("/", response_model=List[VentaResponse])
def obtener_ventas(db: Session = Depends(get_db)):

    return db.query(Venta).all()


@router.get("/{id}", response_model=VentaResponse)
def obtener_venta(id: int, db: Session = Depends(get_db)):

    venta = db.query(Venta).filter(Venta.id == id).first()

    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    return venta


@router.put("/{id}", response_model=VentaResponse)
def actualizar_venta(id: int, datos: VentaUpdate, db: Session = Depends(get_db)):

    venta = db.query(Venta).filter(Venta.id == id).first()

    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(venta, key, value)

    db.commit()
    db.refresh(venta)

    return venta


@router.delete("/{id}")
def eliminar_venta(id: int, db: Session = Depends(get_db)):

    venta = db.query(Venta).filter(Venta.id == id).first()

    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    db.delete(venta)
    db.commit()

    return {"mensaje": "Venta eliminada"}