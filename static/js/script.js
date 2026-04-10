const API = window.location.origin;

document.addEventListener("DOMContentLoaded", () => {
    conectarEventos();
    iniciarVista();
});

function conectarEventos() {
    document.getElementById("form-producto").addEventListener("submit", guardarProducto);
    document.getElementById("form-envio").addEventListener("submit", guardarEnvio);

    document.getElementById("btn-filtrar-productos").addEventListener("click", cargarProductos);
    document.getElementById("btn-limpiar-filtros").addEventListener("click", limpiarFiltrosProductos);

    document.getElementById("btn-recargar-productos").addEventListener("click", cargarProductos);
    document.getElementById("btn-recargar-envios").addEventListener("click", cargarEnvios);
    document.getElementById("btn-recargar-resumen").addEventListener("click", cargarResumen);

    document.getElementById("btn-nuevo-producto").addEventListener("click", resetFormProducto);
    document.getElementById("btn-cancelar-producto").addEventListener("click", resetFormProducto);

    document.getElementById("btn-nuevo-envio").addEventListener("click", resetFormEnvio);
    document.getElementById("btn-cancelar-envio").addEventListener("click", resetFormEnvio);
}

async function iniciarVista() {
    await Promise.all([
        cargarResumen(),
        cargarProductos(),
        cargarEnvios()
    ]);
}

function mostrarMensaje(texto, tipo = "success") {
    const box = document.getElementById("mensaje-global");
    box.textContent = texto;
    box.className = `alert alert-${tipo}`;
    box.classList.remove("hidden");

    setTimeout(() => {
        box.classList.add("hidden");
    }, 3500);
}

function formatearPrecio(valor) {
    return `$${Number(valor).toLocaleString("es-CL")}`;
}

function formatearFecha(valor) {
    if (!valor) return "-";
    return valor;
}

function normalizarEstado(estado) {
    if (!estado) return "registrado";
    return estado.toLowerCase().replaceAll("_", " ").trim();
}

function claseEstado(estado) {
    const limpio = normalizarEstado(estado);
    if (limpio === "registrado") return "badge badge-registrado";
    if (limpio === "en camino") return "badge badge-en-camino";
    if (limpio === "entregado") return "badge badge-entregado";
    return "badge badge-default";
}

function limpiarFiltrosProductos() {
    document.getElementById("filtro-nombre").value = "";
    document.getElementById("filtro-categoria").value = "";
    document.getElementById("filtro-marca").value = "";
    document.getElementById("filtro-ordenar").value = "";
    document.getElementById("filtro-stock").checked = false;
    cargarProductos();
}

function resetFormProducto() {
    document.getElementById("form-producto").reset();
    document.getElementById("producto-edit-id").value = "";
    document.getElementById("titulo-form-producto").textContent = "Agregar producto";
    document.getElementById("btn-guardar-producto").textContent = "Guardar producto";
}

function resetFormEnvio() {
    document.getElementById("form-envio").reset();
    document.getElementById("envio-edit-id").value = "";
    document.getElementById("titulo-form-envio").textContent = "Registrar envío";
    document.getElementById("btn-guardar-envio").textContent = "Registrar envío";
}

async function cargarResumen() {
    try {
        const [productosRes, stockBajoRes, enviosRes] = await Promise.all([
            fetch(`${API}/productos?limit=100&offset=0`),
            fetch(`${API}/productos/stock/bajo`),
            fetch(`${API}/envios`)
        ]);

        const productosData = await productosRes.json();
        const stockBajoData = await stockBajoRes.json();
        const enviosData = await enviosRes.json();

        const productos = Array.isArray(productosData) ? productosData : (productosData.resultados ?? []);
        const envios = Array.isArray(enviosData) ? enviosData : [];

        document.getElementById("stat-total-productos").textContent =
            Array.isArray(productosData) ? productos.length : (productosData.total ?? productos.length);

        document.getElementById("stat-stock-bajo").textContent = stockBajoData.length;
        document.getElementById("stat-total-envios").textContent = envios.length;
        document.getElementById("stat-entregados").textContent =
            envios.filter(e => normalizarEstado(e.estado) === "entregado").length;

    } catch (error) {
        mostrarMensaje("No se pudo cargar el resumen.", "error");
    }
}

async function cargarProductos() {
    const tbody = document.getElementById("tbody-productos");
    tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Cargando productos...</td></tr>`;

    const nombre = document.getElementById("filtro-nombre").value.trim();
    const categoria = document.getElementById("filtro-categoria").value.trim();
    const marca = document.getElementById("filtro-marca").value.trim();
    const ordenar = document.getElementById("filtro-ordenar").value;
    const stock = document.getElementById("filtro-stock").checked;

    const params = new URLSearchParams();
    params.append("limit", "100");
    params.append("offset", "0");

    if (nombre) params.append("nombre", nombre);
    if (categoria) params.append("categoria", categoria);
    if (marca) params.append("marca", marca);
    if (ordenar) params.append("ordenar_precio", ordenar);
    if (stock) params.append("stock_disponible", "true");

    try {
        const response = await fetch(`${API}/productos?${params.toString()}`);
        const data = await response.json();

        const productos = Array.isArray(data) ? data : (data.resultados ?? []);
        const total = Array.isArray(data) ? data.length : (data.total ?? productos.length);

        document.getElementById("texto-total-productos").textContent = `${total} resultados`;

        if (!productos.length) {
            tbody.innerHTML = `<tr><td colspan="7" class="empty-row">No hay productos para mostrar.</td></tr>`;
            return;
        }

        tbody.innerHTML = productos.map(producto => `
            <tr>
                <td>${producto.id}</td>
                <td>
                    <strong>${producto.nombre}</strong><br>
                    <span class="mini-note">${producto.descripcion ?? ""}</span>
                </td>
                <td>${producto.marca}</td>
                <td>${producto.categoria}</td>
                <td>${formatearPrecio(producto.precio)}</td>
                <td>${producto.stock}</td>
                <td>
                    <div class="actions">
                        <button class="btn btn-light btn-sm" onclick="editarProducto(${producto.id})">Editar</button>
                        <button class="btn btn-danger btn-sm" onclick="eliminarProducto(${producto.id})">Eliminar</button>
                    </div>
                </td>
            </tr>
        `).join("");

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Error al cargar productos.</td></tr>`;
    }
}

async function guardarProducto(event) {
    event.preventDefault();

    const id = document.getElementById("producto-edit-id").value;

    const producto = {
        nombre: document.getElementById("nombre").value.trim(),
        marca: document.getElementById("marca").value.trim(),
        categoria: document.getElementById("categoria").value.trim(),
        precio: Number(document.getElementById("precio").value),
        stock: Number(document.getElementById("stock").value),
        descripcion: document.getElementById("descripcion").value.trim()
    };

    try {
        const url = id ? `${API}/productos/${id}` : `${API}/productos`;
        const method = id ? "PUT" : "POST";

        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(producto)
        });

        const data = await response.json();

        if (!response.ok) {
            mostrarMensaje(data.detail || "Error al guardar producto.", "error");
            return;
        }

        mostrarMensaje(id ? "Producto actualizado correctamente." : "Producto agregado correctamente.");
        resetFormProducto();
        await cargarProductos();
        await cargarResumen();

    } catch (error) {
        mostrarMensaje("Error de conexión al guardar producto.", "error");
    }
}

async function editarProducto(id) {
    try {
        const response = await fetch(`${API}/productos/${id}`);
        const producto = await response.json();

        if (!response.ok) {
            mostrarMensaje(producto.detail || "No se pudo cargar el producto.", "error");
            return;
        }

        document.getElementById("producto-edit-id").value = producto.id;
        document.getElementById("nombre").value = producto.nombre;
        document.getElementById("marca").value = producto.marca;
        document.getElementById("categoria").value = producto.categoria;
        document.getElementById("precio").value = producto.precio;
        document.getElementById("stock").value = producto.stock;
        document.getElementById("descripcion").value = producto.descripcion;

        document.getElementById("titulo-form-producto").textContent = "Editar producto";
        document.getElementById("btn-guardar-producto").textContent = "Actualizar producto";
        window.scrollTo({ top: document.getElementById("productos").offsetTop - 20, behavior: "smooth" });

    } catch (error) {
        mostrarMensaje("Error al cargar el producto para edición.", "error");
    }
}

async function eliminarProducto(id) {
    const confirmar = confirm(`¿Seguro que quieres eliminar el producto ${id}?`);
    if (!confirmar) return;

    try {
        const response = await fetch(`${API}/productos/${id}`, { method: "DELETE" });
        const data = await response.json();

        if (!response.ok) {
            mostrarMensaje(data.detail || "No se pudo eliminar el producto.", "error");
            return;
        }

        mostrarMensaje("Producto eliminado correctamente.");
        await cargarProductos();
        await cargarResumen();

    } catch (error) {
        mostrarMensaje("Error de conexión al eliminar producto.", "error");
    }
}

async function cargarEnvios() {
    const tbody = document.getElementById("tbody-envios");
    tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Cargando envíos...</td></tr>`;

    try {
        const response = await fetch(`${API}/envios`);
        const envios = await response.json();

        document.getElementById("texto-total-envios").textContent = `${envios.length} envíos`;

        if (!envios.length) {
            tbody.innerHTML = `<tr><td colspan="7" class="empty-row">No hay envíos registrados.</td></tr>`;
            return;
        }

        tbody.innerHTML = envios.map(envio => `
            <tr>
                <td>${envio.id_envio ?? "-"}</td>
                <td>${envio.nombre_producto ?? "-"}</td>
                <td>${envio.cantidad}</td>
                <td>${envio.destinatario}</td>
                <td>
                    <div class="estado-box">
                        <span class="${claseEstado(envio.estado)}">${normalizarEstado(envio.estado)}</span>
                        <select id="estado-${envio.id_envio}">
                            <option value="registrado" ${normalizarEstado(envio.estado) === "registrado" ? "selected" : ""}>registrado</option>
                            <option value="en camino" ${normalizarEstado(envio.estado) === "en camino" ? "selected" : ""}>en camino</option>
                            <option value="entregado" ${normalizarEstado(envio.estado) === "entregado" ? "selected" : ""}>entregado</option>
                        </select>
                        <button class="btn btn-light btn-sm" onclick="actualizarEstadoEnvio(${envio.id_envio})">Estado</button>
                    </div>
                </td>
                <td>${formatearFecha(envio.fecha_envio || envio.fecha)}</td>
                <td>
                    <div class="actions">
                        <button class="btn btn-light btn-sm" onclick="editarEnvio(${envio.id_envio})">Editar</button>
                        <button class="btn btn-danger btn-sm" onclick="eliminarEnvio(${envio.id_envio})">Eliminar</button>
                    </div>
                </td>
            </tr>
        `).join("");

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Error al cargar envíos.</td></tr>`;
    }
}

async function guardarEnvio(event) {
    event.preventDefault();

    const id = document.getElementById("envio-edit-id").value;

    const envio = {
        producto_id: Number(document.getElementById("producto_id").value),
        cantidad: Number(document.getElementById("cantidad").value),
        destinatario: document.getElementById("destinatario").value.trim(),
        direccion: document.getElementById("direccion").value.trim(),
        observacion: document.getElementById("observacion").value.trim() || null
    };

    try {
        const url = id ? `${API}/envios/${id}` : `${API}/envios`;
        const method = id ? "PUT" : "POST";

        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(envio)
        });

        const data = await response.json();

        if (!response.ok) {
            mostrarMensaje(data.detail || "Error al registrar el envío.", "error");
            return;
        }

        mostrarMensaje(id ? "Envío actualizado correctamente." : "Envío registrado correctamente.");
        resetFormEnvio();
        await cargarEnvios();
        await cargarProductos();
        await cargarResumen();

    } catch (error) {
        mostrarMensaje("Error de conexión al guardar envío.", "error");
    }
}

async function editarEnvio(id) {
    try {
        const response = await fetch(`${API}/envios/${id}`);
        const envio = await response.json();

        if (!response.ok) {
            mostrarMensaje(envio.detail || "No se pudo cargar el envío.", "error");
            return;
        }

        document.getElementById("envio-edit-id").value = envio.id_envio;
        document.getElementById("producto_id").value = envio.producto_id;
        document.getElementById("cantidad").value = envio.cantidad;
        document.getElementById("destinatario").value = envio.destinatario;
        document.getElementById("direccion").value = envio.direccion;
        document.getElementById("observacion").value = envio.observacion ?? "";

        document.getElementById("titulo-form-envio").textContent = "Editar envío";
        document.getElementById("btn-guardar-envio").textContent = "Actualizar envío";
        window.scrollTo({ top: document.getElementById("envios").offsetTop - 20, behavior: "smooth" });

    } catch (error) {
        mostrarMensaje("Error al cargar el envío para edición.", "error");
    }
}

async function eliminarEnvio(id) {
    const confirmar = confirm(`¿Seguro que quieres eliminar el envío ${id}?`);
    if (!confirmar) return;

    try {
        const response = await fetch(`${API}/envios/${id}`, { method: "DELETE" });
        const data = await response.json();

        if (!response.ok) {
            mostrarMensaje(data.detail || "No se pudo eliminar el envío.", "error");
            return;
        }

        mostrarMensaje("Envío eliminado correctamente.");
        await cargarEnvios();
        await cargarProductos();
        await cargarResumen();

    } catch (error) {
        mostrarMensaje("Error de conexión al eliminar envío.", "error");
    }
}

async function actualizarEstadoEnvio(id) {
    const select = document.getElementById(`estado-${id}`);
    const estado = select.value;

    try {
        const response = await fetch(`${API}/envios/${id}/estado`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ estado })
        });

        const data = await response.json();

        if (!response.ok) {
            mostrarMensaje(data.detail || "No se pudo actualizar el estado.", "error");
            return;
        }

        mostrarMensaje("Estado del envío actualizado correctamente.");
        await cargarEnvios();
        await cargarResumen();

    } catch (error) {
        mostrarMensaje("Error de conexión al actualizar estado.", "error");
    }
}