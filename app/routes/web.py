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