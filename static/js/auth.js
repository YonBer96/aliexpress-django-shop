async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access);
        alert("Login correcto. Redirigiendo...");
        window.location.href = "/api/products/";
    } else {
        alert("Usuario o contraseña incorrectos");
    }
}
