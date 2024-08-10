document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    const usernameInput = document.getElementById('id_username');
    const usernameError = document.createElement('div');
    usernameError.className = 'invalid-feedback';
    usernameError.style.display = 'none'; // Initially hide the error
    usernameInput.parentNode.appendChild(usernameError);

    function validateUsername() {
        const username = usernameInput.value;
        const minLength = 3;
        const maxLength = 14;

        if (username.length < minLength || username.length > maxLength) {
            usernameInput.classList.add('is-invalid');
            usernameError.textContent = `Username must be between ${minLength} and ${maxLength} characters.`;
            usernameError.style.display = 'block';
            return false;
        } else {
            usernameInput.classList.remove('is-invalid');
            usernameError.style.display = 'none';
            return true;
        }
    }

    usernameInput.addEventListener('input', validateUsername);

    form.addEventListener('submit', function(event) {
        if (!validateUsername()) {
            event.preventDefault(); // Prevent form submission if there's an error
        }
    });
});
