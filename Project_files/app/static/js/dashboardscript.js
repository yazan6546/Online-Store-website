// Initialize the chart
const ctx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: []
    },
    options: {
        responsive: true,
        scales: {
            x: {
                beginAtZero: true
            },
            y: {
                beginAtZero: true
            }
        }
    }
});

// Define a fixed set of colors
const colors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
    '#E7E9ED', '#76D7C4', '#F7DC6F', '#F1948A', '#85C1E9', '#BB8FCE'
];

async function fetchRevenues() {
    try {
        const response = await fetch('/api/revenues');
        const data = await response.json();

        // Process the data to fit the chart format
        const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const datasets = Object.keys(data).map((year, index) => ({
            label: year,
            data: labels.map((_, monthIndex) => {
                const monthData = data[year].find(item => item.month === monthIndex + 1);
                return monthData ? monthData.total_revenue : 0;
            }),
            borderColor: colors[index % colors.length],
            backgroundColor: colors[index % colors.length] + '33',
            fill: true,
            tension: 0.4,
        }));

        // Update the chart
        revenueChart.data.datasets = datasets;
        revenueChart.update();
    } catch (error) {
        console.error('Error fetching revenues:', error);
    }
}

// Call the function to fetch and process the data
fetchRevenues();