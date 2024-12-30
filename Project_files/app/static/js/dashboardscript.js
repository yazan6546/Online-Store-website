// Revenue Chart
const revenueCtx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenueCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
            {
                label: 'This Year',
                data: [12000, 15000, 13000, 16000, 14000, 18000, 17000, 20000, 22000, 24000, 26000, 28000],
                borderColor: '#007AFF',
                backgroundColor: 'rgba(0, 122, 255, 0.1)',
                fill: true,
                tension: 0.4,
            },
            {
                label: 'Last Year',
                data: [10000, 12000, 11000, 14000, 13000, 15000, 14000, 17000, 19000, 20000, 23000, 25000],
                borderColor: '#FFD322',
                backgroundColor: 'rgba(255, 211, 34, 0.1)',
                fill: true,
                tension: 0.4,
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
        },
        scales: {
            y: {
                beginAtZero: true,
            },
        },
    },
});
