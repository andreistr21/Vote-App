function addFormFieldFields() {
  const htmlToAppend = `
          <hr />

          <div class="vote-field">
            <div class="form-field">
              <label for="form-field-name-input">Field name:</label>
              <input
                type="text"
                class="form-field-name-input"
                name="field-name"
                required
                maxlength="80"
              />
            </div>
            <div class="form-field">
              <label for="form-field-description-input"
                >Field description:</label
              >
              <input
                type="text"
                class="form-description-input"
                name="field-description"
                maxlength="200"
              />
            </div>
`;
  const insertBefore = document.getElementById("add-field-btn");
  insertBefore.insertAdjacentHTML("beforebegin", htmlToAppend);
}

function getVoteFieldsValues() {
  let voteFieldsData = [];
  let formFields = document.querySelectorAll(".vote-field");

  formFields.forEach((field) => {
    let nameInputValue = field.querySelector(".form-field-name-input").value;
    let descriptionInput = field.querySelector(".form-description-input");

    if (nameInputValue && descriptionInput) {
      let fieldInfo = {
        name: nameInputValue,
        description: descriptionInput.value,
      };
      voteFieldsData.push(fieldInfo);
    }
  });
  return voteFieldsData;
}

function getFormData() {
  // let formElement = document.getElementById("vote-form-form");
  let formNameInput = document.getElementById("form-name-input").value;
  let formDescriptionInput = document.getElementById(
    "form-description-input"
  ).value;
  let statisticsTypeDropdown = document.getElementById(
    "statistics-type-dropdown"
  ).value;
  let votesTypeDropdown = document.getElementById("votes-type-dropdown").value;
  let closingDateInput = document.getElementById("closing-date-input").value;

  if (
    // formElement &&
    formNameInput &&
    formDescriptionInput &&
    statisticsTypeDropdown &&
    votesTypeDropdown &&
    closingDateInput
  ) {
    return {
      // formElement: formElement,
      name: formNameInput,
      description: formDescriptionInput,
      statistics_type: statisticsTypeDropdown,
      votes_type: votesTypeDropdown,
      closing: closingDateInput,
      vote_fields: getVoteFieldsValues(),
    };
  } else {
    console.error("Form doesn't filled out correctly.");
    return null;
  }
}

function addErrorsToForm(errors) {
  let form = document.getElementById("vote-form-form");
  let errorsDiv = document.createElement("div");
  errorsDiv.classList.add("form-errors");
  // Iterate through the object's properties and create div elements for each one inside the errorsDiv
  for (const key in errors) {
    // eslint-disable-next-line no-prototype-builtins
    if (errors.hasOwnProperty(key)) {
      const div = document.createElement("div");
      div.textContent = `${key}: ${errors[key]}`;
      errorsDiv.appendChild(div);
    }
  }
  form.insertAdjacentElement("beforeend", errorsDiv);
}

function sendFormData(formData) {
  fetch("http://127.0.0.1:8000/vote/create-form/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      const responseData = JSON.parse(data);

      if (responseData.details === "Form created successfully.") {
        console.log("Form created successfully");
        location.reload();
      } else if (responseData.errors) {
        console.log("Form returned errors");
        addErrorsToForm(responseData.errors);
      } else {
        console.log("Unexpected response");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function formSubmit() {
  const formData = getFormData();
  if (formData) {
    sendFormData(formData);
  }
}

function addFormListeners() {
  // Add more fields btn listener
  const addFieldBtn = document.getElementById("add-field-btn");
  addFieldBtn.addEventListener("click", function () {
    addFormFieldFields();
  });
  // Submit form listener
  let createVoteFormForm = document.getElementById("vote-form-form");
  createVoteFormForm.addEventListener("submit", function (event) {
    event.preventDefault();
    formSubmit();
  });
}

function createFormPageScript() {
  addFormListeners();
}

// eslint-disable-next-line no-unused-vars
export function createFormPage() {
  createFormPageScript();
}
