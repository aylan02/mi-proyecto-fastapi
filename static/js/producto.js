const id = window.location.pathname.split("/").pop();

async function cargarProducto() {

    const respuesta = await fetch(`/productos/${id}`);

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

}

cargarProducto();