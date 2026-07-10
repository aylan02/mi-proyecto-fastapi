from app.services.venta_service import obtener_venta
from app.services.envio_service import obtener_envio_por_venta


def obtener_seguimiento(venta_id: int):

    venta = obtener_venta(venta_id)

    if not venta:
        raise ValueError("Pedido no encontrado")

    envio = obtener_envio_por_venta(venta_id)

    if not envio:
        raise ValueError("Envío no encontrado")

    estado_envio = envio["estado"]

    if estado_envio == "Preparando":

        estado_actual = "Preparando"

        estados = [

            {
                "nombre": "Pedido Registrado",
                "descripcion": "Tu compra fue registrada correctamente.",
                "completado": True
            },

            {
                "nombre": "Preparando",
                "descripcion": "Nuestro equipo está preparando tu pedido.",
                "completado": True
            },

            {
                "nombre": "En Ruta",
                "descripcion": "El pedido aún no ha salido a reparto.",
                "completado": False
            },

            {
                "nombre": "Entregado",
                "descripcion": "El pedido aún no ha sido entregado.",
                "completado": False
            }

        ]

    elif estado_envio == "En Ruta":

        estado_actual = "En Ruta"

        estados = [

            {
                "nombre": "Pedido Registrado",
                "descripcion": "Tu compra fue registrada correctamente.",
                "completado": True
            },

            {
                "nombre": "Preparando",
                "descripcion": "El pedido fue preparado correctamente.",
                "completado": True
            },

            {
                "nombre": "En Ruta",
                "descripcion": "Tu pedido va camino a su destino.",
                "completado": True
            },

            {
                "nombre": "Entregado",
                "descripcion": "El pedido aún no ha sido entregado.",
                "completado": False
            }

        ]

    elif estado_envio == "Entregado":

        estado_actual = "Entregado"

        estados = [

            {
                "nombre": "Pedido Registrado",
                "descripcion": "Tu compra fue registrada correctamente.",
                "completado": True
            },

            {
                "nombre": "Preparando",
                "descripcion": "El pedido fue preparado correctamente.",
                "completado": True
            },

            {
                "nombre": "En Ruta",
                "descripcion": "El pedido fue enviado.",
                "completado": True
            },

            {
                "nombre": "Entregado",
                "descripcion": "El pedido fue entregado correctamente.",
                "completado": True
            }

        ]

    elif estado_envio == "Anulado":

        estado_actual = "Anulado"

        estados = [

            {
                "nombre": "Pedido Registrado",
                "descripcion": "La compra fue registrada.",
                "completado": True
            },

            {
                "nombre": "Pedido Anulado",
                "descripcion": "El pedido fue cancelado.",
                "completado": True
            }

        ]

    else:

        estado_actual = estado_envio

        estados = [

            {
                "nombre": estado_envio,
                "descripcion": "Estado actualizado.",
                "completado": True
            }

        ]

    return {

        "pedido_id": venta["id"],
        "cliente": venta["cliente_nombre"],
        "metodo": venta["metodo_pago"],
        "fecha": venta["fecha"],
        "estado_actual": estado_actual,
        "estados": estados

    }