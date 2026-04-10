from fastapi import APIRouter, HTTPException, status
from app.schemas.envio import Envio, EnvioActualizar, EstadoEnvioActualizar
from app.services.envio_service import (
    registrar_envio,
    obtener_historial,
    obtener_envio_por_id,
    actualizar_estado_envio,
    actualizar_envio,
    eliminar_envio
)

router = APIRouter(tags=["Envíos"])

@router.post(
    "/envios",
    summary="Registrar un envío",
    description="Registra un nuevo envío y descuenta automáticamente el stock del producto.",
    status_code=status.HTTP_201_CREATED,
    response_description="Envío registrado correctamente"
)
def crear_envio(envio: Envio):
    resultado = registrar_envio(envio)

    if resultado["ok"] is False:
        if resultado["error"] == "Producto no encontrado":
            raise HTTPException(status_code=404, detail=resultado["error"])
        raise HTTPException(status_code=400, detail=resultado["error"])

    return resultado["data"]

@router.get(
    "/envios",
    summary="Obtener todos los envíos",
    description="Lista todos los envíos registrados en el sistema."
)
def listar_envios():
    return obtener_historial()

@router.get(
    "/envios/{id_envio}",
    summary="Obtener un envío por ID",
    description="Busca un envío específico según su identificador."
)
def buscar_envio(id_envio: int):
    envio = obtener_envio_por_id(id_envio)

    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")

    return envio

@router.put(
    "/envios/{id_envio}",
    summary="Actualizar un envío",
    description="Permite modificar los datos de un envío ya registrado."
)
def editar_envio(id_envio: int, envio: EnvioActualizar):
    resultado = actualizar_envio(id_envio, envio)

    if resultado["ok"] is False:
        if resultado["error"] == "Envío no encontrado":
            raise HTTPException(status_code=404, detail=resultado["error"])
        if resultado["error"] == "Producto no encontrado":
            raise HTTPException(status_code=404, detail=resultado["error"])
        raise HTTPException(status_code=400, detail=resultado["error"])

    return resultado["data"]

@router.patch(
    "/envios/{id_envio}/estado",
    summary="Actualizar estado de un envío",
    description="Permite cambiar el estado de un envío, por ejemplo a registrado, en camino o entregado."
)
def cambiar_estado_envio(id_envio: int, estado: EstadoEnvioActualizar):
    envio_actualizado = actualizar_estado_envio(id_envio, estado)

    if not envio_actualizado:
        raise HTTPException(status_code=404, detail="Envío no encontrado")

    return {
        "mensaje": "Estado del envío actualizado correctamente",
        "envio": envio_actualizado
    }

@router.delete(
    "/envios/{id_envio}",
    summary="Eliminar un envío",
    description="Elimina un envío y devuelve el stock descontado al producto correspondiente."
)
def borrar_envio(id_envio: int):
    envio_eliminado = eliminar_envio(id_envio)

    if not envio_eliminado:
        raise HTTPException(status_code=404, detail="Envío no encontrado")

    return {
        "mensaje": "Envío eliminado correctamente",
        "envio": envio_eliminado
    }

@router.get(
    "/historial",
    summary="Obtener historial de envíos",
    description="Muestra el historial completo de envíos registrados."
)
def ver_historial():
    return obtener_historial() 