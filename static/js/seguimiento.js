const ventaId =
    window.location.pathname.split("/").pop();

async function cargarSeguimiento(){

    const respuesta =
        await fetch(`/seguimiento/${ventaId}`);

    const seguimiento =
        await respuesta.json();

    renderSeguimiento(seguimiento);

}

function renderSeguimiento(seguimiento){
   
    const contenedor =
        document.getElementById("seguimiento");

    let html = `

        <div class="card-seguimiento">

           <div class="info-pedido">

                <div>

                    <span class="titulo">

                        Pedido

                    </span>

                    <p>

                        #${seguimiento.pedido_id}

                    </p>

                </div>

                <div>

                    <span class="titulo">

                        Cliente

                    </span>

                    <p>

                        ${seguimiento.cliente}

                    </p>

                </div>

                <div>

                    <span class="titulo">

                        Método

                    </span>

                    <p>

                        ${seguimiento.metodo}

                    </p>

                </div>

                <div>

                    <span class="titulo">

                        Fecha

                    </span>

                    <p>

                        ${seguimiento.fecha}

                    </p>

                </div>

            </div>

            <div class="estado-actual">

                <h3>

                    Estado actual

                </h3>

                <h2>

                🚚 ${seguimiento.estado_actual}

                </h2>

                <p class="mensaje-estado">

                   Tu pedido está avanzando correctamente.

                </p>

            </div>

            <div class="timeline">
    `;

    seguimiento.estados.forEach(estado=>{

        html +=`

            <div class="paso ${estado.completado ? "completado":""}">

                <div class="circulo">

                    ${estado.completado ? "✓" : "○"}

                </div>

                <p>

                    ${estado.nombre}

                </p>

                <small>

                    ${estado.descripcion}

                </small>

            </div>

        `;

    });

    html +=`

            </div>

        </div>

    `;

    contenedor.innerHTML = html;

}

document.addEventListener("DOMContentLoaded", async () => {

    try {

        await cargarSesion();

        await cargarSeguimiento();

    } catch (error) {

        console.error(error);

        window.location.href = "/cliente/login";

    }

});

verificarSesion();