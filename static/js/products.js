const API_URL = "http://127.0.0.1:8000/api";

async function loadProducts() {
    const response = await fetch(`${API_URL}/products/`);
    const products = await response.json();

    let html = "";

    products.forEach(p => {
        html += `
        <div class="product-card">
            <img src="https://picsum.photos/200?random=${p.id}" />
            <h3>${p.name}</h3>
            <p>${p.description}</p>
            <strong>${p.price}€</strong>
            <button onclick="addToCart(${p.id})">Añadir al carrito</button>
        </div>`;
    });

    document.getElementById("product-list").innerHTML = html;
}

async function addToCart(productId) {
    const token = localStorage.getItem("access");

    // 🔒 Si no hay token → forzar login
    if (!token) {
        alert("Debes iniciar sesión para añadir productos al carrito.");
        window.location.href = "/login.html";
        return;
    }

    const response = await fetch(`${API_URL}/orders/add_to_cart/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product: productId,
            quantity: 1
        })
    });

    // 🔥 Token expirado o inválido
    if (response.status === 401) {
        alert("Tu sesión ha expirado. Inicia sesión de nuevo.");
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login.html";
        return;
    }

    const data = await response.json();
    alert(data.message);

    // Actualizar contador del carrito
    if (typeof updateCartCount === "function") {
        updateCartCount();
    }
}


loadProducts();
