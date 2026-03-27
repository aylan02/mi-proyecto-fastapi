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

def registrar_envio(envio):
    producto = buscar_producto_por_id(envio.producto_id)

    if not producto:
        return {"ok": False, "error": "Producto no encontrado"}

    if producto["stock"] < envio.cantidad:
        return {"ok": False, "error": "Stock insuficiente para realizar el envío"}

    producto["stock"] -= envio.cantidad
    guardar_datos(ARCHIVO_PRODUCTOS, productos)

    nuevo_envio = {
        "producto_id": envio.producto_id,
        "nombre_producto": producto["nombre"],
        "cantidad": envio.cantidad,
        "destinatario": envio.destinatario,
        "direccion": envio.direccion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

def obtener_historial():
    return historial_envios