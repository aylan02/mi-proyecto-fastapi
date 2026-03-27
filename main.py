from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.productos import router as productos_router
from app.routes.envios import router as envios_router

app = FastAPI(
    title="API de Envíos de Cosméticos",
    description="API para gestionar productos, stock y envíos",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de Envíos de Cosméticos"}

app.include_router(health_router)
app.include_router(productos_router)
app.include_router(envios_router)