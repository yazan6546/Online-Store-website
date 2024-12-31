function enableEditSupplier(supplier_id) {
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

function saveEditSupplier(supplier_id) {
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

function deleteSupplier(supplier_id) {
    console.log('Deleting supplier ID:', supplier_id);
    if (confirm('Are you sure you want to delete this supplier?')) {
        $.ajax({
            url: '/delete_supplier/' + supplier_id,
            type: 'POST',
            success: function(response) {
                if (response.success) {
                    $('#row-' + supplier_id).remove();
                } else {
                    alert('Error deleting supplier: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Error deleting supplier: ' + xhr.responseText);
            }
        });
    }
}

function searchSuppliers() {
    console.log('Searching suppliers');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_supplier',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.suppliers.forEach(function(supplier) {
                    var row = `
                        <tr id="row-${supplier.supplier_id}">
                            <td>${supplier.supplier_id}</td>
                            <td>
                                <span id="name-${supplier.supplier_id}-text">${supplier.name}</span>
                                <input type="text" id="name-${supplier.supplier_id}-input" value="${supplier.name}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="phone-${supplier.supplier_id}-text">${supplier.phone}</span>
                                <input type="text" id="phone-${supplier.supplier_id}-input" value="${supplier.phone}" style="display:none; width: 100px;">
                            </td>
                            <td class="action-buttons">
                                <button id="edit-btn-${supplier.supplier_id}" class="edit" onclick="enableEditSupplier(${supplier.supplier_id})">Edit</button>
                                <button id="save-btn-${supplier.supplier_id}" class="save" style="display:none;" onclick="saveEditSupplier(${supplier.supplier_id})">Save</button>
                                <button class="delete" onclick="deleteSupplier(${supplier.supplier_id})">Delete</button>
                            </td>
                        </tr>`;
                    tableBody.append(row);
                });
            } else {
                alert('Error searching suppliers: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error searching suppliers: ' + xhr.responseText);
        }
    });
}
