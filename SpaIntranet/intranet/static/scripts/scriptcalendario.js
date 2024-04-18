// script.js
document.addEventListener('DOMContentLoaded', () => {
    const calendarDays = document.getElementById('calendar-days');
    const monthYear = document.getElementById('month-year');
    const prevMonth = document.getElementById('prev-month');
    const nextMonth = document.getElementById('next-month');
    const appointmentForm = document.getElementById('appointment-form');
    const selectedDateElement = document.getElementById('selected-date');
    const timeInput = document.getElementById('time');
    const saveAppointmentButton = document.getElementById('save-appointment');

    let currentDate = new Date();

    function renderCalendar() {
        calendarDays.innerHTML = '';
        let tempDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
        monthYear.textContent = tempDate.toLocaleDateString('es', { month: 'long', year: 'numeric' });

        while (tempDate.getMonth() === currentDate.getMonth()) {
            let dayElement = document.createElement('div');
            dayElement.textContent = tempDate.getDate();
            dayElement.onclick = () => selectDay(tempDate);
            calendarDays.appendChild(dayElement);
            tempDate.setDate(tempDate.getDate() + 1);
        }
    }

    function selectDay(date) {
        appointmentForm.style.display = 'flex';
        selectedDateElement.textContent = `Fecha seleccionada: ${date.toLocaleDateString()}`;
        timeInput.value = '';
        saveAppointmentButton.onclick = () => saveAppointment(date);
    }

    function saveAppointment(date) {
        alert(`Cita guardada para el ${date.toLocaleDateString()} a las ${timeInput.value}`);
        appointmentForm.style.display = 'none';
    }

    prevMonth.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextMonth.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    renderCalendar();
});
