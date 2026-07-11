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

    # No permitir clientes en el panel admin
    if usuario["rol"] == "Cliente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los clientes no pueden acceder al Panel Administrativo."
        )

    request.session["user"] = usuario

    return {
        "mensaje": "Login correcto",
        "user": usuario
    }

@router.get("/me")
def me(request: Request):

    usuario = request.session.get("user")

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )

    respuesta = {
        "user": usuario
    }

    cliente_id = request.session.get("cliente_id")

    print("SESSION CLIENTE_ID:", cliente_id)

    if cliente_id:
        respuesta["cliente_id"] = cliente_id

    print(respuesta)

    return respuesta


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"mensaje": "Sesión cerrada correctamente"}