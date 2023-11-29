import { backendDomain } from "../../globals.js";

// TODO: Update form after fetching in both cases

function sendCreateVote(event) {
  const data = getVoteFormData(event);
  fetch(backendDomain + "vote/create-vote/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Happy post!:");
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function sendDeleteVote(event) {
  const data = getVoteFormData(event);
  fetch(backendDomain + "vote/delete-vote/", {
    method: "DELETE",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.status === 204) {
        return {};
      } else {
        return response.json();
      }
    })
    .then((data) => {
      console.log("Happy delete!:");
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function getVoteFormData(target) {
  const voteFormObjId = target.closest(".vote-form").id;
  let data = {};
  data.form = parseInt(voteFormObjId.split("-").pop(), 10);
  const voteField = target.parentNode.parentNode.parentNode.parentNode.id;
  data.vote = parseInt(voteField.split("-").pop(), 10);
  return data;
}

export function addListenersToForms() {
  const voteForms = document.querySelectorAll(".vote-form");
  const previousRadiosEvents = {};

  voteForms.forEach(function (voteForm) {
    // Adds radio inputs to previousRadiosEvents, so they could be identified
    // as previously selected
    const formId = voteForm.id;
    const initialCheckedRadio = voteForm.querySelector(
      "input[type='radio']:checked"
    );
    if (initialCheckedRadio) {
      previousRadiosEvents[formId] = initialCheckedRadio;
    }

    voteForm.addEventListener("change", function (event) {
      const { target } = event;
      const isRadio = target.type === "radio";
      const isCheckbox = target.type === "checkbox";
      if (isRadio) {
        const previousRadioEvent = previousRadiosEvents[formId];
        if (previousRadioEvent) {
          sendDeleteVote(previousRadioEvent);
        }
        previousRadiosEvents[formId] = target;
        sendCreateVote(target);
      } else if (isCheckbox) {
        if (target.checked) {
          sendCreateVote(target);
        } else {
          sendDeleteVote(target);
        }
      }
    });
  });
}
