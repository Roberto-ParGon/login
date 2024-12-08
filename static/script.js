document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (validateInput(username) && validateInput(password)) {
      authenticateUser(username, password);
    } else {
      displayMessage("Entrada no válida.");
    }
  });

function validateInput(input) {
  const regex = /^[a-zA-Z0-9]+$/;
  return regex.test(input);
}

function authenticateUser(username, password) {
  fetch("/api/authenticate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error en la autenticación");
      }
      return response.json();
    })
    .then((data) => {
      displayMessage("Inicio de sesión exitoso.");
      window.location.href = "/home";
    })
    .catch((error) => {
      displayMessage("Error: " + error.message);
    });
}

function displayMessage(message) {
  const messageDiv = document.getElementById("message");
  messageDiv.textContent = message;
  messageDiv.style.color = "red";
}
