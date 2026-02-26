from pydantic import BaseModel

# Base
class UsuarioBase(BaseModel):
    usuario: str
    rol: str


# Create
class UsuarioCreate(UsuarioBase):
    contraseña: str


# Update
class UsuarioUpdate(BaseModel):
    usuario: str | None = None
    contraseña: str | None = None
    rol: str | None = None


# Response
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True