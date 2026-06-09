import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_CLIENTES = BASE_DIR / "clientes.json"


def asegurar_archivo_clientes():
    if not ARCHIVO_CLIENTES.exists():
        ARCHIVO_CLIENTES.write_text("[]", encoding="utf-8")


def leer_clientes():
    asegurar_archivo_clientes()
    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
        if not contenido:
            return []
        return json.loads(contenido)


def guardar_clientes(clientes):
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)


def listar_clientes():
    return leer_clientes()


def obtener_cliente(cliente_id: int):
    clientes = leer_clientes()
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None


def buscar_cliente_por_rut(rut: str):
    clientes = leer_clientes()
    for cliente in clientes:
        if cliente["rut"].strip().lower() == rut.strip().lower():
            return cliente
    return None


def crear_cliente(data: dict):
    clientes = leer_clientes()
    nuevo_id = max([cliente["id"] for cliente in clientes], default=0) + 1

    nuevo_cliente = {
        "id": nuevo_id,
        **data
    }

    clientes.append(nuevo_cliente)
    guardar_clientes(clientes)
    return nuevo_cliente


def actualizar_cliente(cliente_id: int, data: dict):
    clientes = leer_clientes()

    for index, cliente in enumerate(clientes):
        if cliente["id"] == cliente_id:
            cliente_actualizado = {
                **cliente,
                **data,
                "id": cliente_id
            }
            clientes[index] = cliente_actualizado
            guardar_clientes(clientes)
            return cliente_actualizado

    return None


def eliminar_cliente(cliente_id: int):
    clientes = leer_clientes()

    for cliente in clientes:
        if cliente["id"] == cliente_id:
            clientes_filtrados = [c for c in clientes if c["id"] != cliente_id]
            guardar_clientes(clientes_filtrados)
            return cliente

    return None