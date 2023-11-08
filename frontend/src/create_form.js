function addFormFieldFields() {
  const htmlToAppend = `
    <hr />

    <div class="form-field">
      <label for="form-field-name-input">Field name:</label>
      <input
        type="text"
        id="form-field-name-input"
        name="field-name"
        required
        maxlength="80"
      />
    </div>
    <div class="form-field">
      <label for="form-field-description-input">Field description:</label>
      <input
        type="text"
        id="form-description-input"
        name="field-description"
        required
        maxlength="200"
      />
    </div>
`;
  const insertBefore = document.getElementById("add-field-btn");
  insertBefore.insertAdjacentHTML("beforebegin", htmlToAppend);
}

function formAddFieldListener() {
  const addFieldBtn = document.getElementById("add-field-btn");
  addFieldBtn.addEventListener("click", function () {
    addFormFieldFields();
  });
}

function createFormPageScript() {
  formAddFieldListener();
}

// eslint-disable-next-line no-unused-vars
export function createFormPage() {
  createFormPageScript();
}
