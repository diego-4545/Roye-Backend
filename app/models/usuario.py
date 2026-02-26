from sqlalchemy import Column, Integer, String
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    usuario = Column(String(15), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)