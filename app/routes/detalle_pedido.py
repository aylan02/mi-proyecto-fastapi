from fastapi import APIRouter, HTTPException

from app.services.detalle_pedido_service import (
    obtener_detalle_pedido
)

from app.schemas.detalle_pedido import DetallePedido

router = APIRouter(
    prefix="/detalle-pedido",
    tags=["Detalle Pedido"]
)


@router.get(
    "/{venta_id}",
    response_model=DetallePedido
)
def get_detalle_pedido(venta_id: int):

    detalle = obtener_detalle_pedido(venta_id)

    if not detalle:

        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    return detalle