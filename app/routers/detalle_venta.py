from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.detalle_venta import DetalleVenta
from app.models.venta import Venta
from app.models.cliente import Cliente
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


@router.get("/clientes/{cliente_id}/detalles-pendientes")
def obtener_detalles_pendientes(cliente_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de venta pendientes de un cliente (con saldo restante)"""
    detalles = db.query(DetalleVenta).join(
        Venta, DetalleVenta.id_venta == Venta.id
    ).join(
        Cliente, Venta.id_cliente == Cliente.id
    ).filter(
        Venta.id_cliente == cliente_id,
        Venta.tipo_pago == 2  # Solo ventas a pagos
    ).all()
    
    resultado = []
    for detalle in detalles:
        subtotal = detalle.precio * detalle.cantidad
        pendiente = subtotal - (detalle.monto_pagado or 0)
        
        if pendiente > 0:  # Solo incluir si hay pendiente
            resultado.append({
                "id": detalle.id,
                "nombre_producto": detalle.producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_unitario": float(detalle.precio),
                "subtotal": float(subtotal),
                "monto_pagado": float(detalle.monto_pagado or 0),
                "pendiente": float(pendiente),
                "id_venta": detalle.id_venta
            })
    
    return resultado

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