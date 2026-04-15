from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# En models/pago.py
class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True)
    id_detalle_venta = Column(Integer, ForeignKey("detalle_ventas.id"))  # ← CAMBIAR de id_deuda
    fecha = Column(DateTime, default=datetime.utcnow)
    cantidad = Column(Numeric(10,2))
    tipo_pago = Column(Integer)
    detalle_venta = relationship("DetalleVenta")