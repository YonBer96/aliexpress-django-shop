const API_URL = "http://127.0.0.1:8000/api";

async function loadCart() {

    const token = localStorage.getItem("access");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    const response = await fetch(`${API_URL}/orders/cart/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const items = await response.json();
    let html = "";
    let total = 0;

    items.forEach(item => {
        const subtotal = item.quantity * item.product_price;
        total += subtotal;

        html += `
        <div class="cart-item">
            <img src="https://picsum.photos/120?random=${item.product}" />

            <div>
                <div class="cart-title">${item.product_name}</div>
                <div class="cart-price">${item.product_price}€</div>
            </div>

            <div class="qty-controls">
                <button onclick="updateQty(${item.id}, ${item.quantity - 1})">−</button>
                <input type="text" value="${item.quantity}" disabled>
                <button onclick="updateQty(${item.id}, ${item.quantity + 1})">+</button>
            </div>

            <div class="cart-price">${subtotal.toFixed(2)}€</div>

            <button class="delete-btn qty-controls" onclick="deleteItem(${item.id})">X</button>
        </div>
        `;
    });

    document.getElementById("cart-container").innerHTML = html;
    document.getElementById("cart-total").textContent = total.toFixed(2) + "€";
}

async function updateQty(itemId, newQty) {
    if (newQty <= 0) return;

    const token = localStorage.getItem("access");

    await fetch(`${API_URL}/orders/cart/items/${itemId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ quantity: newQty })
    });

    loadCart();
}

async function deleteItem(itemId) {
    const token = localStorage.getItem("access");

    await fetch(`${API_URL}/orders/cart/items/${itemId}/delete/`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    loadCart();
}

document.getElementById("checkout-btn").onclick = async () => {
    window.location.href = "/checkout.html";
};

loadCart();
