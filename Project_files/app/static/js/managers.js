    function enableEdit(person_id) {
        console.log('Enabling edit for manager ID:', person_id);
        var row = document.getElementById('row-' + person_id);
        row.classList.add('edit-mode');
        document.getElementById('first_name-' + person_id + '-text').style.display = 'none';
        document.getElementById('first_name-' + person_id + '-input').style.display = 'inline';
        document.getElementById('last_name-' + person_id + '-text').style.display = 'none';
        document.getElementById('last_name-' + person_id + '-input').style.display = 'inline';
        document.getElementById('email-' + person_id + '-text').style.display = 'none';
        document.getElementById('email-' + person_id + '-input').style.display = 'inline';
        document.getElementById('since-' + person_id + '-text').style.display = 'none';
        document.getElementById('since-' + person_id + '-input').style.display = 'inline';
        document.getElementById('role-' + person_id + '-text').style.display = 'none';
        document.getElementById('role-' + person_id + '-input').style.display = 'inline';
        document.getElementById('save-btn-' + person_id).style.display = 'inline';
        document.getElementById('edit-btn-' + person_id).style.display = 'none';
    }

    function saveEdit(person_id) {
        console.log('Saving edit for manager ID:', person_id);
        var first_name = $('#first_name-' + person_id + '-input').val();
        var last_name = $('#last_name-' + person_id + '-input').val();
        var email = $('#email-' + person_id + '-input').val();
        var since = $('#since-' + person_id + '-input').val();
        var role = $('#role-' + person_id + '-input').val();
        $.ajax({
            url: '/update_manager/' + person_id,
            type: 'POST',
            data: {
                first_name: first_name,
                last_name: last_name,
                email: email,
                since: since,
                role: role
            },
            success: function(response) {
                if (response.success) {
                    $('#first_name-' + person_id + '-text').text(first_name).show();
                    $('#first_name-' + person_id + '-input').hide();
                    $('#last_name-' + person_id + '-text').text(last_name).show();
                    $('#last_name-' + person_id + '-input').hide();
                    $('#email-' + person_id + '-text').text(email).show();
                    $('#email-' + person_id + '-input').hide();
                    $('#since-' + person_id + '-text').text(since).show();
                    $('#since-' + person_id + '-input').hide();
                    $('#role-' + person_id + '-text').text(role).show();
                    $('#role-' + person_id + '-input').hide();
                    $('#edit-btn-' + person_id).show();
                    $('#save-btn-' + person_id).hide();
                } else {
                    alert('Error updating manager: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Error updating manager: ' + xhr.responseText);
            }
        });
    }


    function deleteManager(person_id) {
        console.log('Deleting manager ID:', person_id);
        if (confirm('Are you sure you want to delete this manager?')) {
            $.ajax({
                url: '/delete_manager/' + person_id,
                type: 'POST',
                success: function(response) {
                    if (response.success) {
                        $('#row-' + person_id).remove();
                    } else {
                        alert('Error deleting manager: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    alert('Error deleting manager: ' + xhr.responseText);
                }
            });
        }
    }

    function searchManagers() {
    console.log('Searching managers');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_manager',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody'); // Ensure the id matches the HTML
                tableBody.empty(); // Clear the existing table rows
                response.managers.forEach(function(manager) {
                    var row = `
                        <tr id="row-${manager.person_id}">
                            <td>${manager.person_id}</td>
                            <td>
                                <span id="first_name-${manager.person_id}-text">${manager.first_name}</span>
                                <input type="text" id="first_name-${manager.person_id}-input" value="${manager.first_name}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="last_name-${manager.person_id}-text">${manager.last_name}</span>
                                <input type="text" id="last_name-${manager.person_id}-input" value="${manager.last_name}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="email-${manager.person_id}-text">${manager.email}</span>
                                <input type="text" id="email-${manager.person_id}-input" value="${manager.email}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="since-${manager.person_id}-text">${manager.since}</span>
                                <input type="text" id="since-${manager.person_id}-input" value="${manager.since}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="role-${manager.person_id}-text">${manager.role}</span>
                                <select id="role-${manager.person_id}-input" style="display:none; width: 150px;">
                                    <option value="Financial Manager" ${manager.role === 'Financial Manager' ? 'selected' : ''}>Financial Manager</option>
                                    <option value="Assistant Manager" ${manager.role === 'Assistant Manager' ? 'selected' : ''}>Assistant Manager</option>
                                    <option value="Regional Manager" ${manager.role === 'Regional Manager' ? 'selected' : ''}>Regional Manager</option>
                                </select>
                            </td>
                            <td class="action-buttons">
                                <button id="edit-btn-${manager.person_id}" class="edit" onclick="enableEdit(${manager.person_id})">Edit</button>
                                <button id="save-btn-${manager.person_id}" class="save" style="display:none;" onclick="saveEdit(${manager.person_id})">Save</button>
                                <button class="delete" onclick="deleteManager(${manager.person_id})">Delete</button>
                            </td>
                        </tr>`;
                    tableBody.append(row);
                });
            } else {
                alert('Error searching managers: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error searching managers: ' + xhr.responseText);
        }
    });
}

/////////////////////////////////
function openModalManager() {
    const modal = document.getElementById("add-manager-modal");
    modal.classList.add("show");
}

function closeModalManager() {
    const modal = document.getElementById("add-manager-modal");
    modal.classList.remove("show");
}

// Add manager
function addManager() {
    const first_name = document.getElementById('manager-firstName').value;
    const last_name = document.getElementById('manager-lastName').value;
    const email = document.getElementById('manager-email').value;
    const role = document.getElementById('manager-role').value;

    // Validate inputs
    if (!first_name || !last_name || !email || !role) {
        alert('Please fill in all fields.');
        return;
    }

    // Send data to the server via AJAX
    fetch('/add_manager', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ first_name, last_name, email, role }),
    })
        .then(response => response.json())
        .then(data => {

            if (data.success) {
                alert('Manager added successfully!');
                closeModalManager();
                // Optionally, update the table dynamically
                const tableBody = document.querySelector('#table tbody');
                const newRow = `
                    <tr id="row-${data.manager.person_id}">
                        <td>${data.manager.person_id}</td>
                        <td>
                            <span id="first_name-${data.manager.person_id}-text">${data.manager.first_name}</span>
                            <input type="text" id="first_name-${data.manager.person_id}-input" value="${data.manager.first_name}" style="display:none; width: 100px;">
                        </td>

                         <td>
                            <span id="last_name-${data.manager.person_id}-text">${data.manager.last_name}</span>
                            <input type="text" id="last_name-${data.manager.person_id}-input" value="${data.manager.last_name}" style="display:none; width: 100px;">
                        </td>

                        <td>
                            <span id="email-${data.manager.person_id}-text">${data.manager.email}</span>
                            <input type="text" id="email-${data.manager.person_id}-input" value="${data.manager.email}" style="display:none; width: 100px;">
                        </td>

                         <td>
                            <span id="since-${data.manager.person_id}-text">${data.manager.since}</span>
                            <input type="text" id="since-${data.manager.person_id}-input" value="${data.manager.since}" style="display:none; width: 100px;">
                        </td>
                        
                        <td>
                            <span id="role-${data.manager.person_id}-text">${data.manager.role}</span>
                            <input type="text" id="role-${data.manager.person_id}-input" value="${data.manager.role}" style="display:none; width: 100px;">
                        </td>


                        <td class="action-buttons">
                            <button id="edit-btn-${data.manager.person_id}" class="edit" onclick="enableEdit(${data.manager.person_id})">Edit</button>
                            <button id="save-btn-${data.manager.person_id}" class="save" style="display:none;" onclick="saveEdit(${data.manager.person_id})">Save</button>
                            <button class="delete" onclick="deleteManager(${data.manager.person_id})">Delete</button>
                        </td>
                    </tr>`;
                tableBody.insertAdjacentHTML('beforeend', newRow);
            } else {
                alert('Error adding manager: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the manager.');
        });
}


