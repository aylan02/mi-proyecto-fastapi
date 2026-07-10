verificarSesion();

const btnLogout = document.getElementById("btn-logout");

btnLogout.addEventListener("click", async () => {

    try {

        await fetch("/auth/logout", {
            method: "POST"
        });

        window.location.href = "/";

    } catch (error) {

        console.error(error);

        alert("No fue posible cerrar la sesión.");

    }

});

async function cargarPerfil() {

    try {

        const respuesta = await fetch("/api/cliente/perfil");

        if (!respuesta.ok) {

            throw new Error("No fue posible obtener el perfil.");

        }

        const cliente = await respuesta.json();

        document.getElementById("nombre").value = cliente.nombre || "";

        document.getElementById("apellido").value = cliente.apellido || "";

        document.getElementById("correo").value = cliente.correo || "";

        document.getElementById("username").value = cliente.username || "";

        document.getElementById("telefono").value = cliente.telefono || "";

        document.getElementById("direccion").value = cliente.direccion || "";

    } catch (error) {

        console.error(error);

    }

}

cargarPerfil();

const formulario = document.getElementById("perfil-form");

formulario.addEventListener("submit", async (e) => {

    e.preventDefault();

    const datos = {

        nombre: document.getElementById("nombre").value,

        apellido: document.getElementById("apellido").value,

        correo: document.getElementById("correo").value,

        telefono: document.getElementById("telefono").value,

        direccion: document.getElementById("direccion").value

    };

    try {

        const respuesta = await fetch("/api/cliente/perfil", {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(datos)

        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {

            throw new Error(resultado.detail);

        }

        alert(resultado.mensaje);

    } catch (error) {

        console.error(error);

        alert(error.message);

    }

});