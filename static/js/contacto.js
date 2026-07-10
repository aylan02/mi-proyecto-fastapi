const btnEnviar = document.getElementById("btn-enviar");

btnEnviar.addEventListener("click", () => {

    const nombre = document.getElementById("nombre").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const mensaje = document.getElementById("mensaje").value.trim();

    if (!nombre || !correo || !mensaje) {

        alert("Complete todos los campos.");

        return;

    }

    alert("Mensaje enviado correctamente. Nos pondremos en contacto contigo pronto.");

    document.getElementById("nombre").value = "";
    document.getElementById("correo").value = "";
    document.getElementById("mensaje").value = "";

});

verificarSesion();