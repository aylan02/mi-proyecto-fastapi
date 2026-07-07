import json
import os

ARCHIVO_PRODUCTOS = "productos.json"
ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_MOVIMIENTOS = "movimientos_inventario.json"
ARCHIVO_CARRITO = "carrito.json"

productos_iniciales = [
    {
        "id": 1,
        "nombre": "Labial Mate",
        "marca": "Maybelline",
        "categoria": "Maquillaje",
        "precio": 5990,
        "stock": 15,
        "descripcion": "Labial de larga duración acabado mate"
    },
    {
        "id": 2,
        "nombre": "Base Líquida",
        "marca": "Loreal",
        "categoria": "Maquillaje",
        "precio": 10990,
        "stock": 10,
        "descripcion": "Base líquida de cobertura media"
    },
    {
        "id": 3,
        "nombre": "Crema Facial",
        "marca": "Nivea",
        "categoria": "Cuidado Facial",
        "precio": 7990,
        "stock": 20,
        "descripcion": "Crema hidratante para uso diario"
    }
]

def cargar_datos(ruta, datos_por_defecto):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return datos_por_defecto

def guardar_datos(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

productos = cargar_datos(ARCHIVO_PRODUCTOS, productos_iniciales)
historial_envios = cargar_datos(ARCHIVO_HISTORIAL, [])
movimientos_inventario = cargar_datos(
    ARCHIVO_MOVIMIENTOS,
    []
)

carrito = cargar_datos(
    ARCHIVO_CARRITO,
    []
)