import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(BASE_DIR))

from app.services.security_service import hash_password

ARCHIVO_USUARIOS = BASE_DIR / "usuarios.json"


def leer_usuarios():

    if not ARCHIVO_USUARIOS.exists():
        return []

    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_usuarios(usuarios):

    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:

        json.dump(
            usuarios,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def migrar():

    usuarios = leer_usuarios()

    migrados = 0

    for usuario in usuarios:

        password = usuario["password"]

        # Ya está cifrada
        if password.startswith("$2b$"):
            continue

        usuario["password"] = hash_password(password)

        migrados += 1

    guardar_usuarios(usuarios)

    print(f"Usuarios migrados: {migrados}")


if __name__ == "__main__":
    migrar()