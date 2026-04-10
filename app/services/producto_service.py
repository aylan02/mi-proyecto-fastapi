from app.database.data import productos, guardar_datos, ARCHIVO_PRODUCTOS

def obtener_productos(
    nombre: str = None,
    categoria: str = None,
    marca: str = None,
    stock_disponible: bool = False,
    ordenar_precio: str = None,
    limit: int = 10,
    offset: int = 0
):
    resultado = productos.copy()

    if nombre:
        resultado = [
            producto for producto in resultado
            if nombre.lower() in producto["nombre"].lower()
        ]

    if categoria:
        resultado = [
            producto for producto in resultado
            if producto["categoria"].lower() == categoria.lower()
        ]

    if marca:
        resultado = [
            producto for producto in resultado
            if producto["marca"].lower() == marca.lower()
        ]

    if stock_disponible:
        resultado = [
            producto for producto in resultado
            if producto["stock"] > 0
        ]

    if ordenar_precio == "asc":
        resultado.sort(key=lambda producto: producto["precio"])
    elif ordenar_precio == "desc":
        resultado.sort(key=lambda producto: producto["precio"], reverse=True)

    total = len(resultado)
    resultado_paginado = resultado[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "resultados": resultado_paginado
    }

def obtener_producto_por_id(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None

def obtener_nuevo_id():
    if not productos:
        return 1
    return max(producto["id"] for producto in productos) + 1

def crear_producto(producto):
    nuevo_producto = {
        "id": obtener_nuevo_id(),
        "nombre": producto.nombre,
        "marca": producto.marca,
        "categoria": producto.categoria,
        "precio": producto.precio,
        "stock": producto.stock,
        "descripcion": producto.descripcion
    }

    productos.append(nuevo_producto)
    guardar_datos(ARCHIVO_PRODUCTOS, productos)
    return nuevo_producto

def actualizar_producto(producto_id: int, datos_actualizados):
    producto = obtener_producto_por_id(producto_id)

    if not producto:
        return None

    producto["nombre"] = datos_actualizados.nombre
    producto["marca"] = datos_actualizados.marca
    producto["categoria"] = datos_actualizados.categoria
    producto["precio"] = datos_actualizados.precio
    producto["stock"] = datos_actualizados.stock
    producto["descripcion"] = datos_actualizados.descripcion

    guardar_datos(ARCHIVO_PRODUCTOS, productos)
    return producto

def eliminar_producto(producto_id: int):
    producto = obtener_producto_por_id(producto_id)

    if not producto:
        return None

    productos.remove(producto)
    guardar_datos(ARCHIVO_PRODUCTOS, productos)
    return producto

def obtener_productos_stock_bajo():
    return [producto for producto in productos if producto["stock"] <= 5]