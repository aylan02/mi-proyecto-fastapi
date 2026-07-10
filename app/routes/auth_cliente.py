from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.auth import LoginRequest
from app.schemas.auth_cliente import ClienteRegistro

from app.services.auth_cliente_service import (
    registrar_cliente,
    autenticar_cliente
)

router = APIRouter(
    prefix="/auth-cliente",
    tags=["Autenticación Cliente"]
)

@router.post(
    "/registro",
    status_code=status.HTTP_201_CREATED
)
def post_registro(datos: ClienteRegistro):

    try:

        return registrar_cliente(datos)

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.post("/login")
def login_cliente(
    datos: LoginRequest,
    request: Request
):

    usuario = autenticar_cliente(
        datos.username,
        datos.password
    )

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    request.session["user"] = usuario

    request.session["cliente_id"] = usuario["cliente_id"]

    return {
        "mensaje": "Login correcto",
        "user": usuario
    }
