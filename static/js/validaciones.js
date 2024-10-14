function validarRUT() {
    const rut = document.getElementById('rut_paciente').value.trim(); // Eliminar espacios en blanco

    // Validar que el formato del RUT sea correcto
    if (!/^\d{1,8}[-]{1}[\dkK]$/.test(rut)) {
        alert("El RUT ingresado no es válido.");
        return false;
    }

    // Separar el RUT en la parte numérica y el dígito verificador
    const rutSplit = rut.split('-');
    const rutNumeros = rutSplit[0];
    const dv = rutSplit[1].toLowerCase();

    // Algoritmo de validación del RUT chileno
    let suma = 0;
    let multiplo = 2;

    for (let i = rutNumeros.length - 1; i >= 0; i--) {
        suma += parseInt(rutNumeros[i]) * multiplo;
        multiplo = multiplo < 7 ? multiplo + 1 : 2;
    }

    const dvEsperado = 11 - (suma % 11);
    const dvCalculado = dvEsperado === 11 ? '0' : dvEsperado === 10 ? 'k' : dvEsperado.toString();

    // Comparar el dígito verificador calculado con el ingresado
    if (dv !== dvCalculado) {
        alert("El RUT ingresado no es válido.");
        return false;
    }

    return true;
}
