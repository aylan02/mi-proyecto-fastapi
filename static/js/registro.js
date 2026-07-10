document.getElementById("registro-form").addEventListener("submit", async (e) => {

    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const confirmar = document.getElementById("confirmar_password").value;

    const errorBox = document.getElementById("error");

    errorBox.style.display = "none";
    errorBox.textContent = "";

    if (password !== confirmar) {

        errorBox.style.display = "block";
        errorBox.textContent = "Las contraseñas no coinciden.";

        return;
    }

    try {

        const respuesta = await fetch("/auth-cliente/registro", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                nombre,
                apellido,
                correo,
                username,
                password,
                confirmar_password: confirmar
            })

        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {

            errorBox.style.display = "block";
           if (Array.isArray(resultado.detail)) {

                errorBox.textContent = resultado.detail
                    .map(error => error.msg)
                    .join(" | ");

            } else {

                errorBox.textContent =
                    resultado.detail || "No fue posible crear la cuenta.";

            }

            return;
        }

        alert("¡Cuenta creada correctamente! Ahora puedes iniciar sesión.");
        window.location.href = "/cliente/login";

    } catch (error) {

        errorBox.style.display = "block";
        errorBox.textContent =
            "No fue posible conectar con el servidor.";

    }
});