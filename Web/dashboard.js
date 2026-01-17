document.addEventListener("DOMContentLoaded", () => {
    
    const workouts = [
        { date: "2026-01-03", workout: "Cardio", duration: 30, calories: 220 },
        { date: "2026-01-04", workout: "Strength", duration: 50, calories: 340 },
        { date: "2026-01-05", workout: "Yoga", duration: 60, calories: 180 },
        { date: "2026-01-06", workout: "HIIT", duration: 25, calories: 280 },
        { date: "2026-01-07", workout: "Running", duration: 40, calories: 400 },
        { date: "2026-01-08", workout: "Cycling", duration: 45, calories: 380 },
        { date: "2026-01-09", workout: "Strength", duration: 55, calories: 360 },
        { date: "2026-01-10", workout: "Cardio", duration: 35, calories: 250 },
        { date: "2026-01-11", workout: "HIIT", duration: 30, calories: 300 },
        { date: "2026-01-12", workout: "Yoga", duration: 60, calories: 190 },
        { date: "2026-01-13", workout: "Running", duration: 45, calories: 420 },
        { date: "2026-01-14", workout: "Cycling", duration: 50, calories: 400 },
        { date: "2026-01-15", workout: "Strength", duration: 60, calories: 380 },
        { date: "2026-01-16", workout: "Cardio", duration: 40, calories: 270 },
    ];

   
    document.getElementById("total-workouts").textContent = workouts.length;
    document.getElementById("total-calories").textContent = workouts.reduce((a,b)=>a+b.calories,0);
    document.getElementById("total-hours").textContent = (workouts.reduce((a,b)=>a+b.duration,0)/60).toFixed(1);

    
    const tableBody = document.getElementById("workoutsTable");
    workouts.slice(-7).forEach(w => {
        const row = `<tr>
            <td>${w.date}</td>
            <td>${w.workout}</td>
            <td>${w.duration}</td>
            <td>${w.calories}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });

   
    const ctx = document.getElementById('progressChart').getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 255, 224, 0.4)');
    gradient.addColorStop(1, 'rgba(0, 255, 224, 0)');

    const caloriesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: workouts.map(w => w.date),
            datasets: [{
                label: 'Calories Burned',
                data: workouts.map(w => w.calories),
                borderColor: '#00ffe0',
                backgroundColor: gradient,
                fill: true,
                pointBackgroundColor: '#00ffe0',
                pointBorderColor: '#fff',
                pointRadius: 6,
                pointHoverRadius: 8,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#00ffe0', font: { size: 14, weight: 'bold' } } },
                tooltip: { 
                    backgroundColor: '#1f1f1f',
                    titleColor: '#00ffe0',
                    bodyColor: '#fff',
                    titleFont: { weight: 'bold' }
                }
            },
            scales: {
                y: { beginAtZero: true, ticks: { color: '#fff' }, grid: { color: '#333' } },
                x: { ticks: { color: '#fff' }, grid: { color: '#333' } }
            }
        }
    });

    
    const durationCtx = document.getElementById('durationChart').getContext('2d');
    const durationGradient = durationCtx.createLinearGradient(0, 0, 0, 400);
    durationGradient.addColorStop(0, 'rgba(255, 99, 132, 0.4)');
    durationGradient.addColorStop(1, 'rgba(255, 99, 132, 0)');

    const durationChart = new Chart(durationCtx, {
        type: 'bar',
        data: {
            labels: workouts.map(w => w.date),
            datasets: [{
                label: 'Workout Duration (min)',
                data: workouts.map(w => w.duration),
                backgroundColor: durationGradient,
                borderColor: '#ff6384',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#ff6384', font: { size: 14 } } },
                tooltip: {
                    backgroundColor: '#1f1f1f',
                    titleColor: '#ff6384',
                    bodyColor: '#fff',
                    titleFont: { weight: 'bold' }
                }
            },
            scales: {
                y: { beginAtZero: true, ticks: { color: '#fff' }, grid: { color: '#333' } },
                x: { ticks: { color: '#fff' }, grid: { color: '#333' } }
            }
        }
    });
});
