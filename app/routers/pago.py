from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse

router = APIRouter(prefix="/pagos", tags=["Pagos"])

@router.post("/", response_model=PagoResponse)
def crear_pago(datos: PagoCreate, db: Session = Depends(get_db)):
    nuevo = Pago(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=List[PagoResponse])
def obtener_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()

@router.get("/{id}", response_model=PagoResponse)
def obtener_pago(id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

@router.put("/{id}", response_model=PagoResponse)
def actualizar_pago(id: int, datos: PagoUpdate, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(pago, key, value)
    db.commit()
    db.refresh(pago)
    return pago

@router.delete("/{id}")
def eliminar_pago(id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    db.delete(pago)
    db.commit()
    return {"mensaje": "Pago eliminado"}