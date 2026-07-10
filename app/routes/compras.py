from fastapi import APIRouter, HTTPException, status

from app.services.compra_service import confirmar_compra
from app.schemas.compra import CompraConfirmar
from fastapi import Request

from app.services.venta_service import obtener_ventas_cliente

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
            destinatario=datos.destinatario,
            direccion=datos.direccion,
            metodo_pago=datos.metodo_pago,
            observacion=datos.observacion
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.get("")
def obtener_historial(request: Request):

    cliente_id = request.session.get("cliente_id")

    if not cliente_id:

        raise HTTPException(
            status_code=401,
            detail="Debe iniciar sesión."
        )

    return obtener_ventas_cliente(cliente_id)