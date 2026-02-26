from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):

    nuevo = Usuario(**datos.dict())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=List[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):

    return db.query(Usuario).all()


@router.get("/{id}", response_model=UsuarioResponse)
def obtener_usuario(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete("/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado"}