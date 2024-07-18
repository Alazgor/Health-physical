$(function() {
    $("#datepicker").datepicker({
        dateFormat: 'dd.mm.yy',
        changeMonth: true,
        changeYear: true
    });
});

function calculateCalories() {
    var workoutType = document.getElementById("workout_type").value;
    var duration = document.getElementById("duration").value;
    var caloriesPerMinute = {
        'bench_press': 0.106,
        'squats': 0.095,
        'deadlift': 0.125,
        'running': 0.15,
        'cycling': 0.12,
        'swimming': 0.13,
        'pull_ups': 0.1,
        'push_ups': 0.09,
        'jumping_jacks': 0.11,
        'burpees': 0.14,
        'rowing': 0.13,
        'yoga': 0.05
    };
    if (duration && caloriesPerMinute[workoutType]) {
        var calories = duration * caloriesPerMinute[workoutType];
        document.getElementById("calories").value = calories.toFixed(2);
    } else {
        document.getElementById("calories").value = '';
    }
}
