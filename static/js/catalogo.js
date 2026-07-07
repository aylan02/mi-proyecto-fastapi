const buscador = document.getElementById("buscar");

const categoria = document.getElementById("categoria");

async function cargarCatalogo(nombre = "", categoriaSeleccionada = "") {

    const respuesta = await fetch(

        `/productos?limit=100&nombre=${nombre}&categoria=${categoriaSeleccionada}`

    );

    const datos = await respuesta.json();

    const contenedor = document.getElementById("catalogo-productos");

    contenedor.innerHTML = "";

    datos.resultados.forEach(producto => {

        contenedor.innerHTML += `

            <div class="producto-card">

                <div class="producto-imagen">

                    <div class="placeholder-img">

                        📦

                    </div>

                </div>

                <div class="producto-info">

                    <h3>${producto.nombre}</h3>

                    <p class="marca">

                        ${producto.marca}

                    </p>

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

}

cargarCatalogo();
buscador.addEventListener("input", () => {

    cargarCatalogo(

        buscador.value,

        categoria.value

    );

});

categoria.addEventListener("change", () => {

    cargarCatalogo(

        buscador.value,

        categoria.value

    );

});