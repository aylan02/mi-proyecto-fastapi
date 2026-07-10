from fastapi import APIRouter, HTTPException, status

from app.services.pedido_service import consultar_estado_pedido

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.get("/{pedido_id}")
def get_pedido(pedido_id: int):

    pedido = consultar_estado_pedido(pedido_id)

    if not pedido:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )

    return pedido