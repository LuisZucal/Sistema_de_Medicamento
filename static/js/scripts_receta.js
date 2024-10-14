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
                tipoSelect.append('<option value="' + tipo.id_tipo + '">' + tipo.nombre_tipo + '</option>');
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
    const tipoMedicamento = document.getElementById('tipo-medicamento').value;
    const medicamentoContainer = document.getElementById('medicamento-container');
    const medicamentoSelect = document.getElementById('medicamento');

    medicamentoSelect.innerHTML = '<option value="">Seleccione un medicamento</option>';

    if (tipoMedicamento) {
        medicamentoContainer.style.display = 'block';

        // Realiza la llamada AJAX para obtener los medicamentos según el tipo seleccionado
        fetch(`/medicamentos/${tipoMedicamento}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(medicamento => {
                    const option = document.createElement('option');
                    option.value = medicamento.id;
                    option.textContent = medicamento.nombre; // Solo mostrar el nombre
                    medicamentoSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error al obtener medicamentos:', error);
                alert('No se pudieron cargar los medicamentos. Intente de nuevo.');
            });
    } else {
        medicamentoContainer.style.display = 'none';
    }
}

let medicamentosCargados = [];  // Array temporal para almacenar medicamentos

function cargarMedicamento() {
    const medicamentoSelect = document.getElementById('medicamento');
    const medicamentoNombre = medicamentoSelect.options[medicamentoSelect.selectedIndex].text;
    const cantidad = document.getElementById('cantidad').value;

    if (!medicamentoSelect.value) {
        alert('Por favor, seleccione un medicamento.');
        return;
    }

    if (!cantidad || cantidad <= 0) {
        alert('Ingrese una cantidad válida.');
        return;
    }

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
    const rut = entregaTerceroCheckbox.checked ? document.getElementById('rut').value.trim() : '{{ paciente.Rut }}';
    const nombre = entregaTerceroCheckbox.checked ? document.getElementById('nombre').value.trim() : '{{ paciente.Nombre }}';
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
        medicamentos: medicamentosCargados
    };

    // Realizar la llamada AJAX para entregar medicamentos
    $.ajax({
        url: '/entregar_medicamentos',  // Asegúrate de que esta URL sea correcta en tu backend
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(entregaData),
        success: function () {
            mostrarMensaje();  // Mostrar el mensaje de éxito
            medicamentosCargados = [];  // Limpiar la lista de medicamentos cargados
            document.getElementById('medicamentos').innerHTML = ''; // Limpiar la lista visualizada
        },
        error: function () {
            alert('Error al entregar los medicamentos. Por favor, intente de nuevo.');
        }
    });
}
