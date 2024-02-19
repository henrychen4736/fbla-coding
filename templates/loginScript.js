const passwordInput = document.querySelector("#password")
const showPassword = document.querySelector("#show-password")

showPassword.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash");
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
    passwordInput.setAttribute("type", type)
})