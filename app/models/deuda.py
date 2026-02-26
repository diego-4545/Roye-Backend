from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Deuda(Base):
    __tablename__ = "deudas"

    id = Column(Integer, primary_key=True, index=True)

    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    id_venta = Column(Integer, ForeignKey("ventas.id"))

    total = Column(Numeric(10,2))
    pendiente = Column(Numeric(10,2))

    estado = Column(Integer)

    cliente = relationship("Cliente")
    venta = relationship("Venta")