from fastapi import APIRouter, HTTPException, status

from app.services.compra_service import confirmar_compra
from app.schemas.compra import CompraConfirmar

router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)


@router.post(
    "/confirmar",
    status_code=status.HTTP_201_CREATED
)
def post_confirmar_compra(datos: CompraConfirmar):

    try:

        return confirmar_compra(
            cliente_id=datos.cliente_id,
            metodo_pago=datos.metodo_pago,
            observacion=datos.observacion
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )