//IT SHOULD BE CHANGED
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