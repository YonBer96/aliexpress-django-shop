const token_checkout = localStorage.getItem("token");

document.getElementById("payBtn").addEventListener("click", () => {

    fetch("http://127.0.0.1:8000/api/orders/pay/", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token_checkout
        }
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("msg").textContent = data.message;
        });

});
