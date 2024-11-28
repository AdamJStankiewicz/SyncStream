document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const messageDiv = document.getElementById("message");

    try {
        const response = await fetch("http://127.0.0.1:1477/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.ERROR || "Login failed");
        }

        const data = await response.json();
        console.log(`Username: ${username}`);
        console.log(`Password: ${password}`);
        console.log(`Session ID: ${data.sessionID}`);
        console.log(`User ID: ${data.id}`);

        const userSessionData = {
            sessionID: data.sessionID,
            userID: data.id
        };
        localStorage.setItem('userSession', JSON.stringify(userSessionData));

        messageDiv.textContent = `Logged in. Session ID: ${data.sessionID}`;
    } catch (error) {
        messageDiv.textContent = error.message;
        console.error("Error:", error);
    }
});
