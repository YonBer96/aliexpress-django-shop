const API_URL = "http://127.0.0.1:8000/api";

function getOrderId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function loadOrderDetail() {
    const token = localStorage.getItem("access");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    const orderId = getOrderId();
    if (!orderId) {
        alert("Pedido no válido");
        return;
    }

    const response = await fetch(`${API_URL}/orders/${orderId}/summary/`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        alert("No se pudo cargar el pedido");
        return;
    }

    const data = await response.json();

    let html = "";

    data.items.forEach(item => {
        html += `
        <div class="order-item">

            <img 
                class="order-item-img"
                src="https://picsum.photos/100?random=${item.product}"
                alt="${item.product}"
            />

            <div class="order-item-info">
                <h3>${item.product}</h3>
                <p>Cantidad: <strong>${item.quantity}</strong></p>
                <p>Precio unidad: ${item.price}€</p>
                <p class="subtotal">
                    Subtotal: <strong>${item.subtotal}€</strong>
                </p>
            </div>

        </div>
    `;
    });

    document.getElementById("order-items").innerHTML = html;
    document.getElementById("order-total").textContent = data.total + "€";
}

loadOrderDetail();

// 📄 Descargar factura PDF
document.addEventListener("DOMContentLoaded", () => {

    const invoiceBtn = document.getElementById("invoice-btn");
    if (!invoiceBtn) return;

    invoiceBtn.onclick = async () => {
        const orderId = getOrderId();
        const token = localStorage.getItem("access");

        if (!orderId || !token) {
            alert("No se pudo descargar la factura.");
            return;
        }

        try {
            const response = await fetch(
                `${API_URL}/orders/${orderId}/invoice/`,
                {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                }
            );

            if (!response.ok) {
                alert("Error al generar la factura.");
                return;
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = `factura_pedido_${orderId}.pdf`;
            document.body.appendChild(a);
            a.click();

            a.remove();
            window.URL.revokeObjectURL(url);

        } catch (error) {
            alert("No se pudo descargar la factura.");
        }
    };
});
