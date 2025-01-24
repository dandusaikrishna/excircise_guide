var counter = document.querySelector(".counter")
var register = document.querySelector(".no-of-users")
let count = 0;

setInterval(() => {
    if (count < 1000) {
        count++
        counter.innerText = count;
    }
}, 0.2);


setTimeout(() => {
    register.innerText = "STAY FIT AND HEALTHY";
    register.style.fontSize = '20px';
    register.style.textAlign = 'center';
}, 5000);


// Function to check if all fields are filled
function validateForm() {
    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const age = document.getElementById("age").value.trim();
    const height = document.getElementById("height").value.trim();
    const weight = document.getElementById("weight").value.trim();
    const gender = document.getElementById("gender").value;

    // Check if all fields are filled
    if (name && phone && age && height && weight && gender) {
        document.getElementById("submitButton").disabled = false; // Enable button
    } else {
        document.getElementById("submitButton").disabled = true; // Disable button
    }
}

// Add event listeners to all fields
const formFields = document.querySelectorAll("#userForm input, #userForm select");
formFields.forEach((field) => {
    field.addEventListener("input", validateForm);
});

// Add click handler for the submit button
document.getElementById("submitButton").addEventListener("click", function () {
    if (!this.disabled) {
        window.location.href = "Opening.html"; // Redirect to Opening.html
    }
});
