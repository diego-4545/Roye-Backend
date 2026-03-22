from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.security import verificar_api_key
from app.models.producto import Producto
from app.models.venta import Venta
from app.models.cliente import Cliente

from app.routers import (
    usuario,
    producto,
    venta,
    detalle_venta,
    deuda,
    pago,
    categoria,
    cliente,
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
app.include_router(categoria.router, dependencies=[Depends(verificar_api_key)])
app.include_router(cliente.router, dependencies=[Depends(verificar_api_key)])

@app.get("/stats", tags=["Stats"])
def obtener_stats(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    total_productos = len(productos)
    valor_inventario = sum([
        float(p.precio_venta or 0) * (p.stock or 0)
        for p in productos
    ])
    total_ventas = db.query(Venta).count()
    total_clientes = db.query(Cliente).count()
    return {
        "total_productos": total_productos,
        "valor_inventario": round(valor_inventario, 2),
        "total_ventas": total_ventas,
        "total_clientes": total_clientes
    }

@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
def root():
    return {"mensaje": "API activa"}

@app.get("/health", include_in_schema=False)
@app.head("/health", include_in_schema=False)
def health():
    return {"status": "ok"}