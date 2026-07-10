verificarSesion();

async function cargarHistorial() {

    try {

        const respuesta = await fetch("/compras");

        if (!respuesta.ok) {
            throw new Error("No fue posible cargar el historial.");
        }

        const compras = await respuesta.json();

        renderHistorial(compras);

    } catch (error) {

        console.error(error);

    }

}

function renderHistorial(compras) {

    const contenedor = document.getElementById("lista-historial");

    if (!contenedor) return;

    if (compras.length === 0) {

        contenedor.innerHTML = `
            <p>No existen compras realizadas.</p>
        `;

        return;

    }

    let html = "";

    compras.forEach(compra => {

        html += `
            <div class="card-historial">

                <div class="info-historial">

                    <h3>Pedido #${compra.id}</h3>

                    <p><strong>Fecha:</strong> ${compra.fecha}</p>

                    <p><strong>Total:</strong> $${compra.total.toLocaleString()}</p>

                    <p><strong>Método:</strong> ${compra.metodo_pago}</p>

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

cargarHistorial();