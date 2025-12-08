async function loadCart() {
    const token = localStorage.getItem("token");

    const response = await fetch("/api/orders/cart/", {
        headers: { "Authorization": "Bearer " + token }
    });

    const data = await response.json();

    const container = document.getElementById("cart-container");

    if (data.length === 0) {
        container.innerHTML = "<p>El carrito está vacío.</p>";
        return;
    }

    container.innerHTML = "";

    data.forEach(item => {
        const html = `
            <div class="cart-item">
                <h3>${item.product_name}</h3>
                <p>Cantidad: 
                    <input type="number" id="qty-${item.id}" value="${item.quantity}" min="1">
                </p>
                <button onclick="updateItem(${item.id})">Actualizar</button>
                <button onclick="deleteItem(${item.id})">Eliminar</button>
            </div>
        `;
        container.innerHTML += html;
    });
}

async function updateItem(itemId) {
    const token = localStorage.getItem("token");
    const qty = document.getElementById(`qty-${itemId}`).value;

    const response = await fetch(`/api/orders/cart/item/${itemId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ quantity: qty })
    });

    const data = await response.json();
    alert(data.message);

    loadCart();
}

async function deleteItem(itemId) {
    const token = localStorage.getItem("token");

    const response = await fetch(`/api/orders/cart/item/${itemId}/delete/`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    });

    const data = await response.json();
    alert(data.message);
    loadCart();
}

loadCart();
