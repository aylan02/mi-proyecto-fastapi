from fastapi import APIRouter, HTTPException, Request, status
from app.schemas.auth import LoginRequest
from app.services.auth_service import autenticar_usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login")
def login(data: LoginRequest, request: Request):
    usuario = autenticar_usuario(data.username, data.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )

    return {"user": usuario}


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"mensaje": "Sesión cerrada correctamente"}