import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_PEDIDOS = BASE_DIR / "pedidos.json"

def asegurar_archivo():
    if not ARCHIVO_PEDIDOS.exists():
        with open(ARCHIVO_PEDIDOS, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4, ensure_ascii=False)


def leer_pedidos():
    asegurar_archivo()

    with open(ARCHIVO_PEDIDOS, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def guardar_pedidos(pedidos):
    with open(ARCHIVO_PEDIDOS, "w", encoding="utf-8") as archivo:
        json.dump(
            pedidos,
            archivo,
            indent=4,
            ensure_ascii=False
        )

def crear_pedido(cliente_id: int, venta_id: int, direccion: str):

    pedidos = leer_pedidos()

    nuevo_id = max(
        [pedido["id"] for pedido in pedidos],
        default=0
    ) + 1

    nuevo_pedido = {
        "id": nuevo_id,
        "venta_id": venta_id,
        "cliente_id": cliente_id,
        "direccion": direccion,
        "estado": "Pendiente",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    pedidos.append(nuevo_pedido)

    guardar_pedidos(pedidos)

    return nuevo_pedido

def consultar_estado_pedido(id_pedido: int):

    pedidos = leer_pedidos()

    for pedido in pedidos:

        if pedido["id"] == id_pedido:
            return pedido

    return None