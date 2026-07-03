import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_USUARIOS = BASE_DIR / "usuarios.json"


def asegurar_archivo_usuarios():
    if not ARCHIVO_USUARIOS.exists():
        ARCHIVO_USUARIOS.write_text("[]", encoding="utf-8")


def leer_usuarios():
    asegurar_archivo_usuarios()

    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


def listar_usuarios():
    return leer_usuarios()


def obtener_usuario(usuario_id: int):
    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario

    return None


def buscar_usuario_por_username(username: str):
    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario["username"].strip().lower() == username.strip().lower():
            return usuario

    return None


def crear_usuario(data: dict):
    usuarios = leer_usuarios()

    nuevo_id = max([u["id"] for u in usuarios], default=0) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        **data
    }

    usuarios.append(nuevo_usuario)

    guardar_usuarios(usuarios)

    return nuevo_usuario


def actualizar_usuario(usuario_id: int, data: dict):
    usuarios = leer_usuarios()

    for index, usuario in enumerate(usuarios):
        if usuario["id"] == usuario_id:

            usuario_actualizado = {
                **usuario,
                **data,
                "id": usuario_id
            }

            usuarios[index] = usuario_actualizado

            guardar_usuarios(usuarios)

            return usuario_actualizado

    return None


def desactivar_usuario(usuario_id: int):
    usuarios = leer_usuarios()

    for usuario in usuarios:

        if usuario["id"] == usuario_id:

            if usuario.get("estado") == "Inactivo":
                return "INACTIVO"

            usuario["estado"] = "Inactivo"

            guardar_usuarios(usuarios)

            return usuario

    return None