var pasword = document.getElementById("password");
var confirm_password = document.getElementById("confirm_password");

function validatePassword() {
    if (password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Passwords don't match!");
    }
    else {
        confirm_password.setCustomValidity('');
    }
    var val = password.value;
    if (val == '') {
        alert("Password cannot be blank!");
        return false;
    }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;