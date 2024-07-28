document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('workoutTable');

    table.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const row = event.target.closest('tr');
            const date = row.children[0].innerText;
            const workoutType = row.children[1].innerText;

            // Отправка запроса на удаление на сервер
            fetch('/delete_workout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ date: date, workout_type: workoutType })
            })
            .then(response => {
                if (response.ok) {
                    // Удаление строки из таблицы
                    row.remove();
                } else {
                    alert('Не удалось удалить тренировку');
                }
            });
        }
    });
});
