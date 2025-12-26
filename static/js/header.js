


async function updateCartCount() {
    const token = localStorage.getItem("access");

    if (!token) {
        document.getElementById("cart-count").textContent = 0;
        return;
    }

    const response = await fetch(`${API_URL}/orders/cart/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.status === 401) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        document.getElementById("cart-count").textContent = 0;
        return;
    }

    const items = await response.json();
    let count = 0;
    items.forEach(i => count += i.quantity);

    document.getElementById("cart-count").textContent = count;
}

document.addEventListener("DOMContentLoaded", updateCartCount);

