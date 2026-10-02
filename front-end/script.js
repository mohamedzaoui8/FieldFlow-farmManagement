document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector("#loginForm");

  loginForm?.addEventListener("submit", (event) => {
    event.preventDefault();

    const email = document.querySelector("#loginEmail").value;
    const password = document.querySelector("#loginPassword").value;

    console.log({ email, password });

    document.querySelector("#loginView").style.display = "none";
    document.querySelector("#appShell").style.display = "flex";
  });
});