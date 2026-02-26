from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    telefono: str | None = None
    direccion: str | None = None
    ciudad_municipio: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    ciudad_municipio: str | None = None


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True