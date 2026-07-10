import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_VENTAS = BASE_DIR / "ventas.json"


def listar_historial(cliente_id: int):

    if not ARCHIVO_VENTAS.exists():
        return []

    with open(
        ARCHIVO_VENTAS,
        "r",
        encoding="utf-8"
    ) as archivo:

        ventas = json.load(archivo)

    historial = []

    for venta in ventas:

        if venta["cliente_id"] == cliente_id:

            historial.append(venta)

    return historial