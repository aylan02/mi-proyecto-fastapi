from fastapi import APIRouter, HTTPException, status

from app.schemas.ruta import Ruta, RutaCrear, RutaActualizar
from app.services.ruta_service import (
    listar_rutas,
    obtener_ruta,
    crear_ruta,
    actualizar_ruta,
    desactivar_ruta
)

router = APIRouter(prefix="/rutas", tags=["Rutas"])


@router.get("", response_model=list[Ruta])
def get_rutas():
    return listar_rutas()


@router.get("/{ruta_id}", response_model=Ruta)
def get_ruta(ruta_id: int):
    ruta = obtener_ruta(ruta_id)

    if not ruta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )

    return ruta


@router.post("", response_model=Ruta, status_code=status.HTTP_201_CREATED)
def post_ruta(ruta: RutaCrear):
    return crear_ruta(ruta.model_dump())


@router.put("/{ruta_id}", response_model=Ruta)
def put_ruta(ruta_id: int, ruta: RutaActualizar):
    ruta_actual = obtener_ruta(ruta_id)

    if not ruta_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )

    return actualizar_ruta(
        ruta_id,
        ruta.model_dump(exclude_unset=True)
    )


@router.delete("/{ruta_id}")
def delete_ruta(ruta_id: int):
    ruta = desactivar_ruta(ruta_id)

    if ruta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )

    if ruta == "INACTIVA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La ruta ya se encuentra inactiva"
        )

    return {"mensaje": "Ruta desactivada correctamente"}