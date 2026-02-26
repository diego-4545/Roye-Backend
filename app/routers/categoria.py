from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorias"])


# CREATE
@router.post("/", response_model=CategoriaResponse)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    nueva = Categoria(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# GET ALL
@router.get("/", response_model=List[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


# GET BY ID
@router.get("/{id}", response_model=CategoriaResponse)
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria


# UPDATE
@router.put("/{id}", response_model=CategoriaResponse)
def actualizar_categoria(id: int, datos: CategoriaUpdate, db: Session = Depends(get_db)):

    categoria = db.query(Categoria).filter(Categoria.id == id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)

    return categoria


# DELETE
@router.delete("/{id}")
def eliminar_categoria(id: int, db: Session = Depends(get_db)):

    categoria = db.query(Categoria).filter(Categoria.id == id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    db.delete(categoria)
    db.commit()

    return {"mensaje": "Categoria eliminada"}