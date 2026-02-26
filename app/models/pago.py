from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)

    id_deuda = Column(Integer, ForeignKey("deudas.id"))

    fecha = Column(DateTime, default=datetime.utcnow)

    cantidad = Column(Numeric(10,2))

    tipo_pago = Column(Integer)

    deuda = relationship("Deuda")