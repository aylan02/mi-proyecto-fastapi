from fastapi import APIRouter, HTTPException
from app.schemas.envio import Envio
from app.services.envio_service import registrar_envio, obtener_historial

router = APIRouter(tags=["Envíos"])

@router.post("/envios")
def crear_envio(envio: Envio):
    resultado = registrar_envio(envio)

    if resultado["ok"] is False:
        if resultado["error"] == "Producto no encontrado":
            raise HTTPException(status_code=404, detail=resultado["error"])
        raise HTTPException(status_code=400, detail=resultado["error"])

    return resultado["data"]

@router.get("/historial")
def ver_historial():
    return obtener_historial()