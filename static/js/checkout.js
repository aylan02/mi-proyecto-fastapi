document.addEventListener("DOMContentLoaded", async () => {

    try {

        await cargarSesion();

        cargarCheckout(obtenerClienteId());

    } catch (error) {

        console.error(error);

        window.location.href = "/cliente/login";

        return;

    }

    const formulario = document.getElementById("form-checkout");

    const btnPagar = document.getElementById("btn-pagar");

    btnPagar.addEventListener("click", (event) => {

        event.preventDefault();

        if (!formulario.checkValidity()) {

            formulario.reportValidity();

            return;

        }

        const datosCheckout = {

            destinatario: document.getElementById("nombre").value,

            direccion: document.getElementById("direccion").value,

            correo: document.getElementById("correo").value,

            telefono: document.getElementById("telefono").value,

            ciudad: document.getElementById("ciudad").value,

            region: document.getElementById("region").value,

            observacion: document.getElementById("observacion").value

        };

        sessionStorage.setItem(
            "checkout",
            JSON.stringify(datosCheckout)
        );

        window.location.href = "/cliente/pago";

    });

});

async function cargarCheckout(clienteId) {

    try {

        const respuesta = await fetch(`/carrito/${clienteId}`);

        if (!respuesta.ok) {
            throw new Error("No se pudo obtener el carrito.");
        }

        const carrito = await respuesta.json();

        renderProductos(carrito);

        actualizarResumen(carrito);

    } catch (error) {

        console.error(error);

    }

}

function renderProductos(carrito) {

    const contenedor = document.getElementById("lista-checkout");

    if (!contenedor) return;

    if (carrito.items.length === 0) {

        contenedor.innerHTML = `
            <p>No hay productos en el carrito.</p>
        `;

        return;

    }

    let html = "";

    carrito.items.forEach(producto => {

        html += `
            <div class="item-checkout">

                <img
                    src="/static/img/productos/${producto.imagen}"
                    alt="${producto.nombre}"
                    class="item-imagen"
                >

                <div class="item-info">

                    <h4>${producto.nombre}</h4>

                    <p>${producto.marca}</p>

                    <p>
                        Cantidad: ${producto.cantidad}
                    </p>

                </div>

                <div class="item-precio">

                    $${producto.subtotal.toLocaleString()}

                </div>

            </div>
        `;

    });

    contenedor.innerHTML = html;

}

function actualizarResumen(carrito) {

    document.getElementById("cantidad-productos").textContent =
        carrito.total_productos;

    document.getElementById("subtotal").textContent =
        `$${carrito.total.toLocaleString()}`;

    document.getElementById("total").textContent =
        `$${carrito.total.toLocaleString()}`;

}

verificarSesion();
