from app.services.envio_service import registrar_envio
from app.schemas.envio import Envio, ProductoEnvio
from app.services.carrito_service import (
    obtener_carrito,
    vaciar_carrito
)

from app.services.venta_service import crear_venta
from app.services.pedido_service import crear_pedido


def confirmar_compra(
    cliente_id: int,
    destinatario: str,
    direccion: str,
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
        direccion=direccion
    )

    productos_envio = []

    for item in venta["detalles"]:

        productos_envio.append(

            ProductoEnvio(
                producto_id=item["producto_id"],
                cantidad=item["cantidad"]
            )

        )

    envio = Envio(

        productos=productos_envio,

        destinatario=destinatario,

        direccion=direccion,

        observacion=observacion,

        ruta="",

        vehiculo="",

        fecha_programada=None,

        venta_id=venta["id"]

    )

    registrar_envio(envio)

    vaciar_carrito(cliente_id)

    return {
        "mensaje": "Compra realizada correctamente",
        "venta": venta,
        "pedido": pedido
    }