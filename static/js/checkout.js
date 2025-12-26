const API_URL = "http://127.0.0.1:8000/api";

async function loadCheckout() {

    const token = localStorage.getItem("access");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    const response = await fetch(`${API_URL}/orders/cart/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const items = await response.json();
    console.log("ITEMS DEL CARRITO:", items);

    if (items.length === 0) {
        alert("Tu carrito está vacío");
        window.location.href = "/products.html";
        return;
    }

    let html = "";
    let total = 0;

    items.forEach(item => {

        const subtotal = item.product_price * item.quantity;
        total += subtotal;
        const subtotalText = subtotal.toFixed(2);

        html += `
            <div class="checkout-item">
                <img class="checkout-img" src="https://picsum.photos/120?random=${item.product}" />

                <div class="checkout-info">
                    <h3>${item.product_name}</h3>

                    <p class="stock">✔ En stock</p>
                    <p class="delivery">🚚 Entrega GRATIS</p>

                    <p>Cantidad: <strong>${item.quantity}</strong></p>
                    <p>Precio unidad: ${item.product_price}€</p>

                    <p class="subtotal">Subtotal: <strong>${subtotalText}€</strong></p>
                </div>
            </div>
        `;
    });

    document.getElementById("checkout-list").innerHTML = html;
    document.getElementById("checkout-total").textContent = total.toFixed(2) + "€";

    // Botón para desplegar resumen
    document.getElementById("summary-toggle").onclick = () => {
        document.getElementById("summary-details").classList.toggle("hidden");
    };

    // 🔥 DETECTAR EL ORDER ID CORRECTO DEL CARRITO
    const activeItem = items.find(i => i.order_id !== undefined);

    if (!activeItem) {
        alert("No se pudo determinar el ID del pedido actual.");
        return;
    }

    const orderId = activeItem.order_id;
    console.log("ORDER ID DETECTADO:", orderId);

    document.getElementById("confirm-order-btn").onclick = () =>
        confirmOrder(orderId, total);
}



async function confirmOrder(orderId, total) {

    // Animación
    document.getElementById("loading-animation").classList.remove("hidden");

    const token = localStorage.getItem("access");

    const paymentMethod = document.querySelector("input[name='payment']:checked").value;
    const shipping = document.querySelector("input[name='shipping']:checked").value;

    const address = {
        name: document.getElementById("address-name").value,
        street: document.getElementById("address-street").value,
        city: document.getElementById("address-city").value,
        zip: document.getElementById("address-zip").value
    };

    if (!address.name || !address.street || !address.city || !address.zip) {
        alert("Por favor completa tu dirección de envío.");
        return;
    }

    const response = await fetch(`${API_URL}/orders/${orderId}/checkout/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            payment: paymentMethod,
            shipping: shipping,
            address: address
        })
    });

    const data = await response.json();

    // Redirección a página de éxito
    window.location.href = "/success.html?order=" + orderId;
}

loadCheckout();
