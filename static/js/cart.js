const token_cart = localStorage.getItem("token");

fetch("http://127.0.0.1:8000/api/cart/", {
    headers: { "Authorization": "Bearer " + token_cart }
})
    .then(res => res.json())
    .then(items => {
        let html = "";
        items.forEach(item => {
            html += `
            <div>
                <h3>${item.product_name}</h3>
                <p>Cantidad: ${item.quantity}</p>

                <button onclick="updateItem(${item.id}, ${item.quantity + 1})">+</button>
                <button onclick="updateItem(${item.id}, ${item.quantity - 1})">-</button>
                <button onclick="deleteItem(${item.id})">Eliminar</button>
            </div>
            <hr>
        `;
        });

        document.getElementById("cart").innerHTML = html;
    });

function updateItem(id, quantity) {
    fetch(`http://127.0.0.1:8000/api/cart/item/${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_cart
        },
        body: JSON.stringify({ quantity })
    })
        .then(res => res.json())
        .then(data => alert(data.message || JSON.stringify(data)));
}

function deleteItem(id) {
    fetch(`http://127.0.0.1:8000/api/cart/item/${id}/`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token_cart
        }
    })
        .then(res => res.json())
        .then(data => alert(data.message || JSON.stringify(data)));
}
