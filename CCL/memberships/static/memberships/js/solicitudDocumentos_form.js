document.addEventListener('DOMContentLoaded', function () {

    function setupFormset(formsetName) {
        const addButton = document.getElementById(`add-${formsetName}-form`);
        if (!addButton) return;

        const formList = document.getElementById(`${formsetName}s-form-list`);
        const totalFormsInput = document.querySelector(`#id_${formsetName}s-TOTAL_FORMS`);
        const emptyFormTemplate = document.getElementById(`empty-${formsetName}-form`);

        if (!formList || !totalFormsInput || !emptyFormTemplate) return;

        addButton.addEventListener('click', function () {
            const newIndex = parseInt(totalFormsInput.value);
            // Reemplaza el prefijo '__prefix__' con el nuevo índice
            const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, newIndex);

            // Crea un div temporal para añadir la nueva fila de formulario
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = newFormHtml;

            // Añade la nueva fila al final de la lista
            formList.appendChild(tempDiv.firstElementChild);

            // Incrementa el contador del management form
            totalFormsInput.value = newIndex + 1;
        });
    }

    // Inicializa la funcionalidad para ambos formsets
    setupFormset('beneficiario');
    setupFormset('documento');

});