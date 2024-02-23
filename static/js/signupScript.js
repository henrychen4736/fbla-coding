const passwordInput = document.querySelector('#password')
const showPassword = document.querySelector('#show-password')

// Add a click event listener to the show/hide password toggle.
showPassword.addEventListener('click', function(){
    this.classList.toggle('fa-eye-slash');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type)
})