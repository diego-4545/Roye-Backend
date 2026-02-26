from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.deuda import Deuda
from app.schemas.deuda import DeudaCreate, DeudaUpdate, DeudaResponse

router = APIRouter(prefix="/deudas", tags=["Deudas"])


@router.post("/", response_model=DeudaResponse)
def crear_deuda(datos: DeudaCreate, db: Session = Depends(get_db)):

    nueva = Deuda(**datos.dict())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


@router.get("/", response_model=List[DeudaResponse])
def obtener_deudas(db: Session = Depends(get_db)):

    return db.query(Deuda).all()


@router.get("/{id}", response_model=DeudaResponse)
def obtener_deuda(id: int, db: Session = Depends(get_db)):

    deuda = db.query(Deuda).filter(Deuda.id == id).first()

    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

    return deuda


@router.put("/{id}", response_model=DeudaResponse)
def actualizar_deuda(id: int, datos: DeudaUpdate, db: Session = Depends(get_db)):

    deuda = db.query(Deuda).filter(Deuda.id == id).first()

    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(deuda, key, value)

    db.commit()
    db.refresh(deuda)

    return deuda


@router.delete("/{id}")
def eliminar_deuda(id: int, db: Session = Depends(get_db)):

    deuda = db.query(Deuda).filter(Deuda.id == id).first()

    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

    db.delete(deuda)
    db.commit()

    return {"mensaje": "Deuda eliminada"}