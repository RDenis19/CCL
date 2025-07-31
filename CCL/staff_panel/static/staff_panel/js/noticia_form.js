document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos los elementos del DOM con los que vamos a trabajar
    const toggleButton = document.getElementById('btn-toggle-new-category');
    const newCategoryGroup = document.getElementById('new-category-form-group');
    const newCategoryInput = document.getElementById('id_nueva_categoria'); // Django genera este ID
    const categorySelect = document.getElementById('id_categoria');

    // Nos aseguramos de que todos los elementos existan antes de añadir los eventos
    if (toggleButton && newCategoryGroup && newCategoryInput && categorySelect) {

        // Evento principal: clic en el botón "+"
        toggleButton.addEventListener('click', function () {
            // Alterna la clase 'd-none' para mostrar u ocultar el contenedor
            const isHidden = newCategoryGroup.classList.toggle('d-none');

            if (isHidden) {
                // Si se acaba de ocultar, limpiamos el campo para no enviar datos viejos
                newCategoryInput.value = '';
            } else {
                // Si se acaba de mostrar, es buena UX deseleccionar la categoría existente
                // para evitar el error de validación de "no ambas"
                categorySelect.value = '';
                newCategoryInput.focus(); // Ponemos el foco en el nuevo campo
            }
        });

        // Evento extra de UX: si el usuario empieza a seleccionar una categoría
        // existente, ocultamos el campo de la nueva categoría para evitar confusiones.
        categorySelect.addEventListener('change', function () {
            if (categorySelect.value) {
                newCategoryGroup.classList.add('d-none');
                newCategoryInput.value = '';
            }
        });
    }
});