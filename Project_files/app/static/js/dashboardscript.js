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


function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

document.addEventListener('DOMContentLoaded', () => {
    const countCustomersElement = document.getElementById('count_customers');
    const countProductsElement = document.getElementById('count_products');
    const countOrdersElement = document.getElementById('count_orders');
    const totalRevenueElement = document.getElementById('total_revenue');

    animateValue(countCustomersElement, 0, parseInt(countCustomersElement.innerText), 500);
    animateValue(countProductsElement, 0, parseInt(countProductsElement.innerText), 500);
    animateValue(countOrdersElement, 0, parseInt(countOrdersElement.innerText), 500);
    animateValue(totalRevenueElement, 0, parseInt(totalRevenueElement.innerText), 500);
});

// Initialize the category chart
const ctxCategory = document.getElementById('categoryChart').getContext('2d');
const categoryChart = new Chart(ctxCategory, {
    type: 'pie',
    data: {
        labels: ['Electronics', 'Clothing', 'Home Appliances', 'Books', 'Toys'],
        datasets: [{
            data: [30, 20, 15, 25, 10],
            backgroundColor: [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
    '#E7E9ED', '#76D7C4', '#F7DC6F', '#F1948A', '#85C1E9', '#BB8FCE',
    '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFA1',
    '#FF8C00', '#8B0000', '#008B8B', '#B8860B', '#A9A9A9', '#2F4F4F'
    ]
        }]
    },
    options: {
        responsive: true
    }
});


async function fetchCategoryData() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        // Process the data to fit the chart format
        const labels = data.map(item => item.category_name);
        const datasetData = data.map(item => item.total_quantity_sold);

        // Update the chart
        categoryChart.data.labels = labels;
        categoryChart.data.datasets[0].data = datasetData;
        categoryChart.update();
    } catch (error) {
        console.error('Error fetching category data:', error);
    }
}


// Define a fixed set of colors
const colors1 = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
    '#E7E9ED', '#76D7C4', '#F7DC6F', '#F1948A', '#85C1E9', '#BB8FCE',
    '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFA1',
    '#FF8C00', '#8B0000', '#008B8B', '#B8860B', '#A9A9A9', '#2F4F4F'
];



// Initialize the top customers chart
const ctxTopCustomers = document.getElementById('topCustomersChart').getContext('2d');
const topCustomersChart = new Chart(ctxTopCustomers, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Amount Paid',
            data: [],
            backgroundColor: colors1.slice(0, 10) // Use the first 10 colors
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                beginAtZero: true
            }
        }
    }
});

// Dummy data for top customers
const dummyData = [
    {"first_name": "John", "last_name": "Doe", "amount_paid": 1500.00},
    {"first_name": "Jane", "last_name": "Smith", "amount_paid": 1400.00},
    {"first_name": "Alice", "last_name": "Johnson", "amount_paid": 1300.00},
    {"first_name": "Bob", "last_name": "Brown", "amount_paid": 1200.00},
    {"first_name": "Charlie", "last_name": "Davis", "amount_paid": 1100.00},
    {"first_name": "Diana", "last_name": "Miller", "amount_paid": 1000.00},
    {"first_name": "Eve", "last_name": "Wilson", "amount_paid": 900.00},
    {"first_name": "Frank", "last_name": "Moore", "amount_paid": 800.00},
    {"first_name": "Grace", "last_name": "Taylor", "amount_paid": 700.00},
    {"first_name": "Hank", "last_name": "Anderson", "amount_paid": 600.00}
];
async function fetchTopCustomersData() {
    try {

        const response = await fetch('/api/best_customers');
        const data = await response.json();


        // Log the data to verify its format
        console.log('Fetched top customers data:', data);

        // Process the dummy data to fit the chart format
        const labels = data.map(item => `${item.first_name} ${item.last_name}`);
        const datasetData = data.map(item => item.total_paid);

        console.log('Processed labels:', labels);
        console.log('Processed dataset data:', datasetData);

        // Update the chart with dummy data
        topCustomersChart.data.labels = labels;
        topCustomersChart.data.datasets[0].data = datasetData;
        topCustomersChart.update();

    } catch (error) {
        console.error('Error fetching top customers data:', error);
    }
}



// async function fetchTopCustomersData() {
//     try {
//         const response = await fetch('/api/top_customers');
//         const data = await response.json();
//
//         // Process the data to fit the chart format
//         const labels = data.map(item => `${item.first_name} ${item.last_name}`);
//         const datasetData = data.map(item => item.amount_paid);
//
//         // Update the chart
//         topCustomersChart.data.labels = labels;
//         topCustomersChart.data.datasets[0].data = datasetData;
//         topCustomersChart.update();
//     } catch (error) {
//         console.error('Error fetching top customers data:', error);
//     }
// }
//
//
// // Call the function to fetch and process the data
fetchTopCustomersData();

// Call the function to fetch and process the data
fetchCategoryData();


// Call the function to fetch and process the data
fetchRevenues();