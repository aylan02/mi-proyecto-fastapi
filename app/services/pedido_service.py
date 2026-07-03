import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_HISTORIAL = BASE_DIR / "historial.json"


def leer_historial():
    if not ARCHIVO_HISTORIAL.exists():
        return []

    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def consultar_estado_pedido(id_envio: int):
    historial = leer_historial()

    for pedido in historial:
        if pedido.get("id_envio") == id_envio:
            return pedido

    return None