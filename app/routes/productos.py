from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.producto import ProductoCrear, ProductoActualizar
from app.services.producto_service import (
    obtener_productos,
    obtener_producto_por_id,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    obtener_productos_stock_bajo
)

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get(
    "",
    summary="Obtener productos con filtros y paginación",
    description="Lista los productos registrados. Permite filtrar por nombre, categoría, marca, disponibilidad de stock, ordenar por precio y paginar resultados."
)
def listar_productos(
    nombre: str = Query(default=None, description="Buscar por nombre del producto"),
    categoria: str = Query(default=None, description="Filtrar por categoría"),
    marca: str = Query(default=None, description="Filtrar por marca"),
    stock_disponible: bool = Query(default=False, description="Mostrar solo productos con stock"),
    ordenar_precio: str = Query(default=None, description="Ordenar precio: asc o desc"),
    limit: int = Query(default=10, ge=1, le=100, description="Cantidad máxima de productos a mostrar"),
    offset: int = Query(default=0, ge=0, description="Desde qué posición comenzar")
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
    summary="Obtener productos con stock bajo",
    description="Muestra los productos cuyo stock es menor o igual a 5 unidades."
)
def stock_bajo():
    return obtener_productos_stock_bajo()

@router.get(
    "/{id}",
    summary="Obtener un producto por ID",
    description="Busca un producto específico usando su identificador."
)
def buscar_producto(id: int):
    producto = obtener_producto_por_id(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post(
    "",
    summary="Agregar un nuevo producto",
    description="Registra un nuevo producto cosmético en el sistema.",
    status_code=status.HTTP_201_CREATED,
    response_description="Producto creado correctamente"
)
def agregar_producto(producto: ProductoCrear):
    nuevo_producto = crear_producto(producto)
    return {
        "mensaje": "Producto agregado correctamente",
        "producto": nuevo_producto
    }

@router.put(
    "/{id}",
    summary="Actualizar un producto",
    description="Actualiza la información de un producto existente."
)
def editar_producto(id: int, producto: ProductoActualizar):
    producto_actualizado = actualizar_producto(id, producto)

    if not producto_actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "mensaje": "Producto actualizado correctamente",
        "producto": producto_actualizado
    }

@router.delete(
    "/{id}",
    summary="Eliminar un producto",
    description="Elimina un producto del sistema según su identificador."
)
def borrar_producto(id: int):
    producto_eliminado = eliminar_producto(id)

    if not producto_eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "mensaje": "Producto eliminado correctamente",
        "producto": producto_eliminado
    }