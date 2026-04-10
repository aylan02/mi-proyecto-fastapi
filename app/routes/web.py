from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Web"])

templates = Jinja2Templates(directory="templates")

@router.get("/web", response_class=HTMLResponse)
def mostrar_web(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )