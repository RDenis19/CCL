// services/static/services/js/recurso_detail.js

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    // Comprobamos si el elemento del calendario existe en la página actual
    if (calendarEl) {
        // Obtenemos los datos pasados desde el HTML
        const isStaff = calendarEl.dataset.isStaff === 'true';
        const eventsUrl = calendarEl.dataset.eventsUrl;

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: eventsUrl,
            locale: 'es',
            selectable: isStaff,
            slotDuration: '01:00:00',
            slotLabelInterval: '01:00:00',
            allDaySlot: false,
            nowIndicator: true,

            eventClick: function (info) {
                info.jsEvent.preventDefault();
                if (info.event.url) {
                    window.location.href = info.event.url;
                }
            },

            dateClick: function (info) {
                if (!isStaff) return;
                const end = new Date(info.date.getTime() + 60 * 60 * 1000);
                calendar.select(info.date, end);
            },

            select: function (info) {
                if (!isStaff) return;

                const horarioModal = new bootstrap.Modal(document.getElementById('addHorarioModal'));
                const modalTitle = document.getElementById('addHorarioModalLabel');
                const form = document.getElementById('horarioForm');
                
                // Limpiamos el formulario antes de llenarlo
                form.reset();

                // Formateamos las fechas y horas para los campos del formulario
                const startDate = info.start;
                const endDate = info.end;
                
                const startYear = startDate.getFullYear();
                const startMonth = String(startDate.getMonth() + 1).padStart(2, '0');
                const startDay = String(startDate.getDate()).padStart(2, '0');
                const startTime = startDate.toTimeString().substring(0, 5);

                const endYear = endDate.getFullYear();
                const endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
                const endDay = String(endDate.getDate()).padStart(2, '0');
                const endTime = endDate.toTimeString().substring(0, 5);
                
                // Asignamos los valores a los campos
                document.getElementById('id_fecha_hora_inicio_0').value = `${startYear}-${startMonth}-${startDay}`;
                document.getElementById('id_fecha_hora_inicio_1').value = startTime;
                document.getElementById('id_fecha_hora_fin_0').value = `${endYear}-${endMonth}-${endDay}`;
                document.getElementById('id_fecha_hora_fin_1').value = endTime;

                modalTitle.textContent = `Crear Horario el ${startDate.toLocaleDateString('es-ES', { dateStyle: 'full' })}`;
                horarioModal.show();
            }
        });

        calendar.render();
    }
});