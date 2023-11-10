import { updateUsername } from "../../services.js";

function setUsername() {
  const username = localStorage.getItem("username");
  if (
    username === null &&
    window.location.pathname != "/pages/user/login.html"
  ) {
    window.location.replace("/pages/user/login.html");
  }
  document.getElementById("username").textContent = username;
}

function getCookie(name) {
  const match = document.cookie.match(
    RegExp("(?:^|;\\s*)" + name + "=([^;]*)")
  );
  return match ? match[1] : null;
}

function fetchAndUpdateUsername() {
  fetch("http://127.0.0.1:8000/user/get-username/", {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const responseData = JSON.parse(data);
      if (responseData.username !== "undefined") {
        updateUsername(responseData.username);
        setUsername();
      } else {
        window.location.replace("/pages/user/login.html");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function checkIfAuthToken() {
  if (
    !getCookie("auth_token") &&
    window.location.pathname != "/pages/user/login.html"
  ) {
    window.location.replace("/pages/user/login.html");
  }
}

export function checkIfUsername() {
  /**
   * Checks if username is in local storage.
   * If not - fetches it and saves in local storage.
   */
  let username = localStorage.getItem("username");
  if (username === null || username === "undefined") {
    checkIfAuthToken();
    fetchAndUpdateUsername();
  } else {
    setUsername(username);
  }
}
