from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)

    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))

    fecha = Column(DateTime, default=datetime.utcnow)

    total = Column(Numeric(10,2))

    tipo_pago = Column(Integer)

    cliente = relationship("Cliente")
    usuario = relationship("Usuario")