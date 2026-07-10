async function verificarSesion() {

    const btnLogin = document.getElementById("btn-login");
    const btnCuenta = document.getElementById("btn-cuenta");

    if (!btnLogin || !btnCuenta) return;

    try {

        const respuesta = await fetch("/auth/me");

        if (!respuesta.ok) {

            btnLogin.style.display = "inline-block";
            btnCuenta.style.display = "none";

            return;
        }

        const datos = await respuesta.json();

        btnLogin.style.display = "none";
        btnCuenta.style.display = "inline-block";

        btnCuenta.textContent = `👤 ${datos.user.nombre}`;

    } catch (error) {

        console.error(error);

    }

}

verificarSesion();