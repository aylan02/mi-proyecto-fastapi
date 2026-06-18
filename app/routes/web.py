from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/web", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get("/web", response_class=HTMLResponse)
def mostrar_web(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )