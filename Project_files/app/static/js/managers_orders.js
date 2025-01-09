let currentSortOrder = 'asc'; // Keeps track of the current sort order

function sortManagersOrders(column) {
    console.log('Sorting by:', column);

    // Get the table body and convert rows to an array
    const tableBody = document.querySelector('#table tbody');
    const rows = Array.from(tableBody.querySelectorAll('tr'));

    // Determine the sort direction
    currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';

    // Sort rows based on the specified column
    rows.sort((a, b) => {
        let aValue = a.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.trim();
        let bValue = b.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.trim();

        // Handle numeric sorting for `supplier_id`
        if (column === 'order_id') {
            aValue = parseInt(aValue, 10);
            bValue = parseInt(bValue, 10);
        }
        else if (column === 'order_date' || column === 'delivery_date') {
        aValue = new Date(aValue);
        bValue = new Date(bValue);
        }

        if (currentSortOrder === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });

    // Clear the table body and append sorted rows
    tableBody.innerHTML = '';
    rows.forEach(row => tableBody.appendChild(row));
}

// Utility to map column names to their respective indices
function getColumnIndex(column) {
    switch (column) {
        case 'order_id':
            return 1; // 1st column
        case 'manager_email':
            return 2; // 2nd column
        case 'order_date':
            return 3; // 3rd column
        case 'delivery_date':
            return 4; // 4th column
        case 'delivery_service_name':
            return 5; // 5th column
        case 'order_status':
            return 6; // 6th column
        default:
            return 1;
    }
}

function generateRow(order) {
// console.log(product);
// console.log(categories);
// console.log(suppliers);
return `
<tr id="row-${ order.order_id }">

                <td>${ order.order_id }</td>
                <td>
                    <span id="email-${ order.order_id }-text"> ${ order.email } </span>

                </td>
                <td>
                    <span id="order_date-${ order.order_id }-text">${ order.order_date }</span>
                    <input type="text" id="order_date-${ order.order_id }-input" value="${ order.order_date }" style="display:none; width: 100px;">
                </td>

                <td>
                    <span id="delivery_date-${ order.order_id }-text">${ order.delivery_date }</span>
                    <input type="text" id="delivery_date-${ order.order_id }-input" value="${ order.delivery_date }" style="display:none; width: 100px;">

                </td>

                <td>
                    <span id="delivery_service_name-${ order.order_id }-text">${ order.delivery_service_name }</span>
                    <input type="text" id="delivery_service_name-${ order.order_id }-input" value="${ order.delivery_service_name }" style="display:none; width: 100px;">
                </td>

                <td>
                    <span id="order_status-${ order.order_id }-text">${ order.order_status }</span>
                    <input type="text" id="order_status-${ order.order_id }-input" value="${ order.order_status }" style="display:none; width: 100px;">

                <td class="action-buttons">
                    <button id="edit-btn-${ order.order_id  }" class="edit" onclick="enableEditManagersOrders(${ order.order_id })">Edit</button>
                    <button id="save-btn-${ order.order_id  }" class="save" style="display:none;" onclick="saveEditManagersOrders(${ order.order_id })">Save</button>
                    <button class="delete" onclick="deleteManagerOrder(${order.order_id })">Cancel</button>
                </td>

            </tr>`;
}


function enableEditManagersOrders(supplier_id) {
    console.log('Enabling edit for supplier ID:', supplier_id);
    var row = document.getElementById('row-' + supplier_id);
    row.classList.add('edit-mode');
    document.getElementById('name-' + supplier_id + '-text').style.display = 'none';
    document.getElementById('name-' + supplier_id + '-input').style.display = 'inline';
    document.getElementById('phone-' + supplier_id + '-text').style.display = 'none';
    document.getElementById('phone-' + supplier_id + '-input').style.display = 'inline';
    document.getElementById('save-btn-' + supplier_id).style.display = 'inline';
    document.getElementById('edit-btn-' + supplier_id).style.display = 'none';
}

function saveEditManagersOrders(supplier_id) {
    console.log('Saving edit for supplier ID:', supplier_id);
    var name = $('#name-' + supplier_id + '-input').val();
    var phone = $('#phone-' + supplier_id + '-input').val();
    $.ajax({
        url: '/update_supplier/' + supplier_id,
        type: 'POST',
        data: {
            name: name,
            phone: phone
        },
        success: function(response) {
            if (response.success) {
                $('#name-' + supplier_id + '-text').text(name).show();
                $('#name-' + supplier_id + '-input').hide();
                $('#phone-' + supplier_id + '-text').text(phone).show();
                $('#phone-' + supplier_id + '-input').hide();
                $('#edit-btn-' + supplier_id).show();
                $('#save-btn-' + supplier_id).hide();
            } else {
                alert('Error updating supplier: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error updating supplier: ' + xhr.responseText);
        }
    });
}

function deleteManagerOrder(order_id) {
    console.log('Deleting order ID:', order_id);
    if (confirm('Are you sure you want to cancel this order?')) {
        $.ajax({
            url: '/delete_managers_orders/' + order_id,
            type: 'POST',
            success: function(response) {
                if (response.success) {
                    // $('#row-' + order_id).remove();
                    $('#order_status-' + order_id + '-text').text("CANCELLED").show();
                } else {
                    alert('Error deleting Order: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Error deleting Order: ' + xhr.responseText);
            }
        });
    }
}

function searchManagersOrders() {
    console.log('Searching orders');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_managers_orders',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.orders.forEach(function(order) {
                    var row = generateRow(order);
                    tableBody.append(row);
                });
            } else {
                alert('Error searching orders: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error searching orders: ' + xhr.responseText);
        }
    });
}
/////////////////////////////////////////////////////////////////////////

// Open the modal
// function openModal() {
//     document.getElementById('add-supplier-modal').style.display = 'block';
//
// }
//
// // Close the modal
// function closeModal() {
//     document.getElementById('add-supplier-modal').style.display = 'none';
//     // Clear form inputs
//     document.getElementById('supplier-name').value = '';
//     document.getElementById('supplier-phone').value = '';
// }


function openModal() {
    const modal = document.getElementById("add-supplier-modal");
    modal.classList.add("show");
}

function closeModal() {
    const modal = document.getElementById("add-supplier-modal");
    modal.classList.remove("show");
}

let currentPage = 1;
const limit = 10; // Rows per page

// Fetch suppliers and update the table
async function fetchManagersOrders(page = 1) {
    try {
        const response = await fetch(`/get_managers_orders?page=${page}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            // Update the table
            const tableBody = document.querySelector('#table tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            data.orders.forEach(order => {
                const newRow = generateRow(order);
                tableBody.innerHTML += newRow;
            });

            // Update pagination controls
            document.getElementById('currentPage').innerText = `Page ${data.page}`;
            document.getElementById('prevPage').disabled = data.page === 1;
            document.getElementById('nextPage').disabled = data.page * limit >= data.total_count;
        } else {
            console.error('Error fetching suppliers:', data.error);
        }
    } catch (error) {
        console.error('Error fetching suppliers:', error);
    }
}

// Add supplier and refresh the table
function addManagersOrders() {
    const name = document.getElementById('supplier-name').value;
    const phone = document.getElementById('supplier-phone').value;

    // Validate inputs
    if (!name || !phone) {
        alert('Please fill in all fields.');
        return;
    }

    // Send data to the server
    fetch('/add_supplier', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, phone }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Supplier added successfully!');
                closeModal(); // Close the modal
                fetchSuppliers(currentPage); // Refresh the current page
            } else {
                alert('Error adding supplier: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the supplier.');
        });
}

// Event Listeners for Pagination
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchSuppliers(currentPage);
    }
});

document.getElementById('nextPage').addEventListener('click', () => {
    currentPage++;
    fetchSuppliers(currentPage);
});

// Initial Fetch
fetchManagersOrders(currentPage);


