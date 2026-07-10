from fastapi import APIRouter

from app.services.historial_service import listar_historial

from app.schemas.historial import HistorialCompra

router = APIRouter(
    prefix="/historial",
    tags=["Historial"]
)


@router.get(
    "/{cliente_id}",
    response_model=list[HistorialCompra]
)
def get_historial(cliente_id: int):

    return listar_historial(cliente_id)