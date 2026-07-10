from datetime import datetime
from app.database.data import (
    productos,
    envios,
    guardar_datos,
    ARCHIVO_PRODUCTOS,
    ARCHIVO_ENVIOS
)

def obtener_nuevo_id_envio():
    if not envios:
        return 1

    ids = [envio.get("id_envio", 0) for envio in envios]
    return max(ids) + 1

def obtener_historial():
    return envios

def obtener_envio_por_id(id_envio: int):
    for envio in envios:
        if envio.get("id_envio") == id_envio:
            return envio
    return None

def registrar_envio(envio):

    nuevo_envio = {
        "id_envio": obtener_nuevo_id_envio(),
        "productos": [
            {
                "producto_id": producto.producto_id,
                "cantidad": producto.cantidad
            }
            for producto in envio.productos
        ],
        "destinatario": envio.destinatario,
        "direccion": envio.direccion,
        "observacion": envio.observacion,
        "estado": "Preparando",
        "fecha_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ruta": envio.ruta,
        "vehiculo": envio.vehiculo,
        "fecha_programada": envio.fecha_programada,
        "venta_id": envio.venta_id
    }

    envios.append(nuevo_envio)

    guardar_datos(ARCHIVO_ENVIOS, envios)

    return {
        "ok": True,
        "data": {
            "mensaje": "Envío registrado correctamente",
            "envio": nuevo_envio
        }
    }

    envios.append(nuevo_envio)
    guardar_datos(ARCHIVO_ENVIOS, envios)

    return {
        "ok": True,
        "data": {
            "mensaje": "Envío registrado correctamente",
            "envio": nuevo_envio,
        }
    }

def actualizar_estado_envio(id_envio: int, datos_estado):
    envio = obtener_envio_por_id(id_envio)

    if not envio:
        return None

    envio["estado"] = datos_estado.estado
    guardar_datos(ARCHIVO_ENVIOS, envios)
    return envio

def actualizar_envio(id_envio: int, datos_envio):

    envio = obtener_envio_por_id(id_envio)

    if not envio:
        return {
            "ok": False,
            "error": "Envío no encontrado"
        }

    envio["venta_id"] = datos_envio.venta_id
    envio["productos"] = [
        {
            "producto_id": producto.producto_id,
            "cantidad": producto.cantidad
        }
        for producto in datos_envio.productos
    ]
    envio["destinatario"] = datos_envio.destinatario
    envio["direccion"] = datos_envio.direccion
    envio["observacion"] = datos_envio.observacion
    envio["ruta"] = datos_envio.ruta
    envio["vehiculo"] = datos_envio.vehiculo
    envio["fecha_programada"] = datos_envio.fecha_programada

    guardar_datos(ARCHIVO_ENVIOS, envios)

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

    envios.remove(envio)

    guardar_datos(ARCHIVO_ENVIOS, envios)

    return envio

def obtener_envio_por_venta(venta_id: int):
    for envio in envios:
        if envio["venta_id"] == venta_id:
            return envio

    return None