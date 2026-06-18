import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVO_USUARIOS = BASE_DIR / "usuarios.json"

PERMISOS_POR_ROL = {
    "Administrador": [
        "dashboard", "productos", "inventario", "clientes", "ventas",
        "envios", "rutas", "usuarios", "roles", "reportes", "seguimiento"
    ],
    "Ejecutivo Comercial": [
        "dashboard", "clientes", "ventas", "reportes"
    ],
    "Encargado de Inventario": [
        "dashboard", "productos", "inventario", "reportes"
    ],
    "Coordinador Logístico": [
        "dashboard", "envios", "rutas", "seguimiento", "reportes"
    ]
}


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
        if usuario["username"] == username and usuario["password"] == password:
            return {
                "id": usuario["id"],
                "username": usuario["username"],
                "nombre": usuario["nombre"],
                "rol": usuario["rol"],
                "permisos": PERMISOS_POR_ROL.get(usuario["rol"], [])
            }

    return None