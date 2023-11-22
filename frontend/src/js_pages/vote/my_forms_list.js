import { backendDomain } from "../../globals.js";

function loadTemplateFile() {
  return fetch("./voteFormTemplate.ejs")
    .then((response) => response.text())
    .catch((error) => {
      console.error("Error loading template:", error);
    });
}

function createFormsList(formsData) {
  let forms = [];

  loadTemplateFile()
    .then((templateString) => {
      formsData.forEach(function (formData) {
        const renderedHTML = ejs.render(templateString, formData);
        forms.push(renderedHTML);
      });

      appendFormsToHTML(forms);
    })
    .catch((error) => {
      console.error("Error loading template:", error);
    });
}

function appendFormsToHTML(formsList) {
  let elementToAppend = document.getElementsByClassName("section-middle")[0];

  formsList.forEach(function (form) {
    elementToAppend.innerHTML += form;
  });
}

function fetchData() {
  fetch(backendDomain + "vote/my-forms/", {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      createFormsList(data.results);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

window.addEventListener("load", function () {
  fetchData();
});
