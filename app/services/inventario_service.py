from datetime import datetime

from app.database.data import (
    productos,
    guardar_datos,
    ARCHIVO_PRODUCTOS,
    movimientos_inventario
)

ARCHIVO_MOVIMIENTOS = "movimientos_inventario.json"
movimientos = movimientos_inventario

def guardar_movimientos():
    guardar_datos(
        ARCHIVO_MOVIMIENTOS,
        movimientos
    )


def guardar_productos():
    guardar_datos(
        ARCHIVO_PRODUCTOS,
        productos
    )


def obtener_nuevo_id():

    if not movimientos:
        return 1

    return max(
        movimiento["id"]
        for movimiento in movimientos
    ) + 1


def buscar_producto(producto_id):

    for producto in productos:

        if (
            producto["id"] == producto_id
            and producto.get("estado", "Activo") == "Activo"
        ):
            return producto

    return None


def obtener_movimientos():

    return movimientos


def obtener_movimiento_por_id(movimiento_id):

    for movimiento in movimientos:

        if movimiento["id"] == movimiento_id:
            return movimiento

    return None

def registrar_movimiento(datos, actualizar_stock=True):

    producto = buscar_producto(datos.producto_id)

    if not producto:
        return None, "Producto no encontrado."

    if actualizar_stock:

        if datos.tipo.value == "Salida":

            if producto["stock"] < datos.cantidad:
                return None, "Stock insuficiente."

            producto["stock"] -= datos.cantidad

        elif datos.tipo.value == "Ingreso":

            producto["stock"] += datos.cantidad

        elif datos.tipo.value == "Ajuste":

            producto["stock"] = datos.cantidad

    movimiento = {
        "id": obtener_nuevo_id(),
        "producto_id": datos.producto_id,
        "tipo": datos.tipo.value,
        "cantidad": datos.cantidad,
        "motivo": datos.motivo,
        "usuario": datos.usuario,
        "fecha": datetime.now().isoformat()
    }

    movimientos.append(movimiento)

    guardar_productos()
    guardar_movimientos()

    return movimiento, None

def obtener_movimientos_producto(producto_id):

    return [
        movimiento
        for movimiento in movimientos
        if movimiento["producto_id"] == producto_id
    ]


def obtener_movimientos_tipo(tipo):

    return [
        movimiento
        for movimiento in movimientos
        if movimiento["tipo"].lower() == tipo.lower()
    ]


def eliminar_movimiento(movimiento_id):

    movimiento = obtener_movimiento_por_id(movimiento_id)

    if not movimiento:
        return None

    movimientos.remove(movimiento)

    guardar_movimientos()

    return movimiento