from sqlalchemy import Column, Integer, String
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(50), nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(255))
    ciudad_municipio = Column(String(50))