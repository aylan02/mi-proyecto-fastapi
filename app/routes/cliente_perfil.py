from fastapi import APIRouter, HTTPException, Request
from app.schemas.cliente import ClientePerfilActualizar
from app.services.cliente_service import (
    obtener_cliente,
    actualizar_cliente
)

router = APIRouter(
    prefix="/api/cliente",
    tags=["Perfil Cliente"]
)


@router.get("/perfil")
def obtener_perfil(request: Request):

    cliente_id = request.session.get("cliente_id")

    usuario = request.session.get("user")

    if not cliente_id or not usuario:

        raise HTTPException(
            status_code=401,
            detail="Debe iniciar sesión."
        )

    cliente = obtener_cliente(cliente_id)

    if not cliente:

        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    return {

        "nombre": cliente.get("nombre", ""),

        "apellido": cliente.get("apellido", ""),

        "correo": cliente.get("correo", ""),

        "telefono": cliente.get("telefono", ""),

        "direccion": cliente.get("direccion", ""),

        "username": usuario.get("username", "")

    }

@router.put("/perfil")
def actualizar_perfil(
    datos: ClientePerfilActualizar,
    request: Request
):

    cliente_id = request.session.get("cliente_id")

    if not cliente_id:

        raise HTTPException(
            status_code=401,
            detail="Debe iniciar sesión."
        )

    cliente = actualizar_cliente(
        cliente_id,
        datos.model_dump()
    )

    if not cliente:

        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    return {
        "mensaje": "Perfil actualizado correctamente."
    }