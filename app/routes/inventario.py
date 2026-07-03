from fastapi import APIRouter, HTTPException, status

from app.schemas.inventario import (
    MovimientoInventarioCrear
)

from app.services.inventario_service import (
    obtener_movimientos,
    obtener_movimiento_por_id,
    registrar_movimiento,
    obtener_movimientos_producto,
    obtener_movimientos_tipo,
    eliminar_movimiento
)

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
)


@router.get(
    "",
    summary="Consultar movimientos de inventario"
)
def listar_movimientos():

    return obtener_movimientos()


@router.get(
    "/{movimiento_id}",
    summary="Consultar movimiento por ID"
)
def obtener_movimiento(movimiento_id: int):

    movimiento = obtener_movimiento_por_id(
        movimiento_id
    )

    if not movimiento:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado."
        )

    return movimiento


@router.get(
    "/producto/{producto_id}",
    summary="Consultar movimientos de un producto"
)
def movimientos_producto(producto_id: int):

    return obtener_movimientos_producto(
        producto_id
    )


@router.get(
    "/tipo/{tipo}",
    summary="Consultar movimientos por tipo"
)
def movimientos_tipo(tipo: str):

    return obtener_movimientos_tipo(tipo)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar movimiento de inventario"
)
def registrar(datos: MovimientoInventarioCrear):

    movimiento, error = registrar_movimiento(datos)

    if error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return {
        "mensaje": "Movimiento registrado correctamente.",
        "movimiento": movimiento
    }


@router.delete(
    "/{movimiento_id}",
    summary="Eliminar movimiento"
)
def eliminar(movimiento_id: int):

    movimiento = eliminar_movimiento(
        movimiento_id
    )

    if not movimiento:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado."
        )

    return {
        "mensaje": "Movimiento eliminado correctamente.",
        "movimiento": movimiento
    }