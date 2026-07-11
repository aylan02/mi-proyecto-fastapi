from app.database.data import (
    productos,
    guardar_datos,
    ARCHIVO_PRODUCTOS
)


def guardar():
    guardar_datos(ARCHIVO_PRODUCTOS, productos)


def obtener_nuevo_id():
    if not productos:
        return 1
    return max(p["id"] for p in productos) + 1


def obtener_productos(
    nombre=None,
    categoria=None,
    marca=None,
    stock_disponible=False,
    ordenar_precio=None,
    limit=10,
    offset=0
):
    resultado = list(productos)

    if nombre:
        resultado = [
            p for p in resultado
            if nombre.lower() in p["nombre"].lower()
        ]

    if categoria:
        resultado = [
            p for p in resultado
            if p["categoria"].lower() == categoria.lower()
        ]

    if marca:
        resultado = [
            p for p in resultado
            if p["marca"].lower() == marca.lower()
        ]

    if stock_disponible:
        resultado = [
            p for p in resultado
            if p["stock"] > 0
        ]

    if ordenar_precio == "asc":
        resultado.sort(key=lambda x: x["precio"])

    elif ordenar_precio == "desc":
        resultado.sort(
            key=lambda x: x["precio"],
            reverse=True
        )

    total = len(resultado)

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "resultados": resultado[offset:offset + limit]
    }


def obtener_producto_por_id(producto_id):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None


def obtener_producto_por_codigo(codigo):
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
    return None


def crear_producto(datos):

    if obtener_producto_por_codigo(datos.codigo):
        return None

    nuevo = {
        "id": obtener_nuevo_id(),
        "codigo": datos.codigo,
        "nombre": datos.nombre,
        "marca": datos.marca,
        "categoria": datos.categoria,
        "precio": datos.precio,
        "stock": datos.stock,
        "descripcion": datos.descripcion,
        "imagen": datos.imagen,
        "destacado": datos.destacado,
        "nuevo": datos.nuevo,
        "oferta": datos.oferta,
        "estado": "Activo"
    }

    productos.append(nuevo)

    guardar()

    return nuevo


def actualizar_producto(producto_id, datos):

    producto = obtener_producto_por_id(producto_id)

    if not producto:
        return None

    cambios = datos.model_dump(exclude_unset=True)

    if "codigo" in cambios:

        existente = obtener_producto_por_codigo(
            cambios["codigo"]
        )

        if existente and existente["id"] != producto_id:
            return None

    producto.update(cambios)

    guardar()

    return producto


def cambiar_estado_producto(producto_id):

    producto = obtener_producto_por_id(producto_id)

    if not producto:
        return None

    if producto["estado"] == "Activo":
        producto["estado"] = "Inactivo"
    else:
        producto["estado"] = "Activo"

    guardar_datos(ARCHIVO_PRODUCTOS, productos)

    return producto


def obtener_productos_stock_bajo():

    return [
        p
        for p in productos
        if p["stock"] <= 5
        and p.get("estado", "Activo") == "Activo"
    ]

def obtener_productos_activos(
    nombre=None,
    categoria=None,
    marca=None
):

    resultado = [
        p for p in productos
        if p.get("estado", "Activo") == "Activo"
    ]

    if nombre:
        resultado = [
            p for p in resultado
            if nombre.lower() in p["nombre"].lower()
        ]

    if categoria:
        resultado = [
            p for p in resultado
            if p["categoria"].lower() == categoria.lower()
        ]

    if marca:
        resultado = [
            p for p in resultado
            if p["marca"].lower() == marca.lower()
        ]

    return {
        "total": len(resultado),
        "limit": len(resultado),
        "offset": 0,
        "resultados": resultado
    }