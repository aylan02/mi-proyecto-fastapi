const API = window.location.origin;

const STORAGE_KEYS = {
    clientes: "cosmelogix_clientes",
    ventas: "cosmelogix_ventas",
    rutas: "cosmelogix_rutas",
    usuarios: "cosmelogix_usuarios",
    roles: "cosmelogix_roles",
    movimientos: "cosmelogix_movimientos",
    envios_meta: "cosmelogix_envios_meta"
};

const state = {
    productos: [],
    envios: [],
    clientes: [],
    ventas: [],
    rutas: [],
    usuarios: [],
    roles: [],
    movimientos: [],
    enviosMeta: []
};

document.addEventListener("DOMContentLoaded", async () => {
    bindNavigation();
    showSection("dashboard");

    try {
        initLocalData();
        initEvents();
        await loadRemoteData();
        renderAll();
    } catch (error) {
        console.error("Error al iniciar la aplicación:", error);
        showAlert("La página cargó con errores. Revisa la consola del navegador.", "error");
    }
});

function bindNavigation() {
    const titles = {
        dashboard: ["Dashboard", "Panel general del sistema CosmeLogix."],
        productos: ["Productos", "Administración de catálogo y control comercial."],
        inventario: ["Inventario", "Entradas, salidas, ajustes y stock crítico."],
        clientes: ["Clientes", "Gestión comercial y perfil de compradores."],
        ventas: ["Ventas", "Registro de ventas y trazabilidad comercial."],
        envios: ["Envíos", "Coordinación logística y seguimiento de despachos."],
        rutas: ["Rutas", "Planificación básica de recorridos de distribución."],
        usuarios: ["Usuarios", "Administración de cuentas del sistema."],
        roles: ["Roles y permisos", "Control de acceso y privilegios."],
        reportes: ["Reportes", "Información administrativa y operacional."],
        seguimiento: ["Seguimiento", "Consulta del estado actual de pedidos/envíos."]
    };

    document.querySelectorAll(".nav-link").forEach(button => {
        button.addEventListener("click", () => {
            const target = button.dataset.section;
            showSection(target);
            document.getElementById("page-title").textContent = titles[target][0];
            document.getElementById("page-subtitle").textContent = titles[target][1];
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    });
}

function showSection(name) {
    document.querySelectorAll(".nav-link").forEach(n => n.classList.remove("active"));
    document.querySelector(`.nav-link[data-section="${name}"]`)?.classList.add("active");

    document.querySelectorAll(".page-section").forEach(section => section.classList.remove("active"));
    document.getElementById(`section-${name}`)?.classList.add("active");
}

function initLocalData() {
    state.clientes = [];

    state.ventas = [];
    state.rutas = readStorage(STORAGE_KEYS.rutas, [
        { id: 1, origen: "Bodega Central", destino: "Iquique Centro", distancia: "12 km", estado: "Activa" },
        { id: 2, origen: "Bodega Central", destino: "Alto Hospicio", distancia: "18 km", estado: "Activa" }
    ]);

    state.roles = readStorage(STORAGE_KEYS.roles, [
        {
            id: 1,
            nombre: "Administrador",
            descripcion: "Control total del sistema",
            estado: "Activo",
            permisos: ["productos", "inventario", "clientes", "ventas", "envios", "reportes", "usuarios"]
        },
        {
            id: 2,
            nombre: "Ejecutivo Comercial",
            descripcion: "Ventas y clientes",
            estado: "Activo",
            permisos: ["clientes", "ventas", "reportes"]
        },
        {
            id: 3,
            nombre: "Encargado de Inventario",
            descripcion: "Control de stock",
            estado: "Activo",
            permisos: ["productos", "inventario"]
        },
        {
            id: 4,
            nombre: "Coordinador Logístico",
            descripcion: "Despachos y seguimiento",
            estado: "Activo",
            permisos: ["envios", "reportes"]
        }
    ]);

    state.usuarios = readStorage(STORAGE_KEYS.usuarios, [
        {
            id: 1,
            username: "admin",
            nombre: "Administrador General",
            correo: "admin@cosmelogix.cl",
            password: "1234",
            rol: "Administrador",
            estado: "Activo"
        },
        {
            id: 2,
            username: "ejecutivo",
            nombre: "Ejecutivo Comercial",
            correo: "ventas@cosmelogix.cl",
            password: "1234",
            rol: "Ejecutivo Comercial",
            estado: "Activo"
        }
    ]);

    state.movimientos = readStorage(STORAGE_KEYS.movimientos, []);
    state.enviosMeta = readStorage(STORAGE_KEYS.envios_meta, []);
}

function readStorage(key, fallback) {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
}

function saveStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

async function loadRemoteData() {
    await Promise.all([loadProductos(), loadEnvios(), loadClientes(), loadVentas()]);
}

async function loadProductos() {
    try {
        const res = await fetch(`${API}/productos?limit=100&offset=0`);
        const data = await res.json();
        state.productos = Array.isArray(data) ? data : (data.resultados ?? []);
    } catch (error) {
        state.productos = [];
        showAlert("No se pudieron cargar los productos desde la API.", "error");
    }
}

async function loadEnvios() {
    try {
        const res = await fetch(`${API}/envios`);
        const data = await res.json();
        state.envios = Array.isArray(data) ? data : [];
    } catch (error) {
        state.envios = [];
        showAlert("No se pudieron cargar los envíos desde la API.", "error");
    }
}

async function loadClientes() {
    try {
        const res = await fetch(`${API}/clientes`);
        const data = await res.json();
        state.clientes = Array.isArray(data) ? data : [];
    } catch (error) {
        state.clientes = [];
        showAlert("No se pudieron cargar los clientes desde la API.", "error");
    }
}

async function loadVentas() {
    try {
        const res = await fetch(`${API}/ventas`);
        const data = await res.json();
        state.ventas = Array.isArray(data) ? data : [];
    } catch (error) {
        state.ventas = [];
        showAlert("No se pudieron cargar las ventas desde la API.", "error");
    }
}

function initEvents() {
    document.getElementById("btn-refresh-dashboard").addEventListener("click", async () => {
        await loadRemoteData();
        renderDashboard();
        renderReportes();
    });

    document.getElementById("btn-refresh-productos").addEventListener("click", async () => {
        await loadProductos();
        renderProductos();
        renderInventario();
        renderVentas();
        renderDashboard();
        renderReportes();
    });

    document.getElementById("btn-refresh-inventario").addEventListener("click", async () => {
        await loadProductos();
        renderInventario();
        renderDashboard();
        renderReportes();
    });

    document.getElementById("btn-refresh-clientes").addEventListener("click", async () => {
        await loadClientes();
        renderClientes();
        renderVentas();
        renderDashboard();
        renderReportes();
    });

    document.getElementById("btn-refresh-ventas").addEventListener("click", async () => {
        await loadVentas();
        renderVentas();
        renderDashboard();
        renderReportes();
        renderEnvioVentaOptions();
    });

    document.getElementById("btn-refresh-envios").addEventListener("click", async () => {
        await loadEnvios();
        renderEnvios();
        renderDashboard();
        renderReportes();
    });

    document.getElementById("btn-refresh-reportes").addEventListener("click", renderReportes);

    document.getElementById("btn-reset-producto").addEventListener("click", resetProductoForm);
    document.getElementById("btn-cancel-producto").addEventListener("click", resetProductoForm);
    document.getElementById("btn-limpiar-filtros-producto").addEventListener("click", limpiarFiltrosProductos);
    document.getElementById("btn-buscar-productos").addEventListener("click", renderProductos);

    document.getElementById("form-producto").addEventListener("submit", submitProducto);
    document.getElementById("form-ingreso").addEventListener("submit", submitIngresoInventario);
    document.getElementById("form-salida").addEventListener("submit", submitSalidaInventario);
    document.getElementById("form-ajuste").addEventListener("submit", submitAjusteInventario);

    document.getElementById("form-cliente").addEventListener("submit", submitCliente);
    document.getElementById("btn-reset-cliente").addEventListener("click", resetClienteForm);
    document.getElementById("btn-cancel-cliente").addEventListener("click", resetClienteForm);

    document.getElementById("form-venta").addEventListener("submit", submitVenta);
    document.getElementById("venta-producto").addEventListener("change", updateVentaResumen);
    document.getElementById("venta-cliente").addEventListener("change", updateVentaResumen);
    document.getElementById("venta-cantidad").addEventListener("input", updateVentaResumen);

    document.getElementById("form-envio").addEventListener("submit", submitEnvio);

    document.getElementById("form-ruta").addEventListener("submit", submitRuta);
    document.getElementById("form-usuario").addEventListener("submit", submitUsuario);
    document.getElementById("form-rol").addEventListener("submit", submitRol);

    document.getElementById("form-tracking").addEventListener("submit", submitTracking);
}

function renderAll() {
    renderDashboard();
    renderProductos();
    renderInventario();
    renderClientes();
    renderVentas();
    renderEnvios();
    renderRutas();
    renderUsuarios();
    renderRoles();
    renderPermisos();
    renderReportes();
}

function showAlert(text, type = "success") {
    const box = document.getElementById("global-alert");
    box.textContent = text;
    box.className = `alert alert-${type}`;
    box.classList.remove("hidden");
    setTimeout(() => box.classList.add("hidden"), 3000);
}

function currency(value) {
    return `$${Number(value || 0).toLocaleString("es-CL")}`;
}

function ventaProductosTexto(venta) {
    if (!venta.detalles || !Array.isArray(venta.detalles)) return "-";
    return venta.detalles.map(d => d.producto_nombre).join(", ");
}

function ventaCantidadTotal(venta) {
    if (!venta.detalles || !Array.isArray(venta.detalles)) return 0;
    return venta.detalles.reduce((acc, d) => acc + Number(d.cantidad || 0), 0);
}

function todayDate() {
    return new Date().toISOString().split("T")[0];
}

function codeFromProduct(producto) {
    return producto.codigo || `COSM-${String(producto.id).padStart(3, "0")}`;
}

function badgeEstadoHTML(estado) {
    const normalized = (estado || "").toString().toLowerCase().trim();

    if (["activo", "activa", "entregado"].includes(normalized)) {
        return `<span class="badge badge-activo">${estado}</span>`;
    }
    if (["inactivo", "inactiva", "cancelado"].includes(normalized)) {
        return `<span class="badge badge-inactivo">${estado}</span>`;
    }
    if (["bajo", "en preparación"].includes(normalized)) {
        return `<span class="badge badge-bajo">${estado}</span>`;
    }
    if (["crítico", "pendiente"].includes(normalized)) {
        return `<span class="badge badge-critico">${estado}</span>`;
    }
    if (["despachado", "en tránsito"].includes(normalized)) {
        return `<span class="badge badge-transito">${estado}</span>`;
    }

    return `<span class="badge badge-critico">${estado || "Pendiente"}</span>`;
}

function productStockLabel(stock) {
    if (stock <= 3) return "Crítico";
    if (stock <= 8) return "Bajo";
    return "Activo";
}

function renderDashboard() {
    document.getElementById("card-total-productos").textContent = state.productos.length;
    document.getElementById("card-stock-bajo").textContent = state.productos.filter(p => p.stock <= 8).length;
    document.getElementById("card-total-clientes").textContent = state.clientes.length;
    document.getElementById("card-total-ventas").textContent = state.ventas.length;
    document.getElementById("card-total-envios").textContent = state.envios.length;

    document.getElementById("dashboard-productos").innerHTML = state.productos.slice(0, 5).map(p => `
        <div class="list-item">
            <strong>${p.nombre}</strong>
            <div class="mini-note">${codeFromProduct(p)} • ${p.marca} • Stock: ${p.stock}</div>
        </div>
    `).join("") || `<div class="empty-state">No hay productos cargados.</div>`;

    document.getElementById("dashboard-ventas").innerHTML = state.ventas.slice(-5).reverse().map(v => `
        <div class="list-item">
            <strong>Venta #${v.id}</strong>
            <div class="mini-note">${v.cliente_nombre} • ${ventaProductosTexto(v)} • ${currency(v.total)}</div>
        </div>
    `).join("") || `<div class="empty-state">No hay ventas registradas.</div>`;

    document.getElementById("dashboard-envios").innerHTML = state.envios.slice(-5).reverse().map(e => `
        <div class="list-item">
            <strong>Envío #${e.id_envio ?? "-"}</strong>
            <div class="mini-note">${e.destinatario ?? "-"} • ${e.nombre_producto ?? "-"} • ${e.estado ?? "Pendiente"}</div>
        </div>
    `).join("") || `<div class="empty-state">No hay envíos registrados.</div>`;
}

function renderProductos() {
    populateProductSelects();

    const nombre = document.getElementById("filtro-producto-nombre").value.trim().toLowerCase();
    const marca = document.getElementById("filtro-producto-marca").value.trim().toLowerCase();
    const categoria = document.getElementById("filtro-producto-categoria").value.trim().toLowerCase();
    const orden = document.getElementById("filtro-producto-orden").value;
    const onlyStock = document.getElementById("filtro-stock-disponible").checked;

    let productos = [...state.productos];

    if (nombre) productos = productos.filter(p => p.nombre.toLowerCase().includes(nombre));
    if (marca) productos = productos.filter(p => p.marca.toLowerCase().includes(marca));
    if (categoria) productos = productos.filter(p => p.categoria.toLowerCase().includes(categoria));
    if (onlyStock) productos = productos.filter(p => p.stock > 0);

    if (orden === "asc") productos.sort((a, b) => a.precio - b.precio);
    if (orden === "desc") productos.sort((a, b) => b.precio - a.precio);

    document.getElementById("texto-total-productos").textContent = `${productos.length} resultados`;

    document.getElementById("tbody-productos").innerHTML = productos.map(p => `
        <tr>
            <td>${p.id}</td>
            <td>${codeFromProduct(p)}</td>
            <td><strong>${p.nombre}</strong><br><span class="mini-note">${p.descripcion ?? ""}</span></td>
            <td>${p.marca}</td>
            <td>${p.categoria}</td>
            <td>${currency(p.precio)}</td>
            <td>${p.stock}</td>
            <td>${badgeEstadoHTML(productStockLabel(p.stock))}</td>
            <td>
                <div class="actions">
                    <button class="btn btn-light btn-sm" onclick="editProducto(${p.id})">Editar</button>
                    <button class="btn btn-light btn-sm" onclick="softDeactivateProducto(${p.id})">Desactivar</button>
                </div>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="9" class="mini-note">No hay productos para mostrar.</td></tr>`;
}

function populateProductSelects() {
    const selects = ["ingreso-producto", "salida-producto", "ajuste-producto", "venta-producto"];
    selects.forEach(id => {
        const select = document.getElementById(id);
        const current = select.value;
        select.innerHTML = `<option value="">Selecciona un producto</option>` + state.productos.map(p => `
            <option value="${p.id}">${codeFromProduct(p)} - ${p.nombre} (stock: ${p.stock})</option>
        `).join("");
        if (current) select.value = current;
    });
}

async function submitProducto(event) {
    event.preventDefault();

    const editId = document.getElementById("producto-id-edit").value;
    const payload = {
        nombre: document.getElementById("producto-nombre").value.trim(),
        marca: document.getElementById("producto-marca").value.trim(),
        categoria: document.getElementById("producto-categoria").value.trim(),
        precio: Number(document.getElementById("producto-precio").value),
        stock: Number(document.getElementById("producto-stock").value),
        descripcion: document.getElementById("producto-descripcion").value.trim()
    };

    try {
        const url = editId ? `${API}/productos/${editId}` : `${API}/productos`;
        const method = editId ? "PUT" : "POST";

        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo guardar el producto.", "error");
            return;
        }

        showAlert(editId ? "Producto actualizado correctamente." : "Producto registrado correctamente.");
        resetProductoForm();
        await loadProductos();
        renderProductos();
        renderInventario();
        renderDashboard();
        renderVentas();
        renderReportes();
    } catch (error) {
        showAlert("Error de conexión al guardar producto.", "error");
    }
}

async function editProducto(id) {
    try {
        const res = await fetch(`${API}/productos/${id}`);
        const p = await res.json();

        if (!res.ok) {
            showAlert("No se pudo cargar el producto.", "error");
            return;
        }

        document.getElementById("producto-id-edit").value = p.id;
        document.getElementById("producto-codigo").value = codeFromProduct(p);
        document.getElementById("producto-nombre").value = p.nombre;
        document.getElementById("producto-marca").value = p.marca;
        document.getElementById("producto-categoria").value = p.categoria;
        document.getElementById("producto-precio").value = p.precio;
        document.getElementById("producto-stock").value = p.stock;
        document.getElementById("producto-descripcion").value = p.descripcion || "";
        document.getElementById("titulo-form-producto").textContent = "Actualizar producto";
        activateSection("productos");
    } catch (error) {
        showAlert("Error al cargar el producto.", "error");
    }
}

function softDeactivateProducto(id) {
    const producto = state.productos.find(p => p.id === id);
    if (!producto) return;
    showAlert(`La desactivación lógica del producto "${producto.nombre}" se implementará en backend después.`, "error");
}

function resetProductoForm() {
    document.getElementById("form-producto").reset();
    document.getElementById("producto-id-edit").value = "";
    document.getElementById("titulo-form-producto").textContent = "Registrar producto";
}

function limpiarFiltrosProductos() {
    document.getElementById("filtro-producto-nombre").value = "";
    document.getElementById("filtro-producto-marca").value = "";
    document.getElementById("filtro-producto-categoria").value = "";
    document.getElementById("filtro-producto-orden").value = "";
    document.getElementById("filtro-stock-disponible").checked = false;
    renderProductos();
}

async function submitIngresoInventario(event) {
    event.preventDefault();
    const productId = Number(document.getElementById("ingreso-producto").value);
    const cantidad = Number(document.getElementById("ingreso-cantidad").value);
    const documento = document.getElementById("ingreso-documento").value.trim();
    const proveedor = document.getElementById("ingreso-proveedor").value.trim();

    if (!productId || cantidad <= 0) {
        showAlert("Debes seleccionar producto y cantidad válida.", "error");
        return;
    }

    const producto = state.productos.find(p => p.id === productId);
    if (!producto) {
        showAlert("Producto no encontrado.", "error");
        return;
    }

    await updateProductStock(producto, producto.stock + cantidad);

    state.movimientos.unshift({
        fecha: new Date().toLocaleString(),
        tipo: "Ingreso",
        producto: producto.nombre,
        cantidad: `+${cantidad}`,
        detalle: `${documento || "Sin documento"} • ${proveedor || "Sin proveedor"}`
    });
    saveStorage(STORAGE_KEYS.movimientos, state.movimientos);

    event.target.reset();
    await loadProductos();
    renderInventario();
    renderProductos();
    renderDashboard();
    renderVentas();
    renderReportes();
    showAlert("Ingreso de inventario registrado correctamente.");
}

async function submitSalidaInventario(event) {
    event.preventDefault();
    const productId = Number(document.getElementById("salida-producto").value);
    const cantidad = Number(document.getElementById("salida-cantidad").value);
    const motivo = document.getElementById("salida-motivo").value;
    const observacion = document.getElementById("salida-observacion").value.trim();

    const producto = state.productos.find(p => p.id === productId);
    if (!producto || cantidad <= 0) {
        showAlert("Debes seleccionar un producto y cantidad válida.", "error");
        return;
    }

    if (cantidad > producto.stock) {
        showAlert("La salida supera el stock disponible.", "error");
        return;
    }

    await updateProductStock(producto, producto.stock - cantidad);

    state.movimientos.unshift({
        fecha: new Date().toLocaleString(),
        tipo: "Salida",
        producto: producto.nombre,
        cantidad: `-${cantidad}`,
        detalle: `${motivo} • ${observacion || "Sin observación"}`
    });
    saveStorage(STORAGE_KEYS.movimientos, state.movimientos);

    event.target.reset();
    await loadProductos();
    renderInventario();
    renderProductos();
    renderDashboard();
    renderVentas();
    renderReportes();
    showAlert("Salida de inventario registrada correctamente.");
}

async function submitAjusteInventario(event) {
    event.preventDefault();
    const productId = Number(document.getElementById("ajuste-producto").value);
    const stockReal = Number(document.getElementById("ajuste-real").value);
    const justificacion = document.getElementById("ajuste-justificacion").value.trim();

    const producto = state.productos.find(p => p.id === productId);
    if (!producto || stockReal < 0) {
        showAlert("Debes seleccionar un producto y un stock real válido.", "error");
        return;
    }

    const variacion = stockReal - producto.stock;
    await updateProductStock(producto, stockReal);

    state.movimientos.unshift({
        fecha: new Date().toLocaleString(),
        tipo: "Ajuste",
        producto: producto.nombre,
        cantidad: variacion >= 0 ? `+${variacion}` : `${variacion}`,
        detalle: justificacion || "Ajuste manual"
    });
    saveStorage(STORAGE_KEYS.movimientos, state.movimientos);

    event.target.reset();
    await loadProductos();
    renderInventario();
    renderProductos();
    renderDashboard();
    renderVentas();
    renderReportes();
    showAlert("Ajuste de inventario guardado correctamente.");
}

async function updateProductStock(producto, nuevoStock) {
    const payload = {
        nombre: producto.nombre,
        marca: producto.marca,
        categoria: producto.categoria,
        precio: Number(producto.precio),
        stock: Number(nuevoStock),
        descripcion: producto.descripcion || ""
    };

    const res = await fetch(`${API}/productos/${producto.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("No se pudo actualizar stock");
}

function renderInventario() {
    populateProductSelects();

    const totalStock = state.productos.reduce((acc, p) => acc + Number(p.stock || 0), 0);
    const stockCritico = state.productos.filter(p => p.stock <= 3).length;

    document.getElementById("inv-total-sku").textContent = state.productos.length;
    document.getElementById("inv-stock-total").textContent = totalStock;
    document.getElementById("inv-stock-critico").textContent = stockCritico;
    document.getElementById("inv-last-update").textContent = new Date().toLocaleDateString();

    document.getElementById("tbody-inventario").innerHTML = state.productos.map(p => `
        <tr>
            <td>${codeFromProduct(p)}</td>
            <td>${p.nombre}</td>
            <td>${p.stock}</td>
            <td>${badgeEstadoHTML(productStockLabel(p.stock))}</td>
        </tr>
    `).join("") || `<tr><td colspan="4" class="mini-note">No hay inventario disponible.</td></tr>`;

    const bajos = state.productos.filter(p => p.stock <= 8);
    document.getElementById("tbody-stock-bajo").innerHTML = bajos.map(p => `
        <tr>
            <td>${p.nombre}</td>
            <td>${p.stock}</td>
            <td>${badgeEstadoHTML(productStockLabel(p.stock))}</td>
        </tr>
    `).join("") || `<tr><td colspan="3" class="mini-note">No hay productos con stock bajo.</td></tr>`;

    document.getElementById("tbody-movimientos").innerHTML = state.movimientos.map(m => `
        <tr>
            <td>${m.fecha}</td>
            <td>${m.tipo}</td>
            <td>${m.producto}</td>
            <td>${m.cantidad}</td>
            <td>${m.detalle}</td>
        </tr>
    `).join("") || `<tr><td colspan="5" class="mini-note">No hay movimientos de inventario registrados.</td></tr>`;
}

async function submitCliente(event) {
    event.preventDefault();

    const editId = Number(document.getElementById("cliente-id-edit").value);

    const payload = {
        rut: document.getElementById("cliente-rut").value.trim(),
        nombre: document.getElementById("cliente-nombre").value.trim(),
        direccion: document.getElementById("cliente-direccion").value.trim(),
        correo: document.getElementById("cliente-correo").value.trim(),
        telefono: document.getElementById("cliente-telefono").value.trim(),
        estado: "Activo"
    };

    try {
        const url = editId ? `${API}/clientes/${editId}` : `${API}/clientes`;
        const method = editId ? "PUT" : "POST";

        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo guardar el cliente.", "error");
            return;
        }

        showAlert(editId ? "Cliente actualizado correctamente." : "Cliente registrado correctamente.");
        resetClienteForm();
        await loadClientes();
        renderClientes();
        renderVentas();
        renderDashboard();
        renderReportes();
    } catch (error) {
        showAlert("Error de conexión al guardar cliente.", "error");
    }
}

function renderClientes() {
    populateClienteSelect();
    document.getElementById("tbody-clientes").innerHTML = state.clientes.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.rut}</td>
            <td>${c.nombre}</td>
            <td>${c.direccion}</td>
            <td>${c.correo}</td>
            <td>${c.telefono}</td>
            <td>${badgeEstadoHTML(c.estado)}</td>
            <td>
                <div class="actions">
                    <button class="btn btn-light btn-sm" onclick="editCliente(${c.id})">Editar</button>
                    <button class="btn btn-light btn-sm" onclick="viewClientePerfil(${c.id})">Perfil</button>
                    <button class="btn btn-danger btn-sm" onclick="toggleClienteEstado(${c.id})">${c.estado === "Activo" ? "Desactivar" : "Activar"}</button>
                </div>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="8" class="mini-note">No hay clientes registrados.</td></tr>`;
}

function populateClienteSelect() {
    const select = document.getElementById("venta-cliente");
    const current = select.value;
    select.innerHTML = `<option value="">Selecciona un cliente</option>` + state.clientes
        .filter(c => c.estado === "Activo")
        .map(c => `<option value="${c.id}">${c.nombre}</option>`)
        .join("");
    if (current) select.value = current;
}

function viewClientePerfil(id) {
    const cliente = state.clientes.find(c => c.id === id);
    const ventas = state.ventas.filter(v => v.cliente_id === id);

    document.getElementById("cliente-perfil").innerHTML = `
        <strong>${cliente.nombre}</strong>
        <p class="mini-note">${cliente.rut} • ${cliente.correo} • ${cliente.telefono}</p>
        <p class="mini-note">${cliente.direccion}</p>
        <hr>
        <p><strong>Historial de ventas:</strong> ${ventas.length}</p>
        ${ventas.slice(-5).reverse().map(v => `
            <div class="list-item">
                <strong>Venta #${v.id}</strong>
                <div class="mini-note">${ventaProductosTexto(v)} • ${ventaCantidadTotal(v)} unidad(es) • ${currency(v.total)}</div>
            </div>
        `).join("") || `<div class="mini-note">Sin ventas registradas.</div>`}
    `;
}

function editCliente(id) {
    const c = state.clientes.find(x => x.id === id);
    document.getElementById("cliente-id-edit").value = c.id;
    document.getElementById("cliente-rut").value = c.rut;
    document.getElementById("cliente-nombre").value = c.nombre;
    document.getElementById("cliente-direccion").value = c.direccion;
    document.getElementById("cliente-correo").value = c.correo;
    document.getElementById("cliente-telefono").value = c.telefono;
    document.getElementById("titulo-form-cliente").textContent = "Actualizar cliente";
    activateSection("clientes");
}

async function toggleClienteEstado(id) {
    const cliente = state.clientes.find(c => c.id === id);
    if (!cliente) return;

    const nuevoEstado = cliente.estado === "Activo" ? "Inactivo" : "Activo";

    const payload = {
        rut: cliente.rut,
        nombre: cliente.nombre,
        direccion: cliente.direccion,
        correo: cliente.correo,
        telefono: cliente.telefono,
        estado: nuevoEstado
    };

    try {
        const res = await fetch(`${API}/clientes/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo cambiar el estado del cliente.", "error");
            return;
        }

        await loadClientes();
        renderClientes();
        renderVentas();
        renderDashboard();
        renderReportes();
        showAlert("Estado del cliente actualizado correctamente.");
    } catch (error) {
        showAlert("Error al actualizar cliente.", "error");
    }
}

function resetClienteForm() {
    document.getElementById("form-cliente").reset();
    document.getElementById("cliente-id-edit").value = "";
    document.getElementById("titulo-form-cliente").textContent = "Registrar cliente";
}

function renderVentas() {
    populateClienteSelect();
    populateProductSelects();
    renderEnvioVentaOptions();
    updateVentaResumen();

    document.getElementById("tbody-ventas").innerHTML = state.ventas.map(v => `
        <tr>
            <td>#${v.id}</td>
            <td>${v.fecha}</td>
            <td>${v.cliente_nombre}</td>
            <td>${ventaProductosTexto(v)}</td>
            <td>${ventaCantidadTotal(v)}</td>
            <td>${v.metodo_pago}</td>
            <td>${currency(v.total)}</td>
            <td>${badgeEstadoHTML(v.estado)}</td>
        </tr>
    `).join("") || `<tr><td colspan="8" class="mini-note">No hay ventas registradas.</td></tr>`;
}

function updateVentaResumen() {
    const clienteId = Number(document.getElementById("venta-cliente").value);
    const productoId = Number(document.getElementById("venta-producto").value);
    const cantidad = Number(document.getElementById("venta-cantidad").value || 0);

    const cliente = state.clientes.find(c => c.id === clienteId);
    const producto = state.productos.find(p => p.id === productoId);

    if (!cliente || !producto || cantidad <= 0) {
        document.getElementById("venta-resumen").innerHTML = "Completa cliente, producto y cantidad para visualizar el resumen.";
        return;
    }

    const total = producto.precio * cantidad;

    document.getElementById("venta-resumen").innerHTML = `
        <p><strong>Cliente:</strong> ${cliente.nombre}</p>
        <p><strong>Producto:</strong> ${producto.nombre}</p>
        <p><strong>Cantidad:</strong> ${cantidad}</p>
        <p><strong>Precio unitario:</strong> ${currency(producto.precio)}</p>
        <p><strong>Total:</strong> ${currency(total)}</p>
        <p class="mini-note">Esta venta rebajará automáticamente el stock del producto seleccionado.</p>
    `;
}

async function submitVenta(event) {
    event.preventDefault();

    const clienteId = Number(document.getElementById("venta-cliente").value);
    const productoId = Number(document.getElementById("venta-producto").value);
    const cantidad = Number(document.getElementById("venta-cantidad").value);
    const metodoPago = document.getElementById("venta-pago").value;
    const observacion = document.getElementById("venta-observacion").value.trim();

    if (!clienteId || !productoId || cantidad <= 0) {
        showAlert("Debes completar cliente, producto y cantidad.", "error");
        return;
    }

    const payload = {
        cliente_id: clienteId,
        detalles: [
            {
                producto_id: productoId,
                cantidad: cantidad
            }
        ],
        metodo_pago: metodoPago,
        observacion: observacion
    };

    try {
        const res = await fetch(`${API}/ventas`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo registrar la venta.", "error");
            return;
        }

        document.getElementById("form-venta").reset();

        await loadVentas();
        await loadProductos();

        renderVentas();
        renderInventario();
        renderProductos();
        renderDashboard();
        renderReportes();
        renderEnvioVentaOptions();

        showAlert("Venta registrada correctamente.");
    } catch (error) {
        showAlert("Error de conexión al registrar la venta.", "error");
    }
}

function renderEnvioVentaOptions() {
    const select = document.getElementById("envio-venta");
    const current = select.value;

    select.innerHTML = `<option value="">Selecciona una venta</option>` + state.ventas.map(v => `
        <option value="${v.id}">
            Venta #${v.id} - ${v.cliente_nombre} - ${ventaProductosTexto(v)}
        </option>
    `).join("");

    if (current) select.value = current;
}

async function submitEnvio(event) {
    event.preventDefault();

    const ventaId = Number(document.getElementById("envio-venta").value);
    const fecha = document.getElementById("envio-fecha").value;
    const direccion = document.getElementById("envio-direccion").value.trim();
    const rutaId = Number(document.getElementById("envio-ruta").value);
    const vehiculo = document.getElementById("envio-vehiculo").value.trim();
    const observacion = document.getElementById("envio-observacion").value.trim();

    const venta = state.ventas.find(v => v.id === ventaId);
    const ruta = state.rutas.find(r => r.id === rutaId);

    if (!venta || !direccion) {
        showAlert("Debes seleccionar una venta y una dirección.", "error");
        return;
    }

    const payload = {
        producto_id: venta.producto_id,
        cantidad: venta.cantidad,
        destinatario: venta.cliente_nombre,
        direccion,
        observacion: `Venta #${venta.id} | Ruta: ${ruta ? ruta.origen + " → " + ruta.destino : "Sin ruta"} | Vehículo: ${vehiculo || "Sin vehículo"} | Fecha: ${fecha} | ${observacion}`.trim()
    };

    try {
        const res = await fetch(`${API}/envios`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo registrar el envío.", "error");
            return;
        }

        const createdId = data.id_envio || data.id || null;

        if (createdId) {
            state.enviosMeta.push({
                id_envio: createdId,
                venta_id: venta.id,
                ruta: ruta ? `${ruta.origen} → ${ruta.destino}` : "",
                vehiculo: vehiculo || "",
                fecha_programada: fecha || ""
            });
            saveStorage(STORAGE_KEYS.envios_meta, state.enviosMeta);
        }

        venta.envio_creado = true;
        saveStorage(STORAGE_KEYS.ventas, state.ventas);

        event.target.reset();
        await loadEnvios();
        renderEnvios();
        renderDashboard();
        renderReportes();
        showAlert("Envío registrado correctamente.");
    } catch (error) {
        showAlert("Error de conexión al registrar envío.", "error");
    }
}

function renderEnvios() {
    renderEnvioVentaOptions();
    populateRutasSelect();

    document.getElementById("tbody-envios").innerHTML = state.envios.map(e => {
        const meta = state.enviosMeta.find(m => Number(m.id_envio) === Number(e.id_envio));
        const statusSelect = e.id_envio ? `
            <select id="estado-envio-${e.id_envio}">
                ${["Pendiente", "En preparación", "Despachado", "En tránsito", "Entregado", "Cancelado"].map(estado => `
                    <option value="${estado}" ${normalizeStatus(e.estado) === normalizeStatus(estado) ? "selected" : ""}>${estado}</option>
                `).join("")}
            </select>
        ` : `<span class="mini-note">Sin ID</span>`;

        return `
            <tr>
                <td>${e.id_envio ?? "-"}</td>
                <td>${meta?.venta_id ? "#" + meta.venta_id : "-"}</td>
                <td>${e.destinatario ?? "-"}</td>
                <td>${e.direccion ?? "-"}</td>
                <td>${meta?.ruta || "-"}</td>
                <td>${meta?.vehiculo || "-"}</td>
                <td>
                    <div class="mini-note">${badgeEstadoHTML(e.estado || "Pendiente")}</div>
                    ${statusSelect}
                </td>
                <td>${extractFechaFromEnvio(e, meta)}</td>
                <td>
                    <div class="actions">
                        ${e.id_envio ? `<button class="btn btn-light btn-sm" onclick="changeEnvioStatus(${e.id_envio})">Actualizar</button>` : ""}
                        ${e.id_envio ? `<button class="btn btn-danger btn-sm" onclick="deleteEnvio(${e.id_envio})">Cancelar</button>` : ""}
                    </div>
                </td>
            </tr>
        `;
    }).join("") || `<tr><td colspan="9" class="mini-note">No hay envíos registrados.</td></tr>`;
}

function normalizeStatus(value) {
    return (value || "").toString().toLowerCase().trim();
}

async function changeEnvioStatus(id) {
    const select = document.getElementById(`estado-envio-${id}`);
    const estado = select.value;

    try {
        const res = await fetch(`${API}/envios/${id}/estado`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ estado })
        });

        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo actualizar el estado.", "error");
            return;
        }

        await loadEnvios();
        renderEnvios();
        renderDashboard();
        renderReportes();
        showAlert("Estado del envío actualizado correctamente.");
    } catch (error) {
        showAlert("Error al actualizar estado.", "error");
    }
}

async function deleteEnvio(id) {
    const confirmDelete = confirm(`¿Cancelar / eliminar envío #${id}?`);
    if (!confirmDelete) return;

    try {
        const res = await fetch(`${API}/envios/${id}`, { method: "DELETE" });
        const data = await res.json();

        if (!res.ok) {
            showAlert(data.detail || "No se pudo cancelar el envío.", "error");
            return;
        }

        state.enviosMeta = state.enviosMeta.filter(m => Number(m.id_envio) !== Number(id));
        saveStorage(STORAGE_KEYS.envios_meta, state.enviosMeta);

        await loadEnvios();
        renderEnvios();
        renderDashboard();
        renderReportes();
        showAlert("Envío cancelado correctamente.");
    } catch (error) {
        showAlert("Error al cancelar envío.", "error");
    }
}

function extractFechaFromEnvio(envio, meta) {
    return envio.fecha_envio || envio.fecha || meta?.fecha_programada || "--";
}

function submitRuta(event) {
    event.preventDefault();

    const editId = Number(document.getElementById("ruta-id-edit").value);
    const ruta = {
        id: editId || nextId(state.rutas),
        origen: document.getElementById("ruta-origen").value.trim(),
        destino: document.getElementById("ruta-destino").value.trim(),
        distancia: document.getElementById("ruta-distancia").value.trim(),
        estado: document.getElementById("ruta-estado").value
    };

    if (editId) {
        const idx = state.rutas.findIndex(r => r.id === editId);
        state.rutas[idx] = ruta;
        showAlert("Ruta actualizada correctamente.");
    } else {
        state.rutas.unshift(ruta);
        showAlert("Ruta registrada correctamente.");
    }

    saveStorage(STORAGE_KEYS.rutas, state.rutas);
    document.getElementById("form-ruta").reset();
    document.getElementById("ruta-id-edit").value = "";
    renderRutas();
    renderEnvios();
}

function renderRutas() {
    populateRutasSelect();

    document.getElementById("tbody-rutas").innerHTML = state.rutas.map(r => `
        <tr>
            <td>${r.id}</td>
            <td>${r.origen}</td>
            <td>${r.destino}</td>
            <td>${r.distancia}</td>
            <td>${badgeEstadoHTML(r.estado)}</td>
            <td>
                <div class="actions">
                    <button class="btn btn-light btn-sm" onclick="editRuta(${r.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="toggleRuta(${r.id})">${r.estado === "Activa" ? "Desactivar" : "Activar"}</button>
                </div>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="6" class="mini-note">No hay rutas registradas.</td></tr>`;
}

function editRuta(id) {
    const ruta = state.rutas.find(r => r.id === id);
    document.getElementById("ruta-id-edit").value = ruta.id;
    document.getElementById("ruta-origen").value = ruta.origen;
    document.getElementById("ruta-destino").value = ruta.destino;
    document.getElementById("ruta-distancia").value = ruta.distancia;
    document.getElementById("ruta-estado").value = ruta.estado;
    activateSection("rutas");
}

function toggleRuta(id) {
    const ruta = state.rutas.find(r => r.id === id);
    ruta.estado = ruta.estado === "Activa" ? "Inactiva" : "Activa";
    saveStorage(STORAGE_KEYS.rutas, state.rutas);
    renderRutas();
    renderEnvios();
}

function populateRutasSelect() {
    const select = document.getElementById("envio-ruta");
    const current = select.value;
    select.innerHTML = `<option value="">Sin ruta</option>` + state.rutas
        .filter(r => r.estado === "Activa")
        .map(r => `<option value="${r.id}">${r.origen} → ${r.destino}</option>`)
        .join("");
    if (current) select.value = current;
}

function submitUsuario(event) {
    event.preventDefault();

    const editId = Number(document.getElementById("usuario-id-edit").value);
    const usuario = {
        id: editId || nextId(state.usuarios),
        username: document.getElementById("usuario-username").value.trim(),
        nombre: document.getElementById("usuario-nombre").value.trim(),
        correo: document.getElementById("usuario-correo").value.trim(),
        password: document.getElementById("usuario-password").value.trim(),
        rol: document.getElementById("usuario-rol").value,
        estado: document.getElementById("usuario-estado").value
    };

    if (editId) {
        const idx = state.usuarios.findIndex(u => u.id === editId);
        state.usuarios[idx] = usuario;
        showAlert("Usuario actualizado correctamente.");
    } else {
        state.usuarios.unshift(usuario);
        showAlert("Usuario registrado correctamente.");
    }

    saveStorage(STORAGE_KEYS.usuarios, state.usuarios);
    document.getElementById("form-usuario").reset();
    document.getElementById("usuario-id-edit").value = "";
    renderUsuarios();
    renderRoles();
    renderPermisos();
}

function renderUsuarios() {
    populateRolesForUsers();

    document.getElementById("tbody-usuarios").innerHTML = state.usuarios.map(u => `
        <tr>
            <td>${u.id}</td>
            <td>${u.username}</td>
            <td>${u.nombre}</td>
            <td>${u.correo}</td>
            <td>${u.rol}</td>
            <td>${badgeEstadoHTML(u.estado)}</td>
            <td>
                <div class="actions">
                    <button class="btn btn-light btn-sm" onclick="editUsuario(${u.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="toggleUsuario(${u.id})">${u.estado === "Activo" ? "Desactivar" : "Activar"}</button>
                </div>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="7" class="mini-note">No hay usuarios registrados.</td></tr>`;
}

function populateRolesForUsers() {
    const select = document.getElementById("usuario-rol");
    const current = select.value;
    select.innerHTML = state.roles
        .filter(r => r.estado === "Activo")
        .map(r => `<option value="${r.nombre}">${r.nombre}</option>`)
        .join("");
    if (current) select.value = current;
}

function editUsuario(id) {
    const u = state.usuarios.find(x => x.id === id);
    document.getElementById("usuario-id-edit").value = u.id;
    document.getElementById("usuario-username").value = u.username;
    document.getElementById("usuario-nombre").value = u.nombre;
    document.getElementById("usuario-correo").value = u.correo;
    document.getElementById("usuario-password").value = u.password;
    document.getElementById("usuario-rol").value = u.rol;
    document.getElementById("usuario-estado").value = u.estado;
    activateSection("usuarios");
}

function toggleUsuario(id) {
    const usuario = state.usuarios.find(u => u.id === id);
    usuario.estado = usuario.estado === "Activo" ? "Inactivo" : "Activo";
    saveStorage(STORAGE_KEYS.usuarios, state.usuarios);
    renderUsuarios();
}

function submitRol(event) {
    event.preventDefault();

    const editId = Number(document.getElementById("rol-id-edit").value);
    const rol = {
        id: editId || nextId(state.roles),
        nombre: document.getElementById("rol-nombre").value.trim(),
        descripcion: document.getElementById("rol-descripcion").value.trim(),
        estado: document.getElementById("rol-estado").value,
        permisos: editId ? (state.roles.find(r => r.id === editId)?.permisos || []) : []
    };

    if (editId) {
        const idx = state.roles.findIndex(r => r.id === editId);
        state.roles[idx] = rol;
        showAlert("Rol actualizado correctamente.");
    } else {
        state.roles.unshift(rol);
        showAlert("Rol registrado correctamente.");
    }

    saveStorage(STORAGE_KEYS.roles, state.roles);
    document.getElementById("form-rol").reset();
    document.getElementById("rol-id-edit").value = "";
    renderRoles();
    renderPermisos();
    renderUsuarios();
}

function renderRoles() {
    document.getElementById("tbody-roles").innerHTML = state.roles.map(r => `
        <tr>
            <td>${r.id}</td>
            <td>${r.nombre}</td>
            <td>${r.descripcion}</td>
            <td>${badgeEstadoHTML(r.estado)}</td>
            <td>
                <div class="actions">
                    <button class="btn btn-light btn-sm" onclick="editRol(${r.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="toggleRol(${r.id})">${r.estado === "Activo" ? "Desactivar" : "Activar"}</button>
                </div>
            </td>
        </tr>
    `).join("") || `<tr><td colspan="5" class="mini-note">No hay roles registrados.</td></tr>`;
}

function renderPermisos() {
    const modules = ["productos", "inventario", "clientes", "ventas", "envios", "reportes", "usuarios"];

    document.getElementById("tbody-permisos").innerHTML = state.roles.map(r => `
        <tr>
            <td><strong>${r.nombre}</strong></td>
            ${modules.map(module => `
                <td>
                    <input type="checkbox"
                        ${r.permisos.includes(module) ? "checked" : ""}
                        onchange="togglePermiso(${r.id}, '${module}', this.checked)" />
                </td>
            `).join("")}
        </tr>
    `).join("") || `<tr><td colspan="8" class="mini-note">No hay roles configurados.</td></tr>`;
}

function togglePermiso(roleId, module, checked) {
    const rol = state.roles.find(r => r.id === roleId);
    if (!rol) return;

    if (checked && !rol.permisos.includes(module)) rol.permisos.push(module);
    if (!checked) rol.permisos = rol.permisos.filter(p => p !== module);

    saveStorage(STORAGE_KEYS.roles, state.roles);
    renderPermisos();
}

function editRol(id) {
    const r = state.roles.find(x => x.id === id);
    document.getElementById("rol-id-edit").value = r.id;
    document.getElementById("rol-nombre").value = r.nombre;
    document.getElementById("rol-descripcion").value = r.descripcion;
    document.getElementById("rol-estado").value = r.estado;
    activateSection("roles");
}

function toggleRol(id) {
    const rol = state.roles.find(r => r.id === id);
    rol.estado = rol.estado === "Activo" ? "Inactivo" : "Activo";
    saveStorage(STORAGE_KEYS.roles, state.roles);
    renderRoles();
    renderUsuarios();
}

function renderReportes() {
    const ventasTotal = state.ventas.reduce((acc, v) => acc + Number(v.total || 0), 0);
    const clientesActivos = state.clientes.filter(c => c.estado === "Activo").length;
    const enviosEntregados = state.envios.filter(e => normalizeStatus(e.estado) === "entregado").length;

    document.getElementById("rep-inventario-total").textContent = state.productos.length;
    document.getElementById("rep-ventas-total").textContent = currency(ventasTotal);
    document.getElementById("rep-clientes-activos").textContent = clientesActivos;
    document.getElementById("rep-envios-entregados").textContent = enviosEntregados;

    document.getElementById("tbody-reporte-inventario").innerHTML = state.productos.map(p => `
        <tr>
            <td>${p.nombre}</td>
            <td>${p.stock}</td>
            <td>${badgeEstadoHTML(productStockLabel(p.stock))}</td>
        </tr>
    `).join("") || `<tr><td colspan="3" class="mini-note">Sin datos de inventario.</td></tr>`;

    document.getElementById("tbody-reporte-ventas").innerHTML = state.ventas.slice(0, 10).map(v => `
        <tr>
            <td>#${v.id} - ${ventaProductosTexto(v)}</td>
            <td>${v.cliente_nombre}</td>
            <td>${currency(v.total)}</td>
            <td>${v.fecha}</td>
        </tr>
    `).join("") || `<tr><td colspan="4" class="mini-note">Sin ventas registradas.</td></tr>`;

    document.getElementById("tbody-reporte-clientes").innerHTML = state.clientes.map(c => `
        <tr>
            <td>${c.nombre}</td>
            <td>${c.correo}</td>
            <td>${badgeEstadoHTML(c.estado)}</td>
        </tr>
    `).join("") || `<tr><td colspan="3" class="mini-note">Sin clientes registrados.</td></tr>`;

    document.getElementById("tbody-reporte-logistico").innerHTML = state.envios.map(e => `
        <tr>
            <td>#${e.id_envio ?? "-"}</td>
            <td>${e.destinatario ?? "-"}</td>
            <td>${badgeEstadoHTML(e.estado ?? "Pendiente")}</td>
            <td>${extractFechaFromEnvio(e)}</td>
        </tr>
    `).join("") || `<tr><td colspan="4" class="mini-note">Sin envíos registrados.</td></tr>`;
}

async function submitTracking(event) {
    event.preventDefault();
    const id = Number(document.getElementById("tracking-id").value);

    if (!id) {
        showAlert("Ingresa un ID de envío válido.", "error");
        return;
    }

    const envio = state.envios.find(e => Number(e.id_envio) === id);
    if (!envio) {
        document.getElementById("tracking-result").innerHTML = `No se encontró un envío con ID #${id}.`;
        return;
    }

    const meta = state.enviosMeta.find(m => Number(m.id_envio) === id);

    document.getElementById("tracking-result").innerHTML = `
        <p><strong>Envío #${envio.id_envio}</strong></p>
        <p><strong>Destinatario:</strong> ${envio.destinatario ?? "-"}</p>
        <p><strong>Producto:</strong> ${envio.nombre_producto ?? "-"}</p>
        <p><strong>Dirección:</strong> ${envio.direccion ?? "-"}</p>
        <p><strong>Ruta:</strong> ${meta?.ruta || "-"}</p>
        <p><strong>Vehículo:</strong> ${meta?.vehiculo || "-"}</p>
        <p><strong>Fecha:</strong> ${extractFechaFromEnvio(envio, meta)}</p>
        <p><strong>Estado actual:</strong> ${badgeEstadoHTML(envio.estado ?? "Pendiente")}</p>
    `;
}

function nextId(collection) {
    return collection.length ? Math.max(...collection.map(item => Number(item.id))) + 1 : 1;
}

function activateSection(name) {
    showSection(name);
}