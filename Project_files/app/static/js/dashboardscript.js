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

// Define a fixed set of 12 colors
const colors2 = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
    '#E7E9ED', '#76D7C4', '#F7DC6F', '#F1948A', '#85C1E9', '#BB8FCE'
];

// Initialize the chart
const ctxBar = document.getElementById('coloredBarChart').getContext('2d');
const coloredBarChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: [], // To be filled with the month of input data
        datasets: [{
            label: 'Total Quantity Sold', // Customize the label as needed
            data: [], // To be filled with the total_quantity_sold of input data
            backgroundColor: colors2 // Use the defined colors
        }]
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

// Function to process input data and update the chart
function updateChartData(inputData) {
    // Assuming inputData is an array of objects with 3 columns
    const labels = inputData.map(item => item.month);
    const datasetData = inputData.map(item => item.total_quantity_sold);

    // Update the chart data
    coloredBarChart.data.labels = labels;
    coloredBarChart.data.datasets[0].data = datasetData;
    coloredBarChart.update();
}

// Example input data
const inputData = [
    { month: '2023-01', product_name: 'time', total_quantity_sold: 26.0 },
    { month: '2023-02', product_name: 'image', total_quantity_sold: 28.0 },
    { month: '2023-03', product_name: 'blue', total_quantity_sold: 22.0 },
    { month: '2023-04', product_name: 'former', total_quantity_sold: 26.0 },
    { month: '2023-05', product_name: 'half', total_quantity_sold: 29.0 },
    { month: '2023-06', product_name: 'represent', total_quantity_sold: 25.0 },
    { month: '2023-07', product_name: 'five', total_quantity_sold: 25.0 },
    { month: '2023-08', product_name: 'option', total_quantity_sold: 29.0 },
    { month: '2023-09', product_name: 'environmental', total_quantity_sold: 41.0 },
    { month: '2023-10', product_name: 'mean', total_quantity_sold: 30.0 },
    { month: '2023-11', product_name: 'theory', total_quantity_sold: 25.0 },
    { month: '2023-12', product_name: 'scientist', total_quantity_sold: 25.0 }
];

// Update the chart with the example input data
updateChartData(inputData);


// // Call the function to fetch and process the data
fetchTopCustomersData();

// Call the function to fetch and process the data
fetchCategoryData();


// Call the function to fetch and process the data
fetchRevenues();