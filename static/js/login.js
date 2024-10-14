function togglePassword() {
    var passwordField = document.getElementById('contrasena');
    var passwordToggle = document.getElementById('password-toggle');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        passwordToggle.textContent = 'Ocultar';
    } else {
        passwordField.type = 'password';
        passwordToggle.textContent = 'Mostrar';
    }
}
