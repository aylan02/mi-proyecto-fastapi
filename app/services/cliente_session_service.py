import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_CLIENTES = BASE_DIR / "clientes.json"


def leer_clientes():

    if not ARCHIVO_CLIENTES.exists():
        return []

    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as archivo:

        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def obtener_cliente_por_usuario(usuario_id: int):

    clientes = leer_clientes()

    for cliente in clientes:

        if cliente.get("usuario_id") == usuario_id:
            return cliente

    return None