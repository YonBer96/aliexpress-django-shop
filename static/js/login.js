const API_URL = "http://127.0.0.1:8000/api";

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_URL}/token/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    console.log("LOGIN RESPONSE:", data);

    if (data.access) {
        // Guardar token
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        // Redirigir a la tienda
        window.location.href = "/products.html";
    } else {
        alert("Usuario o contraseña incorrectos");
    }
});
