from fastapi import APIRouter, HTTPException, status

from app.schemas.venta import Venta, VentaCrear
from app.services.venta_service import (
    listar_ventas,
    obtener_venta,
    crear_venta,
    anular_venta
)

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.get("", response_model=list[Venta])
def get_ventas():
    return listar_ventas()


@router.get("/{venta_id}", response_model=Venta)
def get_venta(venta_id: int):
    venta = obtener_venta(venta_id)

    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )

    return venta


@router.post("", response_model=Venta, status_code=status.HTTP_201_CREATED)
def post_venta(venta: VentaCrear):
    try:
        return crear_venta(venta.model_dump())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{venta_id}")
def delete_venta(venta_id: int):
    try:
        venta = anular_venta(venta_id)

        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        return {"mensaje": "Venta anulada correctamente", "venta": venta}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )