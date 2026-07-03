from fastapi import APIRouter, HTTPException, status

from app.schemas.cliente import Cliente, ClienteCrear, ClienteActualizar
from app.services.cliente_service import (
    listar_clientes,
    obtener_cliente,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente,
    buscar_cliente_por_rut
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("", response_model=list[Cliente])
def get_clientes():
    return listar_clientes()


@router.get("/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: int):
    cliente = obtener_cliente(cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    return cliente


@router.post("", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def post_cliente(cliente: ClienteCrear):
    existente = buscar_cliente_por_rut(cliente.rut)

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese RUT/ID"
        )

    return crear_cliente(cliente.model_dump())


@router.put("/{cliente_id}", response_model=Cliente)
def put_cliente(cliente_id: int, cliente: ClienteActualizar):
    cliente_existente = obtener_cliente(cliente_id)

    if not cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    data_actualizada = cliente.model_dump(exclude_unset=True)

    if "rut" in data_actualizada:
        otro_cliente = buscar_cliente_por_rut(data_actualizada["rut"])
        if otro_cliente and otro_cliente["id"] != cliente_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro cliente con ese RUT/ID"
            )

    cliente_actualizado = actualizar_cliente(cliente_id, data_actualizada)
    return cliente_actualizado


@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int):
    cliente_eliminado = eliminar_cliente(cliente_id)

    if cliente_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    if cliente_eliminado == "INACTIVO":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente ya se encuentra desactivado"
        )

    return {"mensaje": "Cliente desactivado correctamente"}