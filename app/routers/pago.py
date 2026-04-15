from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.pago import Pago
from app.models.detalle_venta import DetalleVenta
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse

router = APIRouter(prefix="/pagos", tags=["Pagos"])

@router.post("/pagos/")
def crear_pago(pago_data: PagoCreate, db: Session = Depends(get_db)):
    # ... código existente de validación ...
    
    detalle_venta = db.query(DetalleVenta).filter(
        DetalleVenta.id == pago_data.id_detalle_venta
    ).first()
    
    if not detalle_venta:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    
    subtotal = detalle_venta.precio * detalle_venta.cantidad
    if detalle_venta.monto_pagado + pago_data.cantidad > subtotal:
        raise HTTPException(status_code=400, detail="El pago supera el total del producto")
    
    deuda = db.query(Deuda).filter(
        Deuda.id_venta == detalle_venta.id_venta
    ).first()
    
    if deuda:
        if deuda.pendiente >= pago_data.cantidad:
            deuda.pendiente -= pago_data.cantidad
        else:
            raise HTTPException(status_code=400, detail="El pago supera la deuda pendiente")
    
    detalle_venta.monto_pagado += pago_data.cantidad
    
    nuevo_pago = Pago(**pago_data.dict())
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    
    return nuevo_pago

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