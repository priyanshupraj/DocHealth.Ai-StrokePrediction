document.addEventListener("DOMContentLoaded", function() {
    // Event listener for the form submission
    document.querySelector("#signupForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting by default

        // Get user input values
        var numEmail = document.querySelector("#numEmail").value;
        var number = document.querySelector("#number").value;
        var password = document.querySelector("#pass").value;

        // Clear input fields
        document.querySelector("#numEmail").value = "";
        document.querySelector("#number").value = "";
        document.querySelector("#pass").value = "";

        // Create a user object
        var userDetail = {
            email: numEmail,
            number: number,
            password: password,
        };

        // Retrieve existing user data from local storage or initialize an empty array
        var userData = JSON.parse(localStorage.getItem("userData")) || [];

        // Add the new user to the data array
        userData.push(userDetail);

        // Store the updated user data in local storage
        localStorage.setItem("userData", JSON.stringify(userData));

        // Alert the user and redirect to the login page
        alert("Registration successful. Please log in.");
        window.location.href = "login.html";
    });
});
