function sortCustomers(column) {
    const table = document.getElementById('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    // Extract elements at indices that are multiples of 4
    const elementsToSort = rows.filter((_, index) => index % 4 === 0);
    console.log('Elements to sort:', elementsToSort);

    // Sort the extracted elements
    const sortedElements = elementsToSort.sort((a, b) => {
        const aElement = a.querySelector(`td:nth-child(${getColumnIndex(column)})`);
        const bElement = b.querySelector(`td:nth-child(${getColumnIndex(column)})`);

        const aText = aElement ? aElement.textContent.trim() : '';
        const bText = bElement ? bElement.textContent.trim() : '';

        if (aText < bText) return -1;
        if (aText > bText) return 1;
        return 0;
    });
    console.log('Sorted elements:', sortedElements);

    // Create a copy of the sorted elements and place them back into their original positions
    sortedElements.forEach((sortedElement, sortedIndex) => {
        const originalIndex = sortedIndex * 4;
        const newRow = sortedElement.cloneNode(true);
        tbody.replaceChild(newRow, rows[originalIndex]);
    });
}

function getColumnIndex(column) {
    switch (column) {
        case 'person_id': return 1;
        case 'first_name': return 2;
        case 'last_name': return 3;
        case 'email': return 4;
        default: return 1;
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
            success: function(response) {
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
            error: function(xhr, status, error) {
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
                success: function(response) {
                    if (response.success) {
                        $('#address-row-' + address_id).remove();
                    } else {
                        alert('Error deleting address: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    alert('Error deleting address: ' + xhr.responseText);
                }
            });
        }
    }

    function searchCustomers() {
    console.log('Searching customers');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_customer',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.customers.forEach(function(customer) {
                    var addressesHtml = '';
                    console.log(customer.addresses)
                    if (Array.isArray(customer.addresses)) {
                        customer.addresses.forEach(function(address) {
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
        error: function(xhr, status, error) {
            alert('Error searching customers: ' + xhr.responseText);
        }
    });
}


       function enableEdit(person_id) {
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

    function saveEdit(person_id) {
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
            success: function(response) {
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
            error: function(xhr, status, error) {
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
                success: function(response) {
                    if (response.success) {
                        $('#row-' + person_id).remove();
                    } else {
                        alert('Error deleting customer: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    alert('Error deleting customer: ' + xhr.responseText);
                }
            });
        }
    }
