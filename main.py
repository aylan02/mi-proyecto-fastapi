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
from app.routes.usuarios import router as usuarios_router
from app.routes.roles import router as roles_router
from app.routes.reportes import router as reportes_router
from app.routes.pedidos import router as pedidos_router
from app.routes.carritos import router as carrito_router
from app.routes.historial import router as historial_router
from app.routes.detalle_pedido import router as detalle_pedido_router
from app.routes import rutas
from app.routes import compras

app = FastAPI(
    title="API de Envíos de Cosméticos",
    description="API para gestionar productos, stock y envíos",
    version="1.0.0"
)

app.add_middleware(SessionMiddleware, secret_key="cosmelogix_secreto_2026")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(health_router)
app.include_router(productos_router)
app.include_router(envios_router)
app.include_router(web_router)
app.include_router(clientes_router)
app.include_router(ventas_router)
app.include_router(auth_router)
app.include_router(inventario_router)
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(reportes_router)
app.include_router(pedidos_router)
app.include_router(carrito_router)
app.include_router(historial_router)
app.include_router(detalle_pedido_router)
app.include_router(rutas.router)
app.include_router(compras.router)
