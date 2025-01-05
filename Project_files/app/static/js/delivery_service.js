let currentSortOrder = 'asc'; // Keeps track of the current sort order

function sortDelivery(column) {
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

        // Handle numeric sorting for `delivery_service_id`
        if (column === 'delivery_service_id') {
            aValue = parseInt(aValue, 10);
            bValue = parseInt(bValue, 10);
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
        case 'delivery_service_id':
            return 1; // 1st column
        case 'name':
            return 2; // 2nd column
        case 'phone':
            return 3; // 3rd column
        default:
            return 1;
    }
}



function enableEditDelivery(delivery_service_id) {
    console.log('Enabling edit for delivery service ID:', delivery_service_id);
    var row = document.getElementById('row-' + delivery_service_id);
    row.classList.add('edit-mode');
    document.getElementById('name-' + delivery_service_id + '-text').style.display = 'none';
    document.getElementById('name-' + delivery_service_id + '-input').style.display = 'inline';
    document.getElementById('phone-' + delivery_service_id + '-text').style.display = 'none';
    document.getElementById('phone-' + delivery_service_id + '-input').style.display = 'inline';
    document.getElementById('save-btn-' + delivery_service_id).style.display = 'inline';
    document.getElementById('edit-btn-' + delivery_service_id).style.display = 'none';
}

function saveEditDelivery(delivery_service_id) {
    console.log('Saving edit for delivery service ID:', delivery_service_id);
    var name = $('#name-' + delivery_service_id + '-input').val();
    var phone = $('#phone-' + delivery_service_id + '-input').val();
    $.ajax({
        url: '/update_delivery/' + delivery_service_id,
        type: 'POST',
        data: {
            name: name,
            phone: phone
        },
        success: function(response) {
            if (response.success) {
                $('#name-' + delivery_service_id + '-text').text(name).show();
                $('#name-' + delivery_service_id + '-input').hide();
                $('#phone-' + delivery_service_id + '-text').text(phone).show();
                $('#phone-' + delivery_service_id + '-input').hide();
                $('#edit-btn-' + delivery_service_id).show();
                $('#save-btn-' + delivery_service_id).hide();
            } else {
                alert('Error updating delivery service: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error updating delivery service: ' + xhr.responseText);
        }
    });
}

function deleteDelivery(delivery_service_id) {
    console.log('Deleting delivery service ID:', delivery_service_id);
    if (confirm('Are you sure you want to delete this delivery service?')) {
        $.ajax({
            url: '/delete_delivery/' + delivery_service_id,
            type: 'POST',
            success: function(response) {
                if (response.success) {
                    $('#row-' + delivery_service_id).remove();
                } else {
                    alert('Error deleting delivery service: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Error deleting delivery service: ' + xhr.responseText);
            }
        });
    }
}

function searchDelivery() {
    console.log('Searching delivery services...');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_delivery',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.delivery_services.forEach(function(delivery) {
                    var row = `
                        <tr id="row-${delivery.delivery_service_id}">
                            <td>${delivery.delivery_id}</td>
                            <td>
                                <span id="name-${delivery.delivery_service_id}-text">${delivery.delivery_service_name}</span>
                                <input type="text" id="name-${delivery.delivery_service_id}-input" value="${delivery.delivery_service_name}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="phone-${delivery.delivery_service_id}-text">${delivery.phone_number}</span>
                                <input type="text" id="phone-${delivery.delivery_service_id}-input" value="${delivery.phone_number}" style="display:none; width: 100px;">
                            </td>
                            <td class="action-buttons">
                                <button id="edit-btn-${delivery.delivery_service_id}" class="edit" onclick="enableEditDelivery(${delivery.delivery_service_id})">Edit</button>
                                <button id="save-btn-${delivery.delivery_service_id}" class="save" style="display:none;" onclick="saveEditDelivery(${delivery.delivery_service_id})">Save</button>
                                <button class="delete" onclick="deleteDelivery(${delivery.delivery_service_id})">Delete</button>
                            </td>
                        </tr>`;
                    tableBody.append(row);
                });
            } else {
                alert('Error searching delivery service: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error searching delivery service: ' + xhr.responseText);
        }
    });
}


function openModal() {
    const modal = document.getElementById("add-delivery-modal");
    modal.classList.add("show");
}

function closeModal() {
    const modal = document.getElementById("add-delivery-modal");
    modal.classList.remove("show");
}

let currentPage = 1;
const limit = 8; // Rows per page

// Fetch delivery services and update the table
async function fetchDelivery(page = 1) {
    try {
        const response = await fetch(`/get_delivery?page=${page}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            // Update the table
            const tableBody = document.querySelector('#table tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            data.delivery_services.forEach(delivery => {
                const newRow = `
                    <tr id="row-${delivery.delivery_service_id}">
                        <td>${delivery.delivery_service_id}</td>
                        <td>
                            <span id="name-${delivery.delivery_service_id}-text">${delivery.delivery_service_name}</span>
                            <input type="text" id="name-${delivery.delivery_service_id}-input" value="${delivery.delivery_service_name}" style="display:none; width: 100px;">
                        </td>
                        <td>
                            <span id="phone-${delivery.delivery_service_id}-text">${delivery.phone_number}</span>
                            <input type="text" id="phone-${delivery.delivery_service_id}-input" value="${delivery.phone_number}" style="display:none; width: 100px;">
                        </td>
                        <td class="action-buttons">
                            <button id="edit-btn-${delivery.delivery_service_id}" class="edit" onclick="enableEditDelivery(${delivery.delivery_service_id})">Edit</button>
                            <button id="save-btn-${delivery.delivery_service_id}" class="save" style="display:none;" onclick="saveEditDelivery(${delivery.delivery_service_id})">Save</button>
                            <button class="delete" onclick="deleteDelivery(${delivery.delivery_service_id})">Delete</button>
                        </td>
                    </tr>`;
                tableBody.innerHTML += newRow;
            });

            // Update pagination controls
            document.getElementById('currentPage').innerText = `Page ${data.page}`;
            document.getElementById('prevPage').disabled = data.page === 1;
            document.getElementById('nextPage').disabled = data.page * limit >= data.total_count;
        } else {
            console.error('Error fetching delivery service:', data.error);
        }
    } catch (error) {
        console.error('Error fetching delivery service:', error);
    }
}

// Add delivery service and refresh the table
function addDelivery() {
    const name = document.getElementById('delivery-name').value;
    const phone = document.getElementById('delivery-phone').value;

    // Validate inputs
    if (!name || !phone) {
        alert('Please fill in all fields.');
        return;
    }

    // Send data to the server
    fetch('/add_delivery', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, phone }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Delivery service added successfully!');
                closeModal(); // Close the modal
                fetchDelivery(currentPage); // Refresh the current page
            } else {
                alert('Error adding delivery service: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the delivery service.');
        });
}

// Event Listeners for Pagination
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchDelivery(currentPage);
    }
});

document.getElementById('nextPage').addEventListener('click', () => {
    currentPage++;
    fetchDelivery(currentPage);
});

// Initial Fetch
fetchDelivery(currentPage);


