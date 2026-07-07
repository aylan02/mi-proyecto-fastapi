import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_RUTAS = BASE_DIR / "rutas.json"


def asegurar_archivo_rutas():
    if not ARCHIVO_RUTAS.exists():
        ARCHIVO_RUTAS.write_text("[]", encoding="utf-8")


def leer_rutas():
    asegurar_archivo_rutas()

    with open(ARCHIVO_RUTAS, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def guardar_rutas(rutas):
    with open(ARCHIVO_RUTAS, "w", encoding="utf-8") as archivo:
        json.dump(rutas, archivo, indent=4, ensure_ascii=False)


def listar_rutas():
    return leer_rutas()


def obtener_ruta(ruta_id: int):
    rutas = leer_rutas()

    for ruta in rutas:
        if ruta["id"] == ruta_id:
            return ruta

    return None


def crear_ruta(data: dict):
    rutas = leer_rutas()

    nuevo_id = max([r["id"] for r in rutas], default=0) + 1

    nueva_ruta = {
        "id": nuevo_id,
        **data
    }

    rutas.append(nueva_ruta)

    guardar_rutas(rutas)

    return nueva_ruta


def actualizar_ruta(ruta_id: int, data: dict):
    rutas = leer_rutas()

    for index, ruta in enumerate(rutas):
        if ruta["id"] == ruta_id:

            ruta_actualizada = {
                **ruta,
                **data,
                "id": ruta_id
            }

            rutas[index] = ruta_actualizada

            guardar_rutas(rutas)

            return ruta_actualizada

    return None


def desactivar_ruta(ruta_id: int):
    rutas = leer_rutas()

    for ruta in rutas:

        if ruta["id"] == ruta_id:

            if ruta.get("estado") == "Inactiva":
                return "INACTIVA"

            ruta["estado"] = "Inactiva"

            guardar_rutas(rutas)

            return ruta

    return None