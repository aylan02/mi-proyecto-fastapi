const clienteId = 1; 

document.addEventListener("DOMContentLoaded", () => {

    cargarCarrito();

    const btnVaciar = document.getElementById("btn-vaciar");

    if (btnVaciar) {

        btnVaciar.addEventListener("click", () => {

            vaciarCarrito();

        });

    }

    const btnCheckout = document.getElementById("btn-checkout");

    if (btnCheckout) {

        btnCheckout.addEventListener("click", () => {

            window.location.href = "/cliente/checkout";

        });

    }

});

async function cargarCarrito() {

    try {

        const respuesta = await fetch(`/carrito/${clienteId}`);

        if (!respuesta.ok) {
            throw new Error("No se pudo obtener el carrito.");
        }

       const carrito = await respuesta.json();

        renderCarrito(carrito);

        actualizarResumen(carrito);

    } catch (error) {

        console.error(error);

    }

}

function renderCarrito(carrito) {

    const contenedor = document.getElementById("lista-carrito");

    if (!contenedor) return;

    contenedor.innerHTML = "";

    if (carrito.items.length === 0) {

        contenedor.innerHTML = `
            <p class="carrito-vacio">
                Tu carrito está vacío.
            </p>
        `;

        return;
    }

   let html = "";

    carrito.items.forEach(producto => {

        html += `
            <div class="item-carrito">

                <img
                    src="${producto.imagen}"
                    alt="${producto.nombre}"
                >

                <div class="info-producto">

                    <h3>${producto.nombre}</h3>

                    <p>${producto.marca}</p>

                    <p>$${producto.precio.toLocaleString()}</p>

                    <div class="cantidad-producto">

                        <button
                            class="btn-cantidad disminuir"
                            data-id="${producto.producto_id}"
                        >
                            −
                        </button>

                        <span>${producto.cantidad}</span>

                        <button
                            class="btn-cantidad aumentar"
                            data-id="${producto.producto_id}"
                        >
                            +
                        </button>

                    </div>
                </div>

                <div class="subtotal">

                    $${producto.subtotal.toLocaleString()}

                </div>

                <button
                class="btn-eliminar"
                    data-id="${producto.producto_id}"
            >
                    🗑
                </button>

                </div>
        `;

});

contenedor.innerHTML = html;

document.querySelectorAll(".aumentar").forEach(boton => {

    boton.addEventListener("click", () => {

        const productoId = Number(boton.dataset.id);

        const producto = carrito.items.find(
            item => item.producto_id === productoId
        );

        actualizarCantidad(
            productoId,
            producto.cantidad + 1
        );

    });

});

document.querySelectorAll(".disminuir").forEach(boton => {

    boton.addEventListener("click", () => {

        const productoId = Number(boton.dataset.id);

        const producto = carrito.items.find(
            item => item.producto_id === productoId
        );

        if (producto.cantidad > 1) {

            actualizarCantidad(
                productoId,
                producto.cantidad - 1
            );

        }

    });

});

document.querySelectorAll(".btn-eliminar").forEach(boton => {

    boton.addEventListener("click", () => {

        const productoId = Number(boton.dataset.id);

        eliminarProducto(productoId);

    });

});
}

function actualizarResumen(carrito) {

    document.getElementById("cantidad-productos").textContent =
        carrito.total_productos;

    document.getElementById("subtotal").textContent =
        `$${carrito.total.toLocaleString()}`;

    document.getElementById("total").textContent =
        `$${carrito.total.toLocaleString()}`;

}

async function actualizarCantidad(productoId, cantidad) {

    try {

        const respuesta = await fetch(`/carrito/${clienteId}/${productoId}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                cantidad: cantidad
            })

        });

        if (!respuesta.ok) {
            throw new Error("No se pudo actualizar la cantidad.");
        }

        cargarCarrito();

    } catch (error) {

        console.error(error);

    }

}

async function eliminarProducto(productoId) {

    try {

        const respuesta = await fetch(`/carrito/${clienteId}/${productoId}`, {

            method: "DELETE"

        });

        if (!respuesta.ok) {
            throw new Error("No se pudo eliminar el producto.");
        }

        cargarCarrito();

    } catch (error) {

        console.error(error);

    }

}

async function vaciarCarrito() {

    try {

        const respuesta = await fetch(`/carrito/${clienteId}`, {

            method: "DELETE"

        });

        if (!respuesta.ok) {
            throw new Error("No se pudo vaciar el carrito.");
        }

        cargarCarrito();

    } catch (error) {

        console.error(error);

    }

}

