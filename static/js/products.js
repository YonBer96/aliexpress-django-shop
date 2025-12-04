document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    const response = await fetch("/api/products/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const products = await response.json();

    let html = "";
    products.forEach(prod => {
        html += `<p><strong>${prod.name}</strong> - ${prod.price}€</p>`;
    });

    document.getElementById("product-list").innerHTML = html;
});
