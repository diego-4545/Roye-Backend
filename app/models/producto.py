from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    id_original = Column(String(50))
    nombre = Column(String(100), nullable=False)

    id_categoria = Column(Integer, ForeignKey("categorias.id"))

    peso = Column(String(20))
    material = Column(String(50))

    precio_compra = Column(Numeric(10,2))
    precio_venta = Column(Numeric(10,2))

    stock = Column(Integer)

    categoria = relationship("Categoria", back_populates="productos")