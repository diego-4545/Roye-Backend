from fastapi import FastAPI, Depends
from app.database import engine, Base
from app.security import verificar_api_key

from app.routers import (
    usuario,
    producto,
    venta,
    detalle_venta,
    deuda,
    pago
)

# crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# incluir routers protegidos con API KEY
app.include_router(usuario.router, dependencies=[Depends(verificar_api_key)])
app.include_router(producto.router, dependencies=[Depends(verificar_api_key)])
app.include_router(venta.router, dependencies=[Depends(verificar_api_key)])
app.include_router(detalle_venta.router, dependencies=[Depends(verificar_api_key)])
app.include_router(deuda.router, dependencies=[Depends(verificar_api_key)])
app.include_router(pago.router, dependencies=[Depends(verificar_api_key)])