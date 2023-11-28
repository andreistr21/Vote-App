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

function getVoteFormData(event) {
  const voteFormObjId = event.target.closest(".vote-form").id;
  let data = {};
  data.form = parseInt(voteFormObjId.split("-").pop(), 10);
  const voteField = event.target.parentNode.parentNode.parentNode.parentNode.id;
  data.vote = parseInt(voteField.split("-").pop(), 10);
  return data;
}

export function addListenersToForms() {
  const voteForms = document.querySelectorAll(".vote-form");

  voteForms.forEach(function (voteForm) {
    voteForm.addEventListener("change", function (event) {
      if (event.target.type === "radio" || event.target.type === "checkbox") {
        if (event.target.checked) {
          sendCreateVote(event);
        } else {
          sendDeleteVote(event);
        }
      }
    });
  });
}
