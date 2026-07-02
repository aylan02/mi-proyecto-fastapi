from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.producto import (
    ProductoCrear,
    ProductoActualizar
)

from app.services.producto_service import (
    obtener_productos,
    obtener_producto_por_id,
    crear_producto,
    actualizar_producto,
    desactivar_producto,
    obtener_productos_stock_bajo
)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get(
    "",
    summary="Consultar productos"
)
def listar_productos(
    nombre: str = Query(None),
    categoria: str = Query(None),
    marca: str = Query(None),
    stock_disponible: bool = False,
    ordenar_precio: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):

    return obtener_productos(
        nombre=nombre,
        categoria=categoria,
        marca=marca,
        stock_disponible=stock_disponible,
        ordenar_precio=ordenar_precio,
        limit=limit,
        offset=offset
    )


@router.get(
    "/stock/bajo",
    summary="Consultar productos con stock bajo"
)
def listar_stock_bajo():

    return obtener_productos_stock_bajo()


@router.get(
    "/{producto_id}",
    summary="Consultar producto por ID"
)
def obtener_producto(producto_id: int):

    producto = obtener_producto_por_id(producto_id)

    if not producto:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    return producto


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar producto"
)
def registrar_producto(producto: ProductoCrear):

    nuevo = crear_producto(producto)

    if nuevo is None:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con ese código."
        )

    return {
        "mensaje": "Producto registrado correctamente.",
        "producto": nuevo
    }


@router.put(
    "/{producto_id}",
    summary="Actualizar producto"
)
def editar_producto(
    producto_id: int,
    producto: ProductoActualizar
):

    actualizado = actualizar_producto(
        producto_id,
        producto
    )

    if actualizado is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado o código duplicado."
        )

    return {
        "mensaje": "Producto actualizado correctamente.",
        "producto": actualizado
    }


@router.patch(
    "/{producto_id}/desactivar",
    summary="Desactivar producto"
)
def desactivar(producto_id: int):

    producto = desactivar_producto(producto_id)

    if producto is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    return {
        "mensaje": "Producto desactivado correctamente.",
        "producto": producto
    }