import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_VENTAS = BASE_DIR / "ventas.json"
ARCHIVO_PRODUCTOS = BASE_DIR / "productos.json"
ARCHIVO_CLIENTES = BASE_DIR / "clientes.json"


def asegurar_archivo(path: Path):
    if not path.exists():
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4, ensure_ascii=False)


def leer_json(path: Path):
    asegurar_archivo(path)
    with open(path, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
        if not contenido:
            return []
        return json.loads(contenido)


def guardar_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)


def leer_ventas():
    return leer_json(ARCHIVO_VENTAS)


def guardar_ventas(ventas):
    guardar_json(ARCHIVO_VENTAS, ventas)


def leer_productos():
    return leer_json(ARCHIVO_PRODUCTOS)


def guardar_productos(productos):
    guardar_json(ARCHIVO_PRODUCTOS, productos)


def leer_clientes():
    return leer_json(ARCHIVO_CLIENTES)


def listar_ventas():
    return leer_ventas()


def obtener_venta(venta_id: int):
    ventas = leer_ventas()
    for venta in ventas:
        if venta["id"] == venta_id:
            return venta
    return None


def obtener_cliente(cliente_id: int):
    clientes = leer_clientes()
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None


def obtener_producto(producto_id: int):
    productos = leer_productos()
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None


def crear_venta(data: dict):
    ventas = leer_ventas()
    productos = leer_productos()
    cliente = obtener_cliente(data["cliente_id"])

    if not cliente:
        raise ValueError("Cliente no encontrado")

    if cliente.get("estado", "Activo") != "Activo":
        raise ValueError("El cliente no está activo")

    detalles_recibidos = data["detalles"]

    if not detalles_recibidos:
        raise ValueError("La venta debe contener al menos un producto")

    acumulado_por_producto = {}
    for detalle in detalles_recibidos:
        producto_id = detalle["producto_id"]
        cantidad = detalle["cantidad"]

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        acumulado_por_producto[producto_id] = acumulado_por_producto.get(producto_id, 0) + cantidad

    mapa_productos = {producto["id"]: producto for producto in productos}

    for producto_id, cantidad_total in acumulado_por_producto.items():
        producto = mapa_productos.get(producto_id)

        if not producto:
            raise ValueError(f"Producto con ID {producto_id} no encontrado")

        if cantidad_total > producto["stock"]:
            raise ValueError(f"Stock insuficiente para el producto '{producto['nombre']}'")

    detalles_guardados = []
    total_venta = 0.0

    for detalle in detalles_recibidos:
        producto = mapa_productos[detalle["producto_id"]]
        subtotal = float(producto["precio"]) * detalle["cantidad"]

        detalles_guardados.append({
            "producto_id": producto["id"],
            "producto_nombre": producto["nombre"],
            "precio_unitario": float(producto["precio"]),
            "cantidad": detalle["cantidad"],
            "subtotal": subtotal
        })

        total_venta += subtotal

    for producto_id, cantidad_total in acumulado_por_producto.items():
        mapa_productos[producto_id]["stock"] -= cantidad_total

    guardar_productos(list(mapa_productos.values()))

    nuevo_id = max([venta["id"] for venta in ventas], default=0) + 1

    nueva_venta = {
        "id": nuevo_id,
        "cliente_id": cliente["id"],
        "cliente_nombre": cliente["nombre"],
        "detalles": detalles_guardados,
        "metodo_pago": data["metodo_pago"],
        "observacion": data.get("observacion", ""),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total_venta,
        "estado": "Registrada"
    }

    ventas.append(nueva_venta)
    guardar_ventas(ventas)

    return nueva_venta


def anular_venta(venta_id: int):
    ventas = leer_ventas()
    productos = leer_productos()

    venta_encontrada = None
    for venta in ventas:
        if venta["id"] == venta_id:
            venta_encontrada = venta
            break

    if not venta_encontrada:
        return None

    if venta_encontrada["estado"] == "Anulada":
        raise ValueError("La venta ya fue anulada")

    mapa_productos = {producto["id"]: producto for producto in productos}

    for detalle in venta_encontrada["detalles"]:
        producto = mapa_productos.get(detalle["producto_id"])
        if producto:
            producto["stock"] += detalle["cantidad"]

    venta_encontrada["estado"] = "Anulada"

    guardar_productos(list(mapa_productos.values()))
    guardar_ventas(ventas)

    return venta_encontrada