
function checkPasswords() {
  const pass = document.getElementById("password").value;
  const confirm = document.getElementById("confirmPassword").value;
  const msg = document.getElementById("message");

  if (confirm === "") {
    msg.textContent = "";
  } else if (pass !== confirm) {
    msg.textContent = "Passwords do not match!";
  } else {
    msg.textContent = "";
  }
}
