import { backendDomain } from "../../globals.js";

function loadTemplateFile() {
  return fetch("./voteFormTemplate.ejs")
    .then((response) => response.text())
    .catch((error) => {
      console.error("Error loading template:", error);
    });
}

function normalizeDate(date) {
  const parsedDate = new Date(date);

  const year = parsedDate.getFullYear();
  const month = String(parsedDate.getMonth() + 1).padStart(2, "0");
  const day = String(parsedDate.getDate()).padStart(2, "0");
  const hours = String(parsedDate.getHours()).padStart(2, "0");
  const minutes = String(parsedDate.getMinutes()).padStart(2, "0");

  return `${hours}:${minutes}, ${year}.${month}.${day}`;
}

function findVoteCountById(formData, voteCountId) {
  const voteCount = formData.votes_count.find(
    (vote) => vote.vote === voteCountId
  );
  return voteCount ? voteCount.vote_count ?? 0 : 0;
}

function getTotalVotes(formData) {
  let total = 0;
  formData.votes_count.forEach(function (vote_count) {
    total += vote_count.vote_count;
  });

  return total;
}

/**
 * Adds votes count and percentage to vote_fields
 */
function addVotesCount(formsData) {
  formsData.forEach(function (formData) {
    const totalVotes = getTotalVotes(formData);
    formData.total_votes = totalVotes;
    formData.vote_fields.forEach(function (vote_field) {
      const votesPerField = findVoteCountById(formData, vote_field.id);
      vote_field.votes_amount = votesPerField;
      if (votesPerField == 0) {
        vote_field.votes_percentage = 0;
      } else {
        vote_field.votes_percentage = (
          (votesPerField / totalVotes) *
          100
        ).toFixed(2);
      }
    });
  });
}

function createFormsList(formsData) {
  let forms = [];

  loadTemplateFile()
    .then((templateString) => {
      formsData.forEach(function (formData) {
        formData.created = normalizeDate(formData.created);
        formData.closing = normalizeDate(formData.closing);
        addVotesCount(formsData);
        // eslint-disable-next-line no-undef
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
