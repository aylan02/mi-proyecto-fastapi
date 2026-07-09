from app.database.data import (
    carrito,
    productos,
    guardar_datos,
    ARCHIVO_CARRITO
)

from app.services.cliente_service import obtener_cliente


def guardar():
    guardar_datos(ARCHIVO_CARRITO, carrito)


def obtener_carrito_cliente(cliente_id):
    for c in carrito:
        if c["cliente_id"] == cliente_id:
            return c
    return None


def obtener_producto(producto_id):
    for producto in productos:
        if (
            producto["id"] == producto_id
            and producto.get("estado", "Activo") == "Activo"
        ):
            return producto
    return None

def agregar_producto(datos):

    cliente = obtener_cliente(datos.cliente_id)

    if not cliente:
        return None

    producto = obtener_producto(datos.producto_id)

    if not producto:
        return None

    if producto["stock"] < datos.cantidad:
        return False

    carrito_cliente = obtener_carrito_cliente(
        datos.cliente_id
    )

    if not carrito_cliente:

        carrito_cliente = {
            "cliente_id": datos.cliente_id,
            "items": []
        }

        carrito.append(carrito_cliente)

    for item in carrito_cliente["items"]:

        if item["producto_id"] == datos.producto_id:

            nueva_cantidad = (
                item["cantidad"] + datos.cantidad
            )

            if nueva_cantidad > producto["stock"]:
                return False

            item["cantidad"] = nueva_cantidad

            guardar()

            return carrito_cliente

    carrito_cliente["items"].append(
        {
            "producto_id": datos.producto_id,
            "cantidad": datos.cantidad
        }
    )

    guardar()

    return carrito_cliente

def obtener_carrito(cliente_id):

    cliente = obtener_cliente(cliente_id)

    if not cliente:
        return None

    carrito_cliente = obtener_carrito_cliente(cliente_id)

    if not carrito_cliente:
        return {
            "cliente_id": cliente_id,
            "items": [],
            "total_productos": 0,
            "total": 0
        }

    items = []
    total = 0
    total_productos = 0

    for item in carrito_cliente["items"]:

        producto = obtener_producto(item["producto_id"])

        if not producto:
            carrito_cliente["items"].remove(item)
            guardar()
            continue

        subtotal = producto["precio"] * item["cantidad"]

        items.append(
            {
                "producto_id": producto["id"],
                "nombre": producto["nombre"],
                "marca": producto["marca"],
                "categoria": producto["categoria"],
                "imagen": producto["imagen"],
                "precio": producto["precio"],
                "cantidad": item["cantidad"],
                "subtotal": subtotal
            }
        )

        total += subtotal
        total_productos += item["cantidad"]

    return {
        "cliente_id": cliente_id,
        "items": items,
        "total_productos": total_productos,
        "total": total
    }

def actualizar_cantidad(cliente_id, producto_id, datos):

    cliente = obtener_cliente(cliente_id)

    if not cliente:
        return None

    carrito_cliente = obtener_carrito_cliente(cliente_id)

    if not carrito_cliente:
        return None

    producto = obtener_producto(producto_id)

    if not producto:
        return None

    for item in carrito_cliente["items"][:]:

        if item["producto_id"] == producto_id:

            if datos.cantidad > producto["stock"]:
                return False

            item["cantidad"] = datos.cantidad

            guardar()

            return carrito_cliente

    return None

def eliminar_producto(cliente_id, producto_id):

    carrito_cliente = obtener_carrito_cliente(cliente_id)

    if not carrito_cliente:
        return None

    for item in carrito_cliente["items"]:

        if item["producto_id"] == producto_id:

            carrito_cliente["items"].remove(item)

            if not carrito_cliente["items"]:
                carrito.remove(carrito_cliente)

            guardar()

            return True

    return None

def vaciar_carrito(cliente_id):

    carrito_cliente = obtener_carrito_cliente(cliente_id)

    if not carrito_cliente:
        return None

    carrito.remove(carrito_cliente)

    guardar()

    return True