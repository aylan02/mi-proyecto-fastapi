from datetime import datetime
from app.database.data import (
    productos,
    historial_envios,
    guardar_datos,
    ARCHIVO_PRODUCTOS,
    ARCHIVO_HISTORIAL
)

def buscar_producto_por_id(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None

def obtener_nuevo_id_envio():
    if not historial_envios:
        return 1

    ids = [envio.get("id_envio", 0) for envio in historial_envios]
    return max(ids) + 1

def obtener_historial():
    return historial_envios

def obtener_envio_por_id(id_envio: int):
    for envio in historial_envios:
        if envio.get("id_envio") == id_envio:
            return envio
    return None

def registrar_envio(envio):
    producto = buscar_producto_por_id(envio.producto_id)

    if not producto:
        return {"ok": False, "error": "Producto no encontrado"}

    if producto["stock"] < envio.cantidad:
        return {"ok": False, "error": "Stock insuficiente para realizar el envío"}

    producto["stock"] -= envio.cantidad
    guardar_datos(ARCHIVO_PRODUCTOS, productos)

    nuevo_envio = {
        "id_envio": obtener_nuevo_id_envio(),
        "producto_id": envio.producto_id,
        "nombre_producto": producto["nombre"],
        "cantidad": envio.cantidad,
        "destinatario": envio.destinatario,
        "direccion": envio.direccion,
        "observacion": envio.observacion,
        "estado": "registrado",
        "fecha_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    historial_envios.append(nuevo_envio)
    guardar_datos(ARCHIVO_HISTORIAL, historial_envios)

    return {
        "ok": True,
        "data": {
            "mensaje": "Envío registrado correctamente",
            "envio": nuevo_envio,
            "stock_restante": producto["stock"]
        }
    }

def actualizar_estado_envio(id_envio: int, datos_estado):
    envio = obtener_envio_por_id(id_envio)

    if not envio:
        return None

    envio["estado"] = datos_estado.estado
    guardar_datos(ARCHIVO_HISTORIAL, historial_envios)
    return envio

def actualizar_envio(id_envio: int, datos_envio):
    envio = obtener_envio_por_id(id_envio)

    if not envio:
        return {"ok": False, "error": "Envío no encontrado"}

    producto_anterior = buscar_producto_por_id(envio["producto_id"])
    if producto_anterior:
        producto_anterior["stock"] += envio["cantidad"]

    nuevo_producto = buscar_producto_por_id(datos_envio.producto_id)

    if not nuevo_producto:
        if producto_anterior:
            producto_anterior["stock"] -= envio["cantidad"]
        return {"ok": False, "error": "Producto no encontrado"}

    if nuevo_producto["stock"] < datos_envio.cantidad:
        if producto_anterior:
            producto_anterior["stock"] -= envio["cantidad"]
        return {"ok": False, "error": "Stock insuficiente para actualizar el envío"}

    nuevo_producto["stock"] -= datos_envio.cantidad

    envio["producto_id"] = datos_envio.producto_id
    envio["nombre_producto"] = nuevo_producto["nombre"]
    envio["cantidad"] = datos_envio.cantidad
    envio["destinatario"] = datos_envio.destinatario
    envio["direccion"] = datos_envio.direccion
    envio["observacion"] = datos_envio.observacion

    guardar_datos(ARCHIVO_PRODUCTOS, productos)
    guardar_datos(ARCHIVO_HISTORIAL, historial_envios)

    return {
        "ok": True,
        "data": {
            "mensaje": "Envío actualizado correctamente",
            "envio": envio
        }
    }

def eliminar_envio(id_envio: int):
    envio = obtener_envio_por_id(id_envio)

    if not envio:
        return None

    producto = buscar_producto_por_id(envio["producto_id"])
    if producto:
        producto["stock"] += envio["cantidad"]

    historial_envios.remove(envio)

    guardar_datos(ARCHIVO_PRODUCTOS, productos)
    guardar_datos(ARCHIVO_HISTORIAL, historial_envios)

    return envio