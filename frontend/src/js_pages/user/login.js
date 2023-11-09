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
        document.cookie = "auth_token=" + responseData.token + "; path=/";
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

function loginFormEventListener() {
  const loginForm = document.getElementById("login-form");
  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const username = document.getElementById("username-input").value;
    const password = document.getElementById("password-input").value;

    login(username, password);
  });
}

// eslint-disable-next-line no-unused-vars
export function loginPage() {
  loginFormEventListener();
}
