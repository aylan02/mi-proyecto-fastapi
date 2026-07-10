const ventaId = window.location.pathname.split("/").pop();

document.addEventListener("DOMContentLoaded", async () => {

    try {

        await cargarSesion();

        await cargarDetallePedido();

    } catch (error) {

        console.error(error);

        window.location.href = "/cliente/login";

    }

});

async function cargarDetallePedido() {

    try {

        const respuesta = await fetch(
            `/detalle-pedido/${ventaId}`
        );

        if (!respuesta.ok) {

            throw new Error("No se pudo obtener el pedido.");

        }

        const pedido = await respuesta.json();

        renderDetalle(pedido);

    } catch (error) {

        console.error(error);

    }

}

function renderDetalle(pedido) {

    const contenedor =
        document.getElementById("detalle-pedido");

    let html = `
        <div class="cabecera-pedido">

            <div>

                <h2>Pedido #${pedido.id}</h2>

                <p>

                    <strong>Cliente:</strong>

                    ${pedido.cliente_nombre}

                </p>

            </div>

            <span class="estado estado-${pedido.estado.toLowerCase()}">

                ${pedido.estado}

            </span>

        </div>

        <div class="grid-info">

            <div>

                <div class="dato">

                    <span class="titulo">

                        Fecha

                    </span>

                    <p>

                        ${pedido.fecha}

                    </p>

                </div>

                <div class="dato">

                    <span class="titulo">

                        Método

                    </span>

                    <p>

                        ${pedido.metodo_pago}

                    </p>

                </div>

                <div class="dato">

                    <span class="titulo">

                        Observación

                    </span>

                    <p>

                        ${pedido.observacion}

                    </p>

                </div>

            </div>

        </div>

        <hr>

        <h3>Productos</h3>
    `;

    pedido.detalles.forEach(producto => {

        html += `

            <div class="producto-detalle">

                <div class="producto-imagen">

                    📦

                </div>

                <div class="producto-info">

                    <h4>${producto.producto_nombre}</h4>

                    <p>

                        Cantidad:
                        ${producto.cantidad}

                    </p>

                    <p>

                        Precio Unitario:
                        $${producto.precio_unitario.toLocaleString()}

                    </p>

                </div>

                <div class="producto-subtotal">

                    $${producto.subtotal.toLocaleString()}

                </div>

            </div>

        `;

    });

    html += `

        <hr>

        <div class="resumen-total">

            <span>Total del pedido</span>

            <h2>

                $${pedido.total.toLocaleString()}

            </h2>

        </div>

        <button
            class="btn-seguimiento"
            data-id="${pedido.id}"
        >

            🚚 Ver seguimiento

        </button>

        </div>
    `;

    contenedor.innerHTML = html;

    document
        .querySelector(".btn-seguimiento")
        .addEventListener("click", () => {

            window.location.href =
                `/cliente/seguimiento/${pedido.id}`;

        });

}

verificarSesion();