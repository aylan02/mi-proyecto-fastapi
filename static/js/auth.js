let sesionActual = null;

async function cargarSesion() {

    if (sesionActual !== null) {
        return sesionActual;
    }

    const respuesta = await fetch("/auth/me");

    if (!respuesta.ok) {
        throw new Error("Usuario no autenticado.");
    }

    const datos = await respuesta.json();

    sesionActual = datos;

    return sesionActual;

}

function obtenerSesion() {

    return sesionActual;

}

function obtenerClienteId() {

    if (!sesionActual) {
        throw new Error("Sesión no cargada.");
    }

    return sesionActual.cliente_id;

}

function obtenerUsuario() {

    if (!sesionActual) {
        throw new Error("Sesión no cargada.");
    }

    return sesionActual.user;

}