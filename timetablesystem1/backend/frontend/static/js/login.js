function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (!username || !password) {
        document.getElementById("error").innerText = "Please enter username and password";
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => {
        console.log("Response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data);
        if (data.status === "success") {
            console.log("Login successful, redirecting...");
            window.location.href = "/dashboard";
        } else {
            document.getElementById("error").innerText = data.message || "Invalid credentials";
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        document.getElementById("error").innerText = "Connection error: " + error;
    });
}