document.addEventListener("DOMContentLoaded", async () => {

    try {

        await cargarSesion();

        await cargarResumenPago(obtenerClienteId());

    } catch (error) {

        console.error(error);

        window.location.href = "/cliente/login";

        return;

    }

    const radios = document.querySelectorAll('input[name="metodo"]');

    const formulario = document.getElementById("formulario-tarjeta");

    radios.forEach(radio => {

        radio.addEventListener("change", () => {

            if (
                radio.value === "credito" ||
                radio.value === "debito"
            ) {

                formulario.style.display = "block";

            } else {

                formulario.style.display = "none";

            }

        });

    });

// ==========================
// VISTA PREVIA DE LA TARJETA
// ==========================

const inputTitular = document.getElementById("titular");
const inputNumero = document.getElementById("numero");
const inputFecha = document.getElementById("fecha");
const inputCVV = document.getElementById("cvv");
const previewCVV = document.getElementById("cvv-preview");

const previewTitular = document.getElementById("titular-preview");
const previewNumero = document.getElementById("numero-preview");
const previewFecha = document.getElementById("fecha-preview");
const logoPreview = document.getElementById("logo-preview");
const tarjetaPreview = document.getElementById("tarjeta-preview");
const tarjetaVisual = document.querySelector(".tarjeta-visual");
// Nombre del titular
inputTitular.addEventListener("input", () => {

    if (inputTitular.value.trim() === "") {

        previewTitular.textContent = "NOMBRE APELLIDO";

        return;

    }

    previewTitular.textContent =
        inputTitular.value.toUpperCase();

});


// Número de tarjeta

inputNumero.addEventListener("input", () => {

    let valor = inputNumero.value;

    valor = valor.replace(/\D/g, "");

    valor = valor.substring(0,16);

    valor = valor.replace(/(.{4})/g, "$1 ").trim();

    inputNumero.value = valor;

    if (valor === "") {

        previewNumero.textContent =
            "0000 0000 0000 0000";

    } else {

        previewNumero.textContent = valor;

    }

    // ==========================
    // Detectar tipo de tarjeta
    // ==========================

    const numero = valor.replace(/\s/g, "");

    if (numero.startsWith("4")) {

        logoPreview.className =
            "fa-brands fa-cc-visa";

        tarjetaPreview.style.background =
            "linear-gradient(135deg,#1f6fd5,#0c4ea3)";

    }
    else if (numero.startsWith("5")) {

        logoPreview.className =
            "fa-brands fa-cc-mastercard";

        tarjetaPreview.style.background =
            "linear-gradient(135deg,#eb001b,#f79e1b)";

    }
    else if (numero.startsWith("3")) {

        logoPreview.className =
            "fa-brands fa-cc-amex";

        tarjetaPreview.style.background =
            "linear-gradient(135deg,#2e8b57,#3cb371)";

    }
    else {

        logoPreview.className =
            "fa-regular fa-credit-card";

        tarjetaPreview.style.background =
            "linear-gradient(135deg,#6c757d,#495057)";

    }

});
    
// Fecha

inputFecha.addEventListener("input", () => {

    let valor = inputFecha.value;

    valor = valor.replace(/\D/g, "");

    valor = valor.substring(0,4);

    if (valor.length > 2) {

        valor =
            valor.substring(0,2)
            + "/"
            + valor.substring(2);

    }

    inputFecha.value = valor;

    if (valor === "") {

        previewFecha.textContent = "MM/AA";

    } else {

        previewFecha.textContent = valor;

    }

});

// ==========================
// CVV
// ==========================

// Girar la tarjeta cuando entra al CVV

inputCVV.addEventListener("focus", () => {

    tarjetaVisual.classList.add("girada");

});


// Volver al frente
inputCVV.addEventListener("blur", () => {

    tarjetaVisual.classList.remove("girada");

    previewCVV.textContent = "***";

});


// Actualizar CVV
inputCVV.addEventListener("input", () => {

    let valor = inputCVV.value;

    valor = valor.replace(/\D/g, "");

    const numeroTarjeta = inputNumero.value.replace(/\s/g, "");

    const limiteCVV = numeroTarjeta.startsWith("3") ? 4 : 3;

    valor = valor.substring(0, limiteCVV);

    inputCVV.value = valor;

    if(valor === ""){

        previewCVV.textContent = "***";

    }else{

        previewCVV.textContent = valor;

    }

});

// ==========================
// OCULTAR NÚMERO
// ==========================

inputNumero.addEventListener("blur", () => {

    const numero = inputNumero.value.replace(/\s/g, "");

    if(numero.length === 16){

        previewNumero.textContent =
            numero.substring(0,4)
            + " •••• •••• "
            + numero.substring(12);

    }

});

inputNumero.addEventListener("focus", () => {

    if(inputNumero.value !== ""){

        previewNumero.textContent =
            inputNumero.value;

    }

});

// ==========================
// RESUMEN DEL PAGO
// ==========================
const btnConfirmar = document.getElementById("btn-confirmar");

if (btnConfirmar) {

    btnConfirmar.addEventListener(
        "click",
        confirmarCompra
    );
}
});

async function confirmarCompra(event) {

    event.preventDefault();

    const metodoSeleccionado = document.querySelector(
        'input[name="metodo"]:checked'
    );

    if (!metodoSeleccionado) {

        alert("Seleccione un método de pago.");

        return;

    }

    const datosCheckout = JSON.parse(
        sessionStorage.getItem("checkout")
    );

    if (!datosCheckout) {

        alert("No existen datos del checkout.");

        return;

    }

    const datos = {

        cliente_id: obtenerClienteId(),
        destinatario: datosCheckout.destinatario,
        direccion: datosCheckout.direccion,
        metodo_pago: metodoSeleccionado.value,
        observacion: datosCheckout.observacion

    };

    try {

        const respuesta = await fetch(
            "/compras/confirmar",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(datos)
            }
        );

        const resultado = await respuesta.json();

        if (!respuesta.ok) {

            alert(resultado.detail);

            return;

        }

        sessionStorage.removeItem("checkout");

        window.location.href = "/cliente/historial";

    } catch (error) {

        console.error(error);

        alert("Error al confirmar la compra.");

    }

}

async function cargarResumenPago(clienteId) {

    try {

        const respuesta = await fetch(`/carrito/${clienteId}`);

        if (!respuesta.ok) {
            throw new Error("No se pudo obtener el carrito.");
        }

        const carrito = await respuesta.json();

        renderResumenPago(carrito);

        actualizarResumenPago(carrito);

    } catch (error) {

        console.error(error);

    }

}

function renderResumenPago(carrito) {

    const contenedor = document.getElementById("lista-pago");

    if (!contenedor) return;

    let html = "";

    carrito.items.forEach(producto => {

        html += `
            <div class="item-pago">

                <span>${producto.nombre}</span>

                <span>x${producto.cantidad}</span>

                <strong>$${producto.subtotal.toLocaleString()}</strong>

            </div>
        `;

    });

    contenedor.innerHTML = html;

}

function actualizarResumenPago(carrito) {

    document.getElementById("cantidad-productos").textContent =
        carrito.total_productos;

    document.getElementById("subtotal").textContent =
        `$${carrito.total.toLocaleString()}`;

    document.getElementById("total").textContent =
        `$${carrito.total.toLocaleString()}`;

}

verificarSesion();