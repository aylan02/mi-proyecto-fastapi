import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_VENTAS = BASE_DIR / "ventas.json"


def obtener_detalle_pedido(venta_id: int):

    if not ARCHIVO_VENTAS.exists():
        return None

    with open(
        ARCHIVO_VENTAS,
        "r",
        encoding="utf-8"
    ) as archivo:

        ventas = json.load(archivo)

    for venta in ventas:

        if venta["id"] == venta_id:

            return venta

    return None