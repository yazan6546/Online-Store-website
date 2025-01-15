let currentSortOrder = 'asc'; // Keeps track of the current sort order


function sortCustomersOrders(column) {
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
        } else if (column === 'order_date' || column === 'delivery_date') {
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
        case 'customer_email':
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
<tr id="row-${order.order_id}">

                <td>${order.order_id}</td>
                <td>
                    <span id="email-${order.order_id}-text"> ${order.email} </span>

                </td>
                <td>
                    <span id="order_date-${order.order_id}-text">${order.order_date}</span>
                    <input type="text" id="order_date-${order.order_id}-input" value="${order.order_date}" style="display:none; width: 100px;">
                </td>

                <td>
                    <span id="delivery_date-${order.order_id}-text">${order.delivery_date}</span>
                    <input type="text" id="delivery_date-${order.order_id}-input" value="${order.delivery_date}" style="display:none; width: 100px;">

                </td>

                <td>
                    <span id="delivery_service_name-${order.order_id}-text">${order.delivery_service_name}</span>
                    <input type="text" id="delivery_service_name-${order.order_id}-input" value="${order.delivery_service_name}" style="display:none; width: 100px;">
                </td>

                <td>
                    <span id="order_status-${order.order_id}-text">${order.order_status}</span>
                    <input type="text" id="order_status-${order.order_id}-input" value="${order.order_status}" style="display:none; width: 100px;">
                </td>

                 <td class="action-column">
                    <div class="action-dropdown">
                        <button class="action-dropdown-btn">
                            <i class="fas fa-ellipsis-v"></i> <!-- Vertical three dots icon -->
                        </button>
                        <div class="action-dropdown-menu">
                            <button class="show-order" onclick="window.location.href='/view_customer_order/${order.order_id}'">View Order</button>
                            <button id="show-order-${ order.order_id  }" class="show-order" onclick="showAddress(${ order.address_id })">View Address</button>
                            <button class="delete" onclick="deleteCustomerOrder(${order.order_id})">Cancel</button>
                        </div>
                    </div>
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
        success: function (response) {
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
        error: function (xhr, status, error) {
            alert('Error updating supplier: ' + xhr.responseText);
        }
    });
}

function deleteCustomerOrder(order_id) {
    console.log('Deleting order ID:', order_id);
    if (confirm('Are you sure you want to cancel this order?')) {
        $.ajax({
            url: '/delete_customers_orders/' + order_id,
            type: 'POST',
            success: function (response) {
                if (response.success) {
                    // $('#row-' + order_id).remove();
                    $('#order_status-' + order_id + '-text').text("CANCELLED").show();
                } else {
                    alert('Error deleting Order: ' + response.error);
                }
            },
            error: function (xhr, status, error) {
                alert('Error deleting Order: ' + xhr.responseText);
            }
        });
    }
}

function searchCustomersOrders() {
    console.log('Searching orders');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_customers_orders',
        type: 'GET',
        data: {query: query},
        success: function (response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.orders.forEach(function (order) {
                    var row = generateRow(order);
                    tableBody.append(row);
                });
            } else {
                alert('Error searching orders: ' + response.error);
            }
            document.querySelectorAll('.action-dropdown-btn').forEach((btn) => {
                btn.addEventListener('click', function (event) {
                    // Close other open dropdowns
                    document.querySelectorAll('.action-dropdown').forEach((dropdown) => {
                        if (dropdown !== btn.parentElement) {
                            dropdown.classList.remove('active');
                        }
                    });

                    // Toggle the current dropdown
                    btn.parentElement.classList.toggle('active');
                    event.stopPropagation(); // Prevent event bubbling
                });
            });


// make a global event listener to close the dropdown when clicking outside
            document.addEventListener('click', () => {
                document.querySelectorAll('.action-dropdown').forEach((dropdown) => {
                    dropdown.classList.remove('active');
                });
            });


        },
        error: function (xhr, status, error) {
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
async function fetchCustomersOrders(page = 1) {
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
            document.querySelectorAll('.action-dropdown-btn').forEach((btn) => {
                btn.addEventListener('click', function (event) {
                    // Close other open dropdowns
                    document.querySelectorAll('.action-dropdown').forEach((dropdown) => {
                        if (dropdown !== btn.parentElement) {
                            dropdown.classList.remove('active');
                        }
                    });

                    // Toggle the current dropdown
                    btn.parentElement.classList.toggle('active');
                    event.stopPropagation(); // Prevent event bubbling
                });
            });


// make a global event listener to close the dropdown when clicking outside
            document.addEventListener('click', () => {
                document.querySelectorAll('.action-dropdown').forEach((dropdown) => {
                    dropdown.classList.remove('active');
                });
            });


            // Update pagination controls
            document.getElementById('currentPage').innerText = `Page ${data.page}`;
            document.getElementById('prevPage').disabled = data.page === 1;
            document.getElementById('nextPage').disabled = data.page * limit >= data.total_count;
        } else {
            console.error('Error fetching manager order:', data.error);
        }
    } catch (error) {
        console.error('Error fetching manager orders:', error);
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
        body: JSON.stringify({name, phone}),
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
fetchCustomersOrders(currentPage);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Get references to the modal and close button
// const addressModal = document.getElementById('address-modal');
//
// const closeModalBtn = addressModal.querySelector('.close-btn');
//
//
//
//
// async function showAddresses(personId) {
//     // Fetch addresses dynamically (you can replace this with an AJAX call if needed)
//     const customerAddresses = await mockGetAddresses(personId); // Replace with backend call
//     console.log(customerAddresses)
//     currentCustomerID = personId;
//     const addressTableBody = document.getElementById('address-table-body');
//     addressTableBody.innerHTML = ''; // Clear existing rows
//
//     customerAddresses.forEach((address) => {
//         const row = `
//             <tr id="address-row-${address.address_id}">
//                 <td>
//                     <span id="street_address-${address.address_id}-text">${address.street}</span>
//                     <input type="text" id="street_address-${address.address_id}-input" value="${address.street}" style="display:none; width: 300px;">
//                 </td>
//                 <td>
//                     <span id="city-${address.address_id}-text">${address.city}</span>
//                     <input type="text" id="city-${address.address_id}-input" value="${address.city}" style="display:none; width: 100px;">
//                 </td>
//                 <td>
//                     <span id="zip_code-${address.address_id}-text">${address.zip_code}</span>
//                     <input type="text" id="zip_code-${address.address_id}-input" value="${address.zip_code}" style="display:none; width: 100px;">
//                 </td>
//                 <td class="action-buttons">
//                     <button id="edit-address-btn-${address.address_id}" class="edit" onclick="enableEditAddress(${address.address_id})">Edit</button>
//                     <button id="save-address-btn-${address.address_id}" class="save" style="display:none;" onclick="saveEditAddress(${address.address_id})">Save</button>
//                     <button class="delete" onclick="deleteAddress(${address.address_id})">Delete</button>
//                 </td>
//             </tr>
//         `;
//         addressTableBody.innerHTML += row;
//     });
//
//     // Show the modal
//     addressModal.style.display = 'flex';
// }
//
// document.querySelectorAll('.action-dropdown-btn').forEach((btn) => {
//     btn.addEventListener('click', function (event) {
//         // Close other open dropdowns
//         document.querySelectorAll('.action-dropdown').forEach((dropdown) => {
//             if (dropdown !== btn.parentElement) {
//                 dropdown.classList.remove('active');
//             }
//         });
//
//         // Toggle the current dropdown
//         btn.parentElement.classList.toggle('active');
//         event.stopPropagation(); // Prevent event bubbling
//     });
// });
//
//
// // make a global event listener to close the dropdown when clicking outside
// document.addEventListener('click', () => {
//     document.querySelectorAll('.action-dropdown').forEach((dropdown) => {
//         dropdown.classList.remove('active');
//     });
// });
//
//
//
// // Close the modal
// closeModalBtn.addEventListener('click', () => {
//     addressModal.style.display = 'none';
// });
//
// // Close the modal when clicking outside of it
// window.addEventListener('click', (e) => {
//     if (e.target === addressModal) {
//         addressModal.style.display = 'none';
//     }
// });
//
// // Function to fetch address data from the server
// async function mockGetAddresses(personId) {
//     try {
//         const response = await fetch(`/api/get_addresses/${personId}`);
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error('Error fetching addresses:', error);
//         return [];
//     }
// }


