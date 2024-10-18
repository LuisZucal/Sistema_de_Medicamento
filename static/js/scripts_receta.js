$(document).ready(function () {
    // Cargar tipos de medicamentos al cargar la página
    $.ajax({
        url: '/tipo_medicamento',
        type: 'GET',
        success: function (data) {
            const tipoSelect = $('#tipo-medicamento');
            tipoSelect.empty(); // Limpiar opciones anteriores
            tipoSelect.append('<option value="">Seleccione un tipo</option>'); // Opción por defecto

            // Iterar sobre los tipos de medicamento y añadirlos al combo box
            $.each(data.tipos_medicamentos, function (index, tipo) {
                tipoSelect.append(`<option value="${tipo.id_tipo}">${tipo.nombre_tipo}</option>`);
            });
        },
        error: function () {
            alert('Error al cargar los tipos de medicamento.');
        }
    });
});

function mostrarMensaje() {
    document.getElementById('mensaje').style.display = 'block';
}

function toggleFields() {
    const entregaTerceroCheckbox = document.getElementById('entrega_tercero');
    const rutNombreContainer = document.getElementById('rut-nombre-container');

    // Mostrar u ocultar el contenedor de RUT y Nombre
    rutNombreContainer.style.display = entregaTerceroCheckbox.checked ? 'block' : 'none';
}

function showMedicamentos() {
    const tipoId = $('#tipo-medicamento').val();  // Obtener el tipo seleccionado
    const medicamentoSelect = $('#medicamento');

    if (tipoId) {
        $.ajax({
            url: `/medicamentos/${tipoId}`,  // Llamada a la API para obtener medicamentos
            method: 'GET',
            success: function (data) {
                medicamentoSelect.empty();  // Limpiar opciones anteriores
                medicamentoSelect.append('<option value="">Seleccione un medicamento</option>'); // Opción por defecto

                // Iterar sobre los medicamentos y añadirlos al combo box
                $.each(data, function (index, medicamento) {
                    medicamentoSelect.append(`<option value="${medicamento.MedicamentoID}">${medicamento.Nombre}</option>`);
                });
                $('#medicamento-container').show();  // Mostrar el contenedor de medicamentos
            },
            error: function () {
                alert('Error al cargar medicamentos.');
            }
        });
    } else {
        $('#medicamento-container').hide();  // Ocultar si no se selecciona un tipo
    }
}

let medicamentosCargados = [];  // Array temporal para almacenar medicamentos

function cargarMedicamento() {
    const medicamentoSelect = document.getElementById('medicamento');
    const medicamentoNombre = medicamentoSelect.options[medicamentoSelect.selectedIndex].text;
    const cantidad = document.getElementById('cantidad').value;

    // Validaciones
    if (!medicamentoSelect.value) {
        alert('Por favor, seleccione un medicamento.');
        return;
    }

    if (!cantidad || cantidad <= 0) {
        alert('Ingrese una cantidad válida.');
        return;
    }

    // Crear y mostrar el nuevo elemento de medicamento
    const medicamentosDiv = document.getElementById('medicamentos');
    const newMedicamento = document.createElement('div');
    newMedicamento.textContent = `${medicamentoNombre} - Cantidad: ${cantidad}`;
    medicamentosDiv.appendChild(newMedicamento);

    // Agregar el medicamento cargado al array temporal
    medicamentosCargados.push({ nombre: medicamentoNombre, cantidad: cantidad });

    // Limpiar el campo de cantidad después de cargar el medicamento
    document.getElementById('cantidad').value = '';
}

function entregarMedicamentos() {
    // Validar si la entrega es para un tercero
    const entregaTerceroCheckbox = document.getElementById('entrega_tercero');
    const rut = entregaTerceroCheckbox.checked ? document.getElementById('rut').value.trim() : '';
    const nombre = entregaTerceroCheckbox.checked ? document.getElementById('nombre').value.trim() : '';
    const fecha = document.getElementById('fecha').value; // Mantener la fecha sin cambios

    // Validaciones
    if (!fecha) {
        alert('Por favor, seleccione una fecha.');
        return;
    }

    if (entregaTerceroCheckbox.checked && (!rut || !nombre)) {
        alert('Por favor, complete el RUT y Nombre del tercero.');
        return;
    }

    if (medicamentosCargados.length === 0) {
        alert('No hay medicamentos cargados para entregar.');
        return;
    }

    // Crear un objeto con la información de entrega
    const entregaData = {
        rut: rut,
        nombre: nombre,
        fecha: fecha,
        medicamentos: medicamentosCargados  // Enviar el array de medicamentos
    };

    // Mostrar datos enviados para depuración
    console.log(entregaData);

    // Realizar la llamada AJAX para entregar medicamentos
    $.ajax({
        url: '/entregar_medicamentos',  // Asegúrate de que esta URL sea correcta en tu backend
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(entregaData),
        success: function (response) {
            alert(response.message);  // Mostrar el mensaje de éxito
            medicamentosCargados = [];  // Limpiar la lista de medicamentos cargados
            document.getElementById('medicamentos').innerHTML = ''; // Limpiar la lista visualizada

            // Redirigir a dashboard_farmaceutico después de la entrega exitosa
            window.location.href = '/dashboard_farmaceutico'; 
        },
        error: function (xhr) {
            alert('Error al entregar los medicamentos: ' + xhr.responseJSON.error); // Mostrar mensaje de error
        }
    });
}

