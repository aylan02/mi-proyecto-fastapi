from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.health import router as health_router
from app.routes.productos import router as productos_router
from app.routes.envios import router as envios_router
from app.routes.web import router as web_router
from app.routes.clientes import router as clientes_router
from app.routes.ventas import router as ventas_router
from app.routes.inventario import router as inventario_router
from starlette.middleware.sessions import SessionMiddleware
from app.routes.auth import router as auth_router

app = FastAPI(
    title="API de Envíos de Cosméticos",
    description="API para gestionar productos, stock y envíos",
    version="1.0.0"
)

app.add_middleware(SessionMiddleware, secret_key="cosmelogix_secreto_2026")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de Envíos de Cosméticos"}

app.include_router(health_router)
app.include_router(productos_router)
app.include_router(envios_router)
app.include_router(web_router)
app.include_router(clientes_router)
app.include_router(ventas_router)
app.include_router(auth_router)
app.include_router(inventario_router)