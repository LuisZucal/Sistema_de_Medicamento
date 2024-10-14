// Mostrar el campo de especialización solo si se selecciona Doctor
document.getElementById('tipo_usuario').addEventListener('change', function() {
    var especializacionGroup = document.getElementById('especializacion-group');
    if (this.value === 'doctor') {
        especializacionGroup.style.display = 'block';
    } else {
        especializacionGroup.style.display = 'none';
        document.getElementById('especializacion').value = ''; // Limpiar el campo
    }
});
