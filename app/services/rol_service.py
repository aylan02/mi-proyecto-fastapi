import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_ROLES = BASE_DIR / "roles.json"


def asegurar_archivo_roles():
    if not ARCHIVO_ROLES.exists():
        ARCHIVO_ROLES.write_text("[]", encoding="utf-8")


def leer_roles():
    asegurar_archivo_roles()

    with open(ARCHIVO_ROLES, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def guardar_roles(roles):
    with open(ARCHIVO_ROLES, "w", encoding="utf-8") as archivo:
        json.dump(roles, archivo, indent=4, ensure_ascii=False)


def listar_roles():
    return leer_roles()


def obtener_rol(rol_id: int):
    roles = leer_roles()

    for rol in roles:
        if rol["id"] == rol_id:
            return rol

    return None


def buscar_rol_por_nombre(nombre: str):
    roles = leer_roles()

    for rol in roles:
        if rol["nombre"].strip().lower() == nombre.strip().lower():
            return rol

    return None


def crear_rol(data: dict):
    roles = leer_roles()

    nuevo_id = max([rol["id"] for rol in roles], default=0) + 1

    nuevo_rol = {
        "id": nuevo_id,
        **data
    }

    roles.append(nuevo_rol)

    guardar_roles(roles)

    return nuevo_rol


def actualizar_rol(rol_id: int, data: dict):
    roles = leer_roles()

    for index, rol in enumerate(roles):

        if rol["id"] == rol_id:

            rol_actualizado = {
                **rol,
                **data,
                "id": rol_id
            }

            roles[index] = rol_actualizado

            guardar_roles(roles)

            return rol_actualizado

    return None


def desactivar_rol(rol_id: int):
    roles = leer_roles()

    for rol in roles:

        if rol["id"] == rol_id:

            if rol.get("estado") == "Inactivo":
                return "INACTIVO"

            rol["estado"] = "Inactivo"

            guardar_roles(roles)

            return rol

    return None