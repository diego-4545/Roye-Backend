from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.detalle_venta import DetalleVenta
from app.schemas.detalle_venta import DetalleVentaCreate, DetalleVentaUpdate, DetalleVentaResponse

router = APIRouter(prefix="/detalle-ventas", tags=["Detalle Ventas"])


@router.post("/", response_model=DetalleVentaResponse)
def crear_detalle(datos: DetalleVentaCreate, db: Session = Depends(get_db)):

    nuevo = DetalleVenta(**datos.dict())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=List[DetalleVentaResponse])
def obtener_detalles(db: Session = Depends(get_db)):

    return db.query(DetalleVenta).all()


@router.get("/{id}", response_model=DetalleVentaResponse)
def obtener_detalle(id: int, db: Session = Depends(get_db)):

    detalle = db.query(DetalleVenta).filter(DetalleVenta.id == id).first()

    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    return detalle


@router.put("/{id}", response_model=DetalleVentaResponse)
def actualizar_detalle(id: int, datos: DetalleVentaUpdate, db: Session = Depends(get_db)):

    detalle = db.query(DetalleVenta).filter(DetalleVenta.id == id).first()

    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(detalle, key, value)

    db.commit()
    db.refresh(detalle)

    return detalle


@router.delete("/{id}")
def eliminar_detalle(id: int, db: Session = Depends(get_db)):

    detalle = db.query(DetalleVenta).filter(DetalleVenta.id == id).first()

    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    db.delete(detalle)
    db.commit()

    return {"mensaje": "Detalle eliminado"}