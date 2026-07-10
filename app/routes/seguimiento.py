from fastapi import APIRouter

from app.schemas.seguimiento import SeguimientoResponse
from app.services.seguimiento_service import obtener_seguimiento

router = APIRouter(
    prefix="/seguimiento",
    tags=["Seguimiento"]
)


@router.get(
    "/{venta_id}",
    response_model=SeguimientoResponse
)
def get_seguimiento(venta_id: int):

    return obtener_seguimiento(venta_id)