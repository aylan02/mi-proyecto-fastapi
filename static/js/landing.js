async function obtenerProductos() {

    try {

        const respuesta = await fetch("/productos?limit=100&offset=0");

        const datos = await respuesta.json();

        const productos = datos.resultados;

        const contenedor = document.getElementById("contenedor-productos");

        contenedor.innerHTML = "";

        productos.forEach(producto => {

            contenedor.innerHTML += `

               <div class="producto-card">

    <div class="producto-imagen">

        <span class="badge">
            ⭐ Destacado
        </span>

        <div class="placeholder-img">

            📦

        </div>

    </div>

    <div class="producto-info">

        <h3>${producto.nombre}</h3>

        <p class="marca">${producto.marca}</p>

        <p class="precio">

            $${producto.precio.toLocaleString("es-CL")}

        </p>

        <div class="producto-botones">

            <button
                class="btn-detalle"
                onclick="window.location.href='/cliente/producto/${producto.id}'">

                Ver detalle

            </button>

            <button class="btn-carrito">

                Agregar

            </button>

        </div>

    </div>

</div>

`;

});

} catch (error) {

    console.error(error);

}

}

obtenerProductos();