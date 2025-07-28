document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.animated-rain-bg');

    function createRaindrop() {
        const drop = document.createElement('div');
        drop.className = 'raindrop';
        const size = Math.random() * 20 + 10; // 10px - 30px
        drop.style.width = `${size}px`;
        drop.style.height = `${size}px`;
        drop.style.left = `${Math.random() * 100}%`;
        drop.style.top = `${Math.random() * 100}%`;
        container.appendChild(drop);

        setTimeout(() => {
            container.removeChild(drop);
        }, 4000); // Same as animation duration
    }

    // Drop every 300ms
    setInterval(createRaindrop, 300);
});
document.addEventListener('DOMContentLoaded', function () {
if (!document.getElementById('add-beneficiario-form')) return;

const formList = document.querySelector('#beneficiarios-form-list');
const addButton = document.querySelector('#add-beneficiario-form');
const totalForms = document.querySelector('#id_beneficiariopoliza_set-TOTAL_FORMS');
const emptyFormHtml = `{{ formset_beneficiarios.empty_form|escapejs }}`;

addButton.addEventListener('click', function () {
    let formNum = parseInt(totalForms.value);
    let newForm = emptyFormHtml.replace(/__prefix__/g, formNum);
    formList.insertAdjacentHTML('beforeend', newForm);
    totalForms.value = formNum + 1;
});
});