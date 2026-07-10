let clienteId = null;
const id = window.location.pathname.split("/").pop();

async function cargarProducto() {

    try {

        const respuesta = await fetch(`/productos/${id}`);

        if (!respuesta.ok) {
            throw new Error("No se pudo cargar el producto.");
        }

        const producto = await respuesta.json();

        document.getElementById("nombre-producto").textContent =
            producto.nombre;

        document.getElementById("marca-producto").textContent =
            producto.marca;

        document.getElementById("precio-producto").textContent =
            "$" + producto.precio.toLocaleString("es-CL");

        document.getElementById("descripcion-producto").textContent =
            producto.descripcion;

        document.getElementById("stock-producto").textContent =
            "Stock disponible: " + producto.stock;

        document.querySelector(".categoria").textContent =
            producto.categoria;

    } catch (error) {

        console.error(error);

    }

}

async function agregarAlCarrito() {

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
                producto_id: Number(id),
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

document
    .getElementById("btn-agregar-carrito")
    .addEventListener("click", agregarAlCarrito);

cargarProducto();

verificarSesion();