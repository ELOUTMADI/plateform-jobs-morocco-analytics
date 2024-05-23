const usernameField = document.querySelector('#username');
const feedbackAreaUser = document.querySelector('.invalid-feedbackUser');

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  feedbackAreaUser.style.display = "none";
  usernameField.classList.remove("is-invalid");
  feedbackAreaUser.classList.remove("text-danger");

  if (usernameVal.length > 0) {
    fetch('/authentification/validate-username', {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("data", data);
      if (data.username_error) {
        feedbackAreaUser.classList.add("is-invalid");
        usernameField.classList.add("is-invalid");
        feedbackAreaUser.classList.add("text-danger");
        feedbackAreaUser.style.display = "block";
        feedbackAreaUser.innerHTML = `<p>${data.username_error}</p>`;
      }
    });
  }
});

const emailField = document.querySelector('#email');
const feedbackAreaEmail = document.querySelector('.invalid-feedbackEmail');

emailField.addEventListener("keyup", (e) => {
  const EmailVal = e.target.value;
  feedbackAreaEmail.style.display = "none";
  emailField.classList.remove("is-invalid");
  feedbackAreaEmail.classList.remove("text-danger");

  if (EmailVal.length > 0) {
    fetch('/authentification/validate-email', {
      body: JSON.stringify({ email: EmailVal }),
      method: "POST",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("data", data);
      if (data.email_error) {
        feedbackAreaEmail.classList.add("is-invalid");
        emailField.classList.add("is-invalid");
        feedbackAreaEmail.classList.add("text-danger");
        feedbackAreaEmail.style.display = "block";
        feedbackAreaEmail.innerHTML = `<p>${data.email_error}</p>`;
      }
    });
  }
});