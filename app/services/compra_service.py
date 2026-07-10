from app.services.carrito_service import (
    obtener_carrito,
    vaciar_carrito
)

from app.services.venta_service import crear_venta
from app.services.pedido_service import crear_pedido


def confirmar_compra(
    cliente_id: int,
    metodo_pago: str,
    observacion: str = ""
):

    carrito = obtener_carrito(cliente_id)

    if not carrito:
        raise ValueError("Cliente no encontrado")

    if not carrito["items"]:
        raise ValueError("El carrito está vacío")

    detalles = []

    for item in carrito["items"]:
        detalles.append(
            {
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"]
            }
        )

    datos_venta = {
        "cliente_id": cliente_id,
        "detalles": detalles,
        "metodo_pago": metodo_pago,
        "observacion": observacion
    }

    venta = crear_venta(datos_venta)

    pedido = crear_pedido(
        cliente_id=cliente_id,
        venta_id=venta["id"],
        direccion=""
    )

    vaciar_carrito(cliente_id)

    return {
        "mensaje": "Compra realizada correctamente",
        "venta": venta,
        "pedido": pedido
    }