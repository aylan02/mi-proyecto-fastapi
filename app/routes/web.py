from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="templates")


# ===========================
# PORTAL DEL CLIENTE
# ===========================

@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cliente/landing.html",
        context={}
    )

@router.get("/cliente/producto/{producto_id}", response_class=HTMLResponse)
def detalle_producto(request: Request, producto_id: int):

    return templates.TemplateResponse(
        request=request,
        name="cliente/producto.html",
        context={
            "producto_id": producto_id
        }
    )

@router.get("/cliente/catalogo", response_class=HTMLResponse)
def catalogo(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/catalogo.html",
        context={}
    )

@router.get("/cliente/carrito", response_class=HTMLResponse)
def carrito(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/carrito.html",
        context={}
    )

@router.get("/cliente/checkout", response_class=HTMLResponse)
def checkout(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/checkout.html",
        context={}
    )


@router.get("/cliente/pago", response_class=HTMLResponse)
def pago(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/pago.html",
        context={}
    )

@router.get("/cliente/historial", response_class=HTMLResponse)
def historial(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/historial.html",
        context={}
    )

@router.get("/cliente/detalle-pedido/{venta_id}", response_class=HTMLResponse)
def detalle_pedido(request: Request, venta_id: int):

    return templates.TemplateResponse(
        request=request,
        name="cliente/detalle_pedido.html",
        context={
            "venta_id": venta_id
        }
    )

@router.get("/cliente/seguimiento/{venta_id}", response_class=HTMLResponse)
def seguimiento(
    request: Request,
    venta_id: int
):

    return templates.TemplateResponse(
        request=request,
        name="cliente/seguimiento.html",
        context={
            "venta_id": venta_id
        }
    )

@router.get("/cliente/login", response_class=HTMLResponse)
def login_cliente(request: Request):

    if request.session.get("user"):

        return RedirectResponse(
            url="/cliente/catalogo",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="cliente/login_cliente.html",
        context={}
    )

@router.get("/cliente/registro", response_class=HTMLResponse)
def registro_cliente(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/registro.html",
        context={}
    )

@router.get("/cliente/perfil", response_class=HTMLResponse)
def perfil_cliente(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cliente/perfil.html",
        context={}
    )

# ===========================
# PANEL ADMINISTRATIVO
# ===========================

@router.get("/admin/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/admin", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={}
    )


@router.get("/admin", response_class=HTMLResponse)
def mostrar_web(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(url="/admin/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={}
    )