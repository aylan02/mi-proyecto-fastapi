from fastapi import APIRouter, HTTPException

from app.schemas.carrito import (
    AgregarProductoCarrito,
    ActualizarCantidadCarrito,
    CarritoResponse
)

from app.services.carrito_service import (
    agregar_producto,
    obtener_carrito,
    actualizar_cantidad,
    eliminar_producto,
    vaciar_carrito
)

router = APIRouter(
    prefix="/carrito",
    tags=["Carrito"]
)


@router.post(
    "/",
    status_code=201
)
def agregar_al_carrito(datos: AgregarProductoCarrito):

    resultado = agregar_producto(datos)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente o producto no encontrado."
        )

    if resultado is False:
        raise HTTPException(
            status_code=400,
            detail="Stock insuficiente."
        )

    return {
        "mensaje": "Producto agregado al carrito correctamente.",
        "carrito": obtener_carrito(datos.cliente_id)
    }

@router.get(
    "/{cliente_id}",
    response_model=CarritoResponse
)
def ver_carrito(cliente_id: int):

    carrito = obtener_carrito(cliente_id)

    if carrito is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    return carrito

@router.put("/{cliente_id}/{producto_id}")
def modificar_cantidad(
    cliente_id: int,
    producto_id: int,
    datos: ActualizarCantidadCarrito
):

    resultado = actualizar_cantidad(
        cliente_id,
        producto_id,
        datos
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente o producto no encontrado."
        )

    if resultado is False:
        raise HTTPException(
            status_code=400,
            detail="Stock insuficiente."
        )

    return {
        "mensaje": "Cantidad actualizada correctamente.",
        "carrito": obtener_carrito(cliente_id)
    }

@router.delete("/{cliente_id}/{producto_id}")
def eliminar_del_carrito(
    cliente_id: int,
    producto_id: int
):

    resultado = eliminar_producto(
        cliente_id,
        producto_id
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado en el carrito."
        )

    return {
        "mensaje": "Producto eliminado del carrito.",
        "carrito": obtener_carrito(cliente_id)
    }

@router.delete("/{cliente_id}")
def limpiar_carrito(cliente_id: int):

    resultado = vaciar_carrito(cliente_id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Carrito no encontrado."
        )

    return {
        "mensaje": "Carrito vaciado correctamente.",
        "carrito": obtener_carrito(cliente_id)
    }