from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):

    nuevo = Cliente(**datos.dict())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=List[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):

    return db.query(Cliente).all()


@router.get("/{id}", response_model=ClienteResponse)
def obtener_cliente(id: int, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(Cliente.id == id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente


@router.put("/{id}", response_model=ClienteResponse)
def actualizar_cliente(id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(Cliente.id == id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)

    return cliente


@router.delete("/{id}")
def eliminar_cliente(id: int, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(Cliente.id == id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(cliente)
    db.commit()

    return {"mensaje": "Cliente eliminado"}