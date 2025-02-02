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

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("fitnessForm");
    const submitButton = document.getElementById("submitButton");

    function validateForm(){
        const name = document.getElementById("name").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const age = document.getElementById("age").value.trim();
        const height = document.getElementById("height").value.trim();
        const weight = document.getElementById("weight").value.trim();
        const gender = document.getElementById("gender").value.trim();

        submitButton.disabled = !(name && phone && age && height && weight && gender);
    }
    document.querySelectorAll('#name,#phone,#age,#height,#weight,#gender').forEach(input =>{
        input.addEventListener("input",validateForm);
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Retrieve values
        const name = document.getElementById("name").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const age = document.getElementById("age").value.trim();
        const height = document.getElementById("height").value.trim();
        const weight = document.getElementById("weight").value.trim();
        const gender = document.getElementById("gender").value;

        const heightInMeters = height / 100;
        const BMI = (weight / (heightInMeters ** 2)).toFixed(2);

        let status = "";
        if (BMI < 18.5) {
            status = "Underweight";
        } else if (BMI < 24.9) {
            status = "Normal weight";
        } else if (BMI < 29.9) {
            status = "Overweight";
        } else {
            status = "Obese";
        }

        const minWeight = (18.5 * (heightInMeters ** 2)).toFixed(2);
        const maxWeight = (24.9 * (heightInMeters ** 2)).toFixed(2);
        const weightDiff = (weight - ((parseFloat(minWeight) + parseFloat(maxWeight)) / 2)).toFixed(2);

        const userData = {
            name, phone, age, height, weight, gender, BMI, status, minWeight, maxWeight, weightDiff
        };

        // Store userData in localStorage
        localStorage.setItem("userData", JSON.stringify(userData));

        // Redirect to Opening.html
        window.location.href = "file:///D:/EXCIRCISE_GUIDE_FOR_BEGINEERS/OPENING_PAGE/Opening.html";
    });
});



