function sortOrder(column) {
    console.log('Sorting by:', column);

    const tableBody = document.querySelector('#table tbody');
    const rows = Array.from(tableBody.querySelectorAll('tr'));

// Toggle sort direction
    currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';

// Determine column index from column name
    const colIndex = getColumnIndex(column);

// Sort the rows
    rows.sort((a, b) => {
        let aValue = a.querySelector(`td:nth-child(${colIndex})`).innerText.trim();
        let bValue = b.querySelector(`td:nth-child(${colIndex})`).innerText.trim();

// If numeric sorting is needed
        if (['product_id', 'price', 'quantity', 'supplier_id']
            .includes(column)) {
            aValue = parseFloat(aValue) || 0;
            bValue = parseFloat(bValue) || 0;
        }

        if (currentSortOrder === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });

// Clear table body and re-append sorted rows
    tableBody.innerHTML = '';
    rows.forEach(row => tableBody.appendChild(row));
}

function getColumnIndex(column) {
// Adjust based on your table columns
// 1-based indexing in querySelector(`td:nth-child(x)`)
    switch (column) {
        case 'product_id':
            return 1;
        case 'product_name':
            return 2;
        case 'brand':
            return 3;
        case 'category_name':
            return 4;
        case 'price':
            return 5;
        case 'quantity':
            return 6;

        default:
            return 1;
    }
}