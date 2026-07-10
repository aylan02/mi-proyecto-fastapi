document.getElementById("login-form").addEventListener("submit", async (e) => {

    e.preventDefault();

    const username = document.getElementById("username").value.trim();

    const password = document.getElementById("password").value.trim();

    const errorBox = document.getElementById("error");

    const esLoginCliente =
        window.location.pathname === "/cliente/login";

    const endpoint = esLoginCliente
        ? "/auth-cliente/login"
        : "/auth/login";

    const respuesta = await fetch(endpoint, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            username,
            password
        })

    });

    const resultado = await respuesta.json();

    if (!respuesta.ok) {

        errorBox.style.display = "block";

        errorBox.textContent =
            resultado.detail || "Usuario o contraseña incorrectos.";

        return;

    }

    if (esLoginCliente) {

        window.location.href = "/cliente/catalogo";

    } else {

        window.location.href = "/admin";

    }

});