import json
from pathlib import Path

from app.services.rol_service import leer_roles
from app.services.security_service import verify_password
BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_USUARIOS = BASE_DIR / "usuarios.json"


def leer_usuarios():
    if not ARCHIVO_USUARIOS.exists():
        return []

    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
        if not contenido:
            return []
        return json.loads(contenido)
  

def autenticar_usuario(username: str, password: str):

    usuarios = leer_usuarios()

    for usuario in usuarios:

        usuario_login = (
            usuario["username"] == username
            or usuario["correo"].lower() == username.lower()
        )

        if usuario_login and verify_password(
            password,
            usuario["password"]
        ):

            roles = leer_roles()

            permisos = []

            for rol in roles:

                if (
                    rol["nombre"] == usuario["rol"]
                    and rol.get("estado") == "Activo"
                ):

                    permisos = rol.get("permisos", [])

                    break

            return {

                "id": usuario["id"],

                "username": usuario["username"],

                "nombre": usuario["nombre"],

                "correo": usuario["correo"],

                "rol": usuario["rol"],

                "permisos": permisos

            }

    return None