from fastapi import APIRouter

from app.services.reporte_service import (
    reporte_inventario,
    reporte_ventas,
    reporte_clientes,
    reporte_logistico
)

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)


@router.get("/inventario")
def get_reporte_inventario():
    return reporte_inventario()


@router.get("/ventas")
def get_reporte_ventas():
    return reporte_ventas()


@router.get("/clientes")
def get_reporte_clientes():
    return reporte_clientes()


@router.get("/logistico")
def get_reporte_logistico():
    return reporte_logistico()