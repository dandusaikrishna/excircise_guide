document.addEventListener("DOMContentLoaded", function () {
    const userData = JSON.parse(localStorage.getItem("userData"));

    if (userData) {
        document.getElementById("userName").textContent = `Hello, ${userData.name}`;
        document.getElementById("age").textContent = userData.age;
        document.getElementById("height").textContent = userData.height;
        document.getElementById("weight").textContent = userData.weight;
        document.getElementById("BMI").textContent = userData.BMI;
        document.getElementById("status").textContent = userData.status;
        document.getElementById("minWeight").textContent = userData.minWeight;
        document.getElementById("weightDiff").textContent = userData.weightDiff;
    } else {
        console.log("No user data found in localStorage.");
    }
});
