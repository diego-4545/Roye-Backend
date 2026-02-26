from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)

    id_producto = Column(Integer, ForeignKey("productos.id"))
    id_venta = Column(Integer, ForeignKey("ventas.id"))

    precio = Column(Numeric(10,2))
    cantidad = Column(Integer)

    producto = relationship("Producto")
    venta = relationship("Venta")