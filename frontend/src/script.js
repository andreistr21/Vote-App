function updateUsername(username) {
  document.getElementById("username").textContent = username;
}

function login(username, password) {
  fetch("http://127.0.0.1:8000/user/login/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const responseData = JSON.parse(data);
      if (responseData.detail === "Login successful.") {
        console.log("Login successful");
        document.cookie =
          "Authorization=Token " + responseData.token + "; path=/";
        updateUsername(responseData.user.username);
      } else if (responseData.detail === "You are already logged in.") {
        console.log("Already logged in");
        updateUsername(responseData.user.username);
      } else {
        console.log("Login failed");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function loginFormEventListener(loginForm) {
  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    login(username, password);
  });
}

window.addEventListener("load", function () {
  const loginForm = document.getElementById("login-form");

  if (loginForm) {
    loginFormEventListener(loginForm);
  }
});
