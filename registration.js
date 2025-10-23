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

      // City → Physical Address auto-fill
      const addressDisplay = document.getElementById("addressDisplay");
      const cityInput = document.getElementById("city");

      cityInput.addEventListener("input", () => {
        const city = cityInput.value.trim();
        const validCities = Array.from(document.querySelectorAll("#cities option")).map(opt => opt.value);

        if (validCities.includes(city)) {
          addressDisplay.value = "Main Street, " + city + ", Kenya";
        } else {
          addressDisplay.value = "";
        }
      });
   