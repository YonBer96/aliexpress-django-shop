const API_URL = "http://127.0.0.1:8000/api";

async function loadOrders() {

    const token = localStorage.getItem("access");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    const response = await fetch(`${API_URL}/orders/`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const orders = await response.json();

    const container = document.getElementById("orders-list");

    if (orders.length === 0) {
        container.innerHTML = "<p>No tienes pedidos todavía.</p>";
        return;
    }

    let html = "";

    orders.forEach(order => {

        if (!order.is_paid) return;

        html += `
            <div class="order-card">
                <h3>Pedido #${order.id}</h3>
                <p>Fecha: ${new Date(order.created_at).toLocaleDateString()}</p>
                <p>Total: <strong>${order.total_price}€</strong></p>

                <button onclick="viewOrder(${order.id})">
                    Ver detalles
                </button>
            </div>
        `;
    });

    container.innerHTML = html;
}

function viewOrder(orderId) {
    window.location.href = `/order-detail.html?id=${orderId}`;
}

loadOrders();
