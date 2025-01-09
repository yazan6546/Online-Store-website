let currentSortOrder = 'asc'; // Keeps track of the current sort order

function sortCustomers(column) {
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

        // Handle numeric sorting for `person_id`
        if (column === 'person_id') {
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

// Utility function to map column names to their respective indices
function getColumnIndex(column) {
    switch (column) {
        case 'person_id':
            return 1; // 1st column
        case 'first_name':
            return 2; // 2nd column
        case 'last_name':
            return 3; // 3rd column
        case 'email':
            return 4; // 4th column
        default:
            return 1;
    }
}


function enableEditAddress(address_id) {

    console.log('Enabling edit for address ID:', address_id);
    var row = document.getElementById('address-row-' + address_id);
    console.log(row);
    row.classList.add('edit-mode');
    document.getElementById('street_address-' + address_id + '-text').style.display = 'none';
    document.getElementById('street_address-' + address_id + '-input').style.display = 'inline';
    document.getElementById('city-' + address_id + '-text').style.display = 'none';
    document.getElementById('city-' + address_id + '-input').style.display = 'inline';
    document.getElementById('zip_code-' + address_id + '-text').style.display = 'none';
    document.getElementById('zip_code-' + address_id + '-input').style.display = 'inline';
    document.getElementById('save-address-btn-' + address_id).style.display = 'inline';
    document.getElementById('edit-address-btn-' + address_id).style.display = 'none';
}

function saveEditAddress(address_id) {
    console.log('Saving edit for address ID:', address_id);
    var street_address = $('#street_address-' + address_id + '-input').val();
    var city = $('#city-' + address_id + '-input').val();
    var zip_code = $('#zip_code-' + address_id + '-input').val();
    $.ajax({
        url: '/edit_address/' + address_id,
        type: 'POST',
        data: {
            street: street_address,
            city: city,
            zip_code: zip_code
        },
        success: function (response) {
            if (response.success) {
                $('#street_address-' + address_id + '-text').text(street_address).show();
                $('#street_address-' + address_id + '-input').hide();
                $('#city-' + address_id + '-text').text(city).show();
                $('#city-' + address_id + '-input').hide();
                $('#zip_code-' + address_id + '-text').text(zip_code).show();
                $('#zip_code-' + address_id + '-input').hide();
                $('#edit-address-btn-' + address_id).show();
                $('#save-address-btn-' + address_id).hide();
            } else {
                alert('Error updating address: ' + response.error);
            }
        },
        error: function (xhr, status, error) {
            alert('Error updating address: ' + xhr.responseText);
        }
    });
}

function deleteAddress(address_id) {
    console.log('Deleting address ID:', address_id);
    if (confirm('Are you sure you want to delete this address?')) {
        $.ajax({
            url: '/delete_address/' + address_id,
            type: 'POST',
            success: function (response) {
                if (response.success) {
                    $('#address-row-' + address_id).remove();
                } else {
                    alert('Error deleting address: ' + response.error);
                }
            },
            error: function (xhr, status, error) {
                alert('Error deleting address: ' + xhr.responseText);
            }
        });
    }
}

//
// function addAddress(person_id) {
//     console.log('Adding address for customer ID:', person_id);
//     $.ajax({
//         url: '/add_address/' + person_id,
//         type: 'POST',
//         success: function(response) {
//             if (response.success) {
//                 var addressesTable = document.querySelector(`#row-${person_id} .address-subtable tbody`);
//                 var address = response.address;
//                 var row = `
//                     <tr id="address-row-${address.address_id}">
//                         <td>
//                             <span id="street_address-${address.address_id}-text">${address.street}</span>
//                             <input type="text" id="street_address-${address.address_id}-input" value="${address.street}" style="display:none; width: 100px;">
//                         </td>
//                         <td>
//                             <span id="city-${address.address_id}-text">${address.city}</span>
//                             <input type="text" id="city-${address.address_id}-input" value="${address.city}" style="display:none; width: 100px;">
//                         </td>
//                         <td>
//                             <span id="zip_code-${address.address_id}-text">${address.zip_code}</span>
//                             <input type="text" id="zip_code-${address.address_id}-input" value="${address.zip_code}" style="display:none; width: 100px;">
//                         </td>
//                         <td class="action-buttons">
//                             <button id="edit-address-btn-${address.address_id}" class="edit" onclick="enableEditAddress(${address.address_id})">Edit</button>
//                             <button id="save-address-btn-${address.address_id}" class="save" style="display:none;" onclick="saveEditAddress(${address.address_id})">Save</button>
//                             <button class="delete" onclick="deleteAddress(${address.address_id})">Delete</button>
//                         </td>
//                     </tr>`;
//                 addressesTable.insertAdjacentHTML('beforeend', row);
//             } else {
//                 alert('Error adding address: ' + response.error);
//             }
//         },
//         error: function(xhr, status, error) {
//             alert('Error adding address: ' + xhr.responseText);
//         }
//     });
// }


function addAddress() {
    const customerId = document.getElementById('customer-id').value;
    const street = document.getElementById('address-street').value;
    const city = document.getElementById('address-city').value;
    const zip = document.getElementById('address-zip').value;

    // Validate inputs
    if (!street || !city || !zip) {
        alert('Please fill in all fields.');
        return;
    }

    // AJAX call to server
    $.ajax({
        url: `/add_address/${customerId}`,
        type: 'POST',
        data: JSON.stringify({street, city, zip}),
        contentType: 'application/json',
        success: function (response) {
            if (response.success) {
                alert('Address added successfully!');
                const addressesTable = document.querySelector(`#row-${customerId} .address-subtable tbody`);
                const newRow = `
                    <tr id="address-row-${response.address.address_id}">
                        <td>${response.address.street}</td>
                        <td>${response.address.city}</td>
                        <td>${response.address.zip}</td>
                        <td class="action-buttons">
                            <button class="edit" onclick="enableEditAddress(${response.address.address_id})">Edit</button>
                            <button class="delete" onclick="deleteAddress(${response.address.address_id})">Delete</button>
                        </td>
                    </tr>`;
                addressesTable.insertAdjacentHTML('beforeend', newRow);
                closeAddAddressModal();
            } else {
                alert('Error adding address: ' + response.error);
            }
        },
        error: function (xhr) {
            alert('Error adding address: ' + xhr.responseText);
        },
    });
}


function searchCustomers() {
    console.log('Searching customers');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_customer',
        type: 'GET',
        data: {query: query},
        success: function (response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.customers.forEach(function (customer) {
                    var addressesHtml = '';
                    console.log(customer.addresses)
                    if (Array.isArray(customer.addresses)) {
                        customer.addresses.forEach(function (address) {
                            console.log("street = " + address.street)
                            addressesHtml += `
                            <tr id="address-row-${address.address_id}">
                                <td>
                                    <span id="street_address-${address.address_id}-text">${address.street}</span>
                                    <input type="text" id="street_address-${address.address_id}-input" value="${address.street}" style="display:none; width: 100px;">
                                </td>
                                <td>
                                    <span id="city-${address.id}-text">${address.city}</span>
                                    <input type="text" id="city-${address.address_id}-input" value="${address.city}" style="display:none; width: 100px;">
                                </td>
                                <td>
                                    <span id="zip_code-${address.id}-text">${address.zip_code}</span>
                                    <input type="text" id="zip_code-${address.address_id}-input" value="${address.zip_code}" style="display:none; width: 100px;">
                                </td>
                                <td class="action-buttons">
                                    <button id="edit-address-btn-${address.address_id}" class="edit" onclick="enableEditAddress(${address.address_id})">Edit</button>
                                    <button id="save-address-btn-${address.address_id}" class="save" style="display:none;" onclick="saveEditAddress(${address.address_id})">Save</button>
                                    <button class="delete" onclick="deleteAddress(${address.address_id})">Delete</button>
                                </td>
                            </tr>`;
                        });
                    }
                    var row = `
                    <tr id="row-${customer.person_id}">
                        <td>${customer.person_id}</td>
                        <td>
                            <span id="first_name-${customer.person_id}-text">${customer.first_name}</span>
                            <input type="text" id="first_name-${customer.person_id}-input" value="${customer.first_name}" style="display:none; width: 100px;">
                        </td>
                        <td>
                            <span id="last_name-${customer.person_id}-text">${customer.last_name}</span>
                            <input type="text" id="last_name-${customer.person_id}-input" value="${customer.last_name}" style="display:none; width: 100px;">
                        </td>
                        <td>
                            <span id="email-${customer.person_id}-text">${customer.email}</span>
                            <input type="text" id="email-${customer.person_id}-input" value="${customer.email}" style="display:none; width: 100px;">
                        </td>
                        <td>
                            <table class="address-subtable">
                                <thead>
                                    <tr>
                                        <th>Street Address</th>
                                        <th>City</th>
                                        <th>Zip Code</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${addressesHtml}
                                </tbody>
                            </table>
                        </td>
                        <td class="action-buttons">
                            <button id="edit-btn-${customer.person_id}" class="edit" onclick="enableEdit(${customer.person_id})">Edit</button>
                            <button id="save-btn-${customer.person_id}" class="save" style="display:none;" onclick="saveEdit(${customer.person_id})">Save</button>
                            <button class="delete" onclick="deleteCustomer(${customer.person_id})">Delete</button>
                        </td>
                    </tr>`;
                    tableBody.append(row);
                });
            } else {
                alert('Error searching customers: ' + response.error);
            }
        },
        error: function (xhr, status, error) {
            alert('Error searching customers: ' + xhr.responseText);
        }
    });
}


function enableEditCustomer(person_id) {
    console.log('Enabling edit for customer ID:', person_id);
    var row = document.getElementById('row-' + person_id);
    row.classList.add('edit-mode');
    document.getElementById('first_name-' + person_id + '-text').style.display = 'none';
    document.getElementById('first_name-' + person_id + '-input').style.display = 'inline';
    document.getElementById('last_name-' + person_id + '-text').style.display = 'none';
    document.getElementById('last_name-' + person_id + '-input').style.display = 'inline';
    document.getElementById('email-' + person_id + '-text').style.display = 'none';
    document.getElementById('email-' + person_id + '-input').style.display = 'inline';
    document.getElementById('save-btn-' + person_id).style.display = 'inline';
    document.getElementById('edit-btn-' + person_id).style.display = 'none';
}

function saveEditCustomer(person_id) {
    console.log('Saving edit for customer ID:', person_id);
    var first_name = $('#first_name-' + person_id + '-input').val();
    var last_name = $('#last_name-' + person_id + '-input').val();
    var email = $('#email-' + person_id + '-input').val();
    $.ajax({
        url: '/update_customer/' + person_id,
        type: 'POST',
        data: {
            first_name: first_name,
            last_name: last_name,
            email: email
        },
        success: function (response) {
            if (response.success) {
                $('#first_name-' + person_id + '-text').text(first_name).show();
                $('#first_name-' + person_id + '-input').hide();
                $('#last_name-' + person_id + '-text').text(last_name).show();
                $('#last_name-' + person_id + '-input').hide();
                $('#email-' + person_id + '-text').text(email).show();
                $('#email-' + person_id + '-input').hide();
                $('#edit-btn-' + person_id).show();
                $('#save-btn-' + person_id).hide();
            } else {
                alert('Error updating customer: ' + response.error);
            }
        },
        error: function (xhr, status, error) {
            alert('Error updating customer: ' + xhr.responseText);
        }
    });
}

function deleteCustomer(person_id) {
    console.log('Deleting customer ID:', person_id);
    if (confirm('Are you sure you want to delete this customer?')) {
        $.ajax({
            url: '/delete_customer/' + person_id,
            type: 'POST',
            success: function (response) {
                if (response.success) {
                    $('#row-' + person_id).remove();
                } else {
                    alert('Error deleting customer: ' + response.error);
                }
            },
            error: function (xhr, status, error) {
                alert('Error deleting customer: ' + xhr.responseText);
            }
        });
    }
}


///////////////////////////////////////////////////////////////////////////////////

document.getElementById('add-address-btn').addEventListener('click', function () {
    // Show the row for adding a new address
    document.getElementById('new-address-row').style.display = 'table-row';

    // Make sure the "Save" button is visible
    document.querySelector('#new-address-row .save').style.display = 'inline-block';
    document.querySelector('#new-address-row .cancel').style.display = 'inline-block';
});


// Open Address Modal
function showAddresses(customerId) {
    const modal = document.getElementById('address-modal');
    const addressTableBody = document.getElementById('address-table-body');

    // Clear existing rows
    addressTableBody.innerHTML = '';

    // Fetch addresses dynamically (assuming a fetchAddresses function is defined)
    fetchAddresses(customerId).then(addresses => {
        addresses.forEach(address => {
            const row = `
        <tr id="address-row-${address.address_id}">
          <td>${address.street}</td>
          <td>${address.city}</td>
          <td>${address.zip_code}</td>
          <td>
            <button class="edit" onclick="enableEditAddress(${address.address_id})">Edit</button>
            <button class="delete" onclick="deleteAddress(${address.address_id})">Delete</button>
          </td>
        </tr>
      `;
            addressTableBody.insertAdjacentHTML('beforeend', row);
        });
    });

    modal.style.display = 'block';
}

// Close Modal
document.querySelector('.close-btn').addEventListener('click', () => {
    document.getElementById('address-modal').style.display = 'none';
});

function cancelNewAddress() {
    document.getElementById('new-street').value = '';
    document.getElementById('new-city').value = '';
    document.getElementById('new-zip').value = '';
    document.getElementById('new-address-row').style.display = 'none';
}

function saveNewAddress() {
    const street = document.getElementById('new-street').value;
    const city = document.getElementById('new-city').value;
    const zip = document.getElementById('new-zip').value;

    // Validate inputs
    if (!street || !city || !zip) {
        alert('Please fill in all fields.');
        return;
    }

    const customerId = document.getElementById('customer-id').value;

    // Send the new address to the backend
    $.ajax({
        url: `/add_address/${customerId}`,
        type: 'POST',
        data: JSON.stringify({street, city, zip}),
        contentType: 'application/json',
        success: function (response) {
            if (response.success) {
                alert('Address added successfully!');
                // Update the address table with the new row
                const addressesTable = document.querySelector(`#row-${customerId} .address-subtable tbody`);
                const newRow = `
                    <tr id="address-row-${response.address.address_id}">
                        <td>${response.address.street}</td>
                        <td>${response.address.city}</td>
                        <td>${response.address.zip}</td>
                        <td class="action-buttons">
                            <button class="edit" onclick="enableEditAddress(${response.address.address_id})">Edit</button>
                            <button class="delete" onclick="deleteAddress(${response.address.address_id})">Delete</button>
                        </td>
                    </tr>`;
                addressesTable.insertAdjacentHTML('beforeend', newRow);
                // Hide the input row after saving
                document.getElementById('new-address-row').style.display = 'none';
            } else {
                alert('Error adding address: ' + response.error);
            }
        },
        error: function (xhr) {
            alert('Error adding address: ' + xhr.responseText);
        }
    });
}

////////////////////////////////////////////////////////////////////////////////////
function openModalCustomer() {
    const modal = document.getElementById("add-customer-modal");
    modal.classList.add("show");
}

function closeModalCustomer() {
    const modal = document.getElementById("add-customer-modal");
    modal.classList.remove("show");
}

// Add customer
function addCustomer() {
    // Retrieve input values
    const first_name = document.getElementById('customer-firstName').value;
    const last_name = document.getElementById('customer-lastName').value;
    const email = document.getElementById('customer-email').value;

    // Validate inputs
    if (!first_name || !last_name || !email) {
        alert('Please fill in all fields.');
        return;
    }

    // Send data to the server via AJAX
    fetch('/add_customer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({first_name, last_name, email}),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Customer added successfully!');
                closeModalCustomer(); // Make sure to define this function to close the modal

                // Optionally, update the table dynamically
                const tableBody = document.querySelector('#table tbody');
                const newRow = `
                    <tr id="row-${data.customer.person_id}">
                        <td>${data.customer.person_id}</td>
                        <td>
                            <span id="first_name-${data.customer.person_id}-text">${data.customer.first_name}</span>
                            <input type="text" id="first_name-${data.customer.person_id}-input" value="${data.customer.first_name}" style="display:none; width: 100px;">
                        </td>

                        <td>
                            <span id="last_name-${data.customer.person_id}-text">${data.customer.last_name}</span>
                            <input type="text" id="last_name-${data.customer.person_id}-input" value="${data.customer.last_name}" style="display:none; width: 100px;">
                        </td>

                        <td>
                            <span id="email-${data.customer.person_id}-text">${data.customer.email}</span>
                            <input type="text" id="email-${data.customer.person_id}-input" value="${data.customer.email}" style="display:none; width: 100px;">
                        </td>

                        <td class="action-column">
                            <div class="action-dropdown">
                                <button class="action-dropdown-btn">
                                    <i class="fas fa-ellipsis-v"></i> <!-- Vertical three dots icon -->
                                </button>
                                <div class="action-dropdown-menu">
                                    <button id="edit-btn-${data.customer.person_id}" class="edit" onclick="enableEdit(${data.customer.person_id})">Edit</button>
                                    <button id="save-btn-${data.customer.person_id}" class="save" style="display:none;" onclick="saveEdit(${data.customer.person_id})">Save</button>
                                    <button class="delete" onclick="deleteCustomer(${data.customer.person_id})">Delete</button>
                                    <button class="show-addresses" onclick="showAddresses(${data.customer.person_id})">Show Addresses</button>
                                </div>
                            </div>
                        </td>
                    </tr>`;
                tableBody.insertAdjacentHTML('beforeend', newRow);
            } else {
                alert('Error adding customer: ' + data.error);
            }
        })
        .catch(error => {
            alert('An error occurred: ' + error.message);
        });
}
