async function loadProducts() {
    const token = localStorage.getItem("token");

    const response = await fetch("/api/products/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await response.json();

    const container = document.getElementById("product-list");
    container.innerHTML = "";

    data.forEach(prod => {
        const card = `
            <div class="product-card">
                <h3>${prod.name}</h3>
                <p>Precio: ${prod.price} €</p>
                <button onclick="addToCart(${prod.id})">Añadir al carrito</button>
            </div>
        `;
        container.innerHTML += card;
    });
}

async function addToCart(productId) {
    const token = localStorage.getItem("token");
    console.log("TOKEN:", token)
    const response = await fetch("/api/orders/add_to_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            product: productId,
            quantity: 1
        })
    });

    const data = await response.json();

    if (!response.ok) {
        alert("Error: " + (data.detail || "No autorizado"));
        return;
    }

    alert(data.message);
}

loadProducts();
