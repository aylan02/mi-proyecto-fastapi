import json
from pathlib import Path
from app.services.security_service import (
    hash_password,
    verify_password
)

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_USUARIOS = BASE_DIR / "usuarios.json"
ARCHIVO_CLIENTES = BASE_DIR / "clientes.json"


def leer_json(ruta):

    if not ruta.exists():
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:

        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)


def guardar_json(ruta, datos):

    with open(ruta, "w", encoding="utf-8") as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def obtener_nuevo_id(lista):

    if not lista:
        return 1

    return max(item["id"] for item in lista) + 1


def registrar_cliente(datos):

    usuarios = leer_json(ARCHIVO_USUARIOS)

    clientes = leer_json(ARCHIVO_CLIENTES)

    # =====================
    # VALIDAR CORREO
    # =====================

    for usuario in usuarios:

        if usuario["correo"].strip().lower() == datos.correo.strip().lower():

            raise ValueError(
                "El correo ya se encuentra registrado."
            )
   
    for usuario in usuarios:

        if usuario["username"].strip().lower() == datos.username.strip().lower():

            raise ValueError(
                "El nombre de usuario ya está en uso."
            )
    # =====================
    # VALIDAR CONTRASEÑAS
    # =====================

    if datos.password != datos.confirmar_password:

        raise ValueError(
            "Las contraseñas no coinciden."
        )

    # =====================
    # CREAR USUARIO
    # =====================
    nuevo_usuario = {

        "id": obtener_nuevo_id(usuarios),

        "username": datos.username,

        "password": hash_password(datos.password),

        "nombre": datos.nombre,

        "correo": datos.correo,

        "rol": "Cliente",

        "estado": "Activo"

    }

    usuarios.append(nuevo_usuario)

    guardar_json(
        ARCHIVO_USUARIOS,
        usuarios
    )

    # =====================
    # CREAR CLIENTE
    # =====================

    nuevo_cliente = {

        "id": obtener_nuevo_id(clientes),

        "usuario_id": nuevo_usuario["id"],

        "nombre": datos.nombre,

        "apellido": datos.apellido,

        "correo": datos.correo,

        "telefono": "",

        "direccion": "",

        "estado": "Activo"

    }

    clientes.append(nuevo_cliente)

    guardar_json(
        ARCHIVO_CLIENTES,
        clientes
    )

    return {

        "mensaje": "Cliente registrado correctamente.",

        "usuario": nuevo_usuario,

        "cliente": nuevo_cliente

    }

def autenticar_cliente(username: str, password: str):

    usuarios = leer_json(ARCHIVO_USUARIOS)

    for usuario in usuarios:

        if (
            usuario["username"] == username
            and usuario["rol"] == "Cliente"
            and usuario["estado"] == "Activo"
        ):

            if verify_password(
                password,
                usuario["password"]
            ):

                clientes = leer_json(ARCHIVO_CLIENTES)

                cliente = next(
                    (
                        c for c in clientes
                        if c.get("usuario_id") == usuario["id"]
                    ),
                    None
                )

                return {

                    "id": usuario["id"],

                    "cliente_id": cliente["id"] if cliente else None,

                    "username": usuario["username"],

                    "nombre": usuario["nombre"],

                    "correo": usuario["correo"],

                    "rol": usuario["rol"]

                }

    return None