from fastapi import APIRouter, HTTPException
from app.schemas.producto import ProductoCrear
from app.services.producto_service import (
    obtener_productos,
    obtener_producto_por_id,
    crear_producto,
    obtener_productos_stock_bajo
)

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("")
def listar_productos():
    return obtener_productos()

@router.get("/stock/bajo")
def stock_bajo():
    return obtener_productos_stock_bajo()

@router.get("/{id}")
def buscar_producto(id: int):
    producto = obtener_producto_por_id(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("")
def agregar_producto(producto: ProductoCrear):
    nuevo_producto = crear_producto(producto)
    return {
        "mensaje": "Producto agregado correctamente",
        "producto": nuevo_producto
    }