import { createFormPage } from "./js_pages/vote/create_form.js";
import { loginPage } from "./js_pages/user/login.js";

window.addEventListener("load", function () {
  const currentPath = window.location.pathname;

  if (currentPath == "/pages/user/login.html") {
    loginPage();
  } else if (currentPath == "/pages/vote/create_form.html") {
    createFormPage();
  }
});
