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

async function agregarProductoAlCarrito(productoId) {

    try {

        await cargarSesion();

        const clienteId = obtenerClienteId();

        const respuesta = await fetch("/carrito/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                cliente_id: clienteId,
                producto_id: productoId,
                cantidad: 1

            })

        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {

            alert(resultado.detail);
            return;

        }

        alert("Producto agregado al carrito.");

    } catch (error) {

        console.error(error);
        alert("Error al agregar el producto.");

    }

}