from app.database.data import productos, guardar_datos, ARCHIVO_PRODUCTOS

def obtener_productos():
    return productos

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

def obtener_productos_stock_bajo():
    return [producto for producto in productos if producto["stock"] <= 5]