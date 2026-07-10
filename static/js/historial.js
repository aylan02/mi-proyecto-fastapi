const clienteId = 1;

document.addEventListener("DOMContentLoaded", () => {

    cargarHistorial();

});

async function cargarHistorial() {

    try {

        const respuesta = await fetch(
            `/historial/${clienteId}`
        );

        if (!respuesta.ok) {
            throw new Error("No se pudo cargar el historial.");
        }

        const historial = await respuesta.json();

        renderHistorial(historial);

    } catch (error) {

        console.error(error);

    }

}

function renderHistorial(historial) {

    const contenedor =
        document.getElementById("lista-historial");

    if (!contenedor) return;

    if (historial.length === 0) {

        contenedor.innerHTML = `
            <p>No existen compras realizadas.</p>
        `;

        return;

    }

    let html = "";

    historial.forEach(compra => {

        html += `
        <div class="card-historial">

            <div class="info-historial">

                <h3>Pedido #${compra.id}</h3>

                <p>
                    <strong>Fecha:</strong>
                    ${compra.fecha}
                </p>

                <p>
                    <strong>Total:</strong>
                    $${compra.total.toLocaleString()}
                </p>

                <p>
                    <strong>Método:</strong>
                    ${compra.metodo_pago}
                </p>

                <span class="estado ${compra.estado.toLowerCase()}">

                    ${compra.estado}

                </span>

            </div>

            <button
                class="btn-detalle"
                data-id="${compra.id}"
            >

                Ver detalle

            </button>

        </div>
        `;
    });

    contenedor.innerHTML = html;

    document.querySelectorAll(".btn-detalle").forEach(boton => {

        boton.addEventListener("click", () => {

            const ventaId = boton.dataset.id;

            window.location.href =
                `/cliente/detalle-pedido/${ventaId}`;

        });

    });
}