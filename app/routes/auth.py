from fastapi import APIRouter, HTTPException, Request, status
from app.schemas.auth import LoginRequest
from app.services.auth_service import autenticar_usuario
from app.services.cliente_session_service import obtener_cliente_por_usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
def login(data: LoginRequest, request: Request):

    usuario = autenticar_usuario(
        data.username,
        data.password
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    request.session["user"] = usuario

    # ============================
    # SESIÓN DEL CLIENTE
    # ============================

    if usuario["rol"] == "Cliente":

        cliente = obtener_cliente_por_usuario(
            usuario["id"]
        )

        if cliente:

            request.session["cliente_id"] = cliente["id"]

    return {
        "mensaje": "Login correcto",
        "user": usuario
    }


@router.get("/me")
def me(request: Request):

    usuario = request.session.get("user")

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )

    respuesta = {
        "user": usuario
    }

    cliente_id = request.session.get("cliente_id")

    if cliente_id:

        respuesta["cliente_id"] = cliente_id

    return respuesta


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"mensaje": "Sesión cerrada correctamente"}