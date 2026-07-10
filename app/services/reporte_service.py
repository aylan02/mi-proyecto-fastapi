import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_PRODUCTOS = BASE_DIR / "productos.json"
ARCHIVO_VENTAS = BASE_DIR / "ventas.json"
ARCHIVO_CLIENTES = BASE_DIR / "clientes.json"
ARCHIVO_ENVIOS = BASE_DIR / "envios.json"
ARCHIVO_MOVIMIENTOS = BASE_DIR / "movimientos_inventario.json"


def leer_json(ruta):
    if not ruta.exists():
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return []

        return json.loads(contenido)
    
def reporte_inventario():
    productos = leer_json(ARCHIVO_PRODUCTOS)
    movimientos = leer_json(ARCHIVO_MOVIMIENTOS)

    productos_activos = [
        p for p in productos
        if p.get("estado") == "Activo"
    ]

    productos_sin_stock = [
        p for p in productos
        if p.get("stock", 0) == 0
    ]

    productos_bajo_stock = [
        p for p in productos
        if 0 < p.get("stock", 0) < 10
    ]

    total_ingresos = sum(
        m["cantidad"]
        for m in movimientos
        if m["tipo"] == "Ingreso"
    )

    total_salidas = sum(
        m["cantidad"]
        for m in movimientos
        if m["tipo"] == "Salida"
    )

    valor_total_stock = sum(
        producto["precio"] * producto["stock"]
        for producto in productos
    )

    return {
        "resumen": {
            "total_productos": len(productos),
            "productos_activos": len(productos_activos),
            "productos_sin_stock": len(productos_sin_stock),
            "productos_bajo_stock": len(productos_bajo_stock),
            "total_movimientos": len(movimientos),
            "total_ingresos": total_ingresos,
            "total_salidas": total_salidas,
            "valor_total_stock": valor_total_stock
        },
        "productos": productos,
        "movimientos": movimientos
    }

def reporte_ventas():
    ventas = leer_json(ARCHIVO_VENTAS)

    ventas_registradas = [
        v for v in ventas
        if v.get("estado") == "Registrada"
    ]

    ventas_anuladas = [
        v for v in ventas
        if v.get("estado") == "Anulada"
    ]

    monto_total = sum(
        venta.get("total", 0)
        for venta in ventas_registradas
    )

    return {
        "resumen": {
            "total_ventas": len(ventas),
            "ventas_registradas": len(ventas_registradas),
            "ventas_anuladas": len(ventas_anuladas),
            "monto_total": monto_total
        },
        "ventas": ventas
    }


def reporte_clientes():
    clientes = leer_json(ARCHIVO_CLIENTES)

    clientes_activos = [
        c for c in clientes
        if c.get("estado") == "Activo"
    ]

    clientes_inactivos = [
        c for c in clientes
        if c.get("estado") == "Inactivo"
    ]

    return {
        "resumen": {
            "total_clientes": len(clientes),
            "clientes_activos": len(clientes_activos),
            "clientes_inactivos": len(clientes_inactivos)
        },
        "clientes": clientes
    }

def reporte_logistico():

    envios = leer_json(ARCHIVO_ENVIOS)

    preparados = [
        e for e in envios
        if e.get("estado", "").lower() == "preparando"
    ]

    en_ruta = [
        e for e in envios
        if e.get("estado", "").lower() == "en ruta"
    ]

    entregados = [
        e for e in envios
        if e.get("estado", "").lower() == "entregado"
    ]

    return {
        "resumen": {
            "total_envios": len(envios),
            "preparando": len(preparados),
            "en_ruta": len(en_ruta),
            "entregados": len(entregados)
        },
        "envios": envios
    }