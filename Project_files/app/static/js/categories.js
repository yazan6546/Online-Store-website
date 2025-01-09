let currentSortOrder = 'asc'; // Keeps track of the current sort order

function sortCategories(column) {
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

        // Handle numeric sorting for `category_id`
        if (column === 'category_id') {
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
        case 'category_id':
            return 1; // 1st column
        case 'category_name':
            return 2; // 2nd column (or "category_name")
        case 'category_description':
            return 3; // 3rd column (or "category_description")
        default:
            return 1;  // Fallback
    }
}


function enableEditCategory(category_id) {
    console.log('Enabling edit for category ID:', category_id);
    var row = document.getElementById('row-' + category_id);
    row.classList.add('edit-mode');
    document.getElementById('name-' + category_id + '-text').style.display = 'none';
    document.getElementById('name-' + category_id + '-input').style.display = 'inline';
    document.getElementById('description-' + category_id + '-text').style.display = 'none';
    document.getElementById('description-' + category_id + '-input').style.display = 'inline';
    document.getElementById('save-btn-' + category_id).style.display = 'inline';
    document.getElementById('edit-btn-' + category_id).style.display = 'none';
}

function saveEditCategory(category_id) {
    console.log('Saving edit for category ID:', category_id);
    var name = $('#name-' + category_id + '-input').val();
    var description = $('#description-' + category_id + '-input').val();
    $.ajax({
        url: '/update_category/' + category_id,
        type: 'POST',
        data: {
            name: name,
            description: description
        },
        success: function(response) {
            if (response.success) {
                $('#name-' + category_id + '-text').text(name).show();
                $('#name-' + category_id + '-input').hide();
                $('#description-' + category_id + '-text').text(description).show();
                $('#description-' + category_id + '-input').hide();
                $('#edit-btn-' + category_id).show();
                $('#save-btn-' + category_id).hide();
            } else {
                alert('Error updating category: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error updating category: ' + xhr.responseText);
        }
    });
}

function deleteCategory(category_id) {
    console.log('Deleting category ID:', category_id);
    if (confirm('Are you sure you want to delete this category?')) {
        $.ajax({
            url: '/delete_category/' + category_id,
            type: 'POST',
            success: function(response) {
                if (response.success) {
                    $('#row-' + category_id).remove();
                } else {
                    alert('Error deleting category: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Error deleting category: ' + xhr.responseText);
            }
        });
    }
}

function searchCategories() {
    console.log('Searching categorys');
    var query = $('#search-query').val();
    $.ajax({
        url: '/search_category',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody');
                tableBody.empty();
                response.categories.forEach(function(category) {
                    var row = `
                        <tr id="row-${category.category_id}">
                            <td>${category.category_id}</td>
                            <td>
                                <span id="name-${category.category_id}-text">${category.category_name}</span>
                                <input type="text" id="name-${category.category_id}-input" value="${category.category_name}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="description-${category.category_id}-text">${category.category_description}</span>
                                <input type="text" id="description-${category.category_id}-input" value="${category.category_description}" style="display:none; width: 100px;">
                            </td>
                            <td class="action-buttons">
                                <button id="edit-btn-${category.category_id}" class="edit" onclick="enableEditCategory(${category.category_id})">Edit</button>
                                <button id="save-btn-${category.category_id}" class="save" style="display:none;" onclick="saveEditCategory(${category.category_id})">Save</button>
                                <button class="delete" onclick="deleteCategory(${category.category_id})">Delete</button>
                            </td>
                        </tr>`;
                    tableBody.append(row);
                });
            } else {
                alert('Error searching categories: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error searching Category: ' + xhr.responseText);
        }
    });
}
/////////////////////////////////////////////////////////////////////////

// Open the modal
// function openModal() {
//     document.getElementById('add-category-modal').style.display = 'block';
//
// }
//
// // Close the modal
// function closeModal() {
//     document.getElementById('add-category-modal').style.display = 'none';
//     // Clear form inputs
//     document.getElementById('category-name').value = '';
//     document.getElementById('category-phone').value = '';
// }


function openModal() {
    const modal = document.getElementById("add-category-modal");
    modal.classList.add("show");
}

function closeModal() {
    const modal = document.getElementById("add-category-modal");
    modal.classList.remove("show");
}

let currentPage = 1;
const limit = 10; // Rows per page

// Fetch categorys and update the table
async function fetchCategories(page = 1) {
    try {
        const response = await fetch(`/get_categorys?page=${page}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            // Update the table
            const tableBody = document.querySelector('#table tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            data.categorys.forEach(category => {
                const newRow = `
                    <tr id="row-${category.category_id}">
                        <td>${category.category_id}</td>
                        <td>
                            <span id="name-${category.category_id}-text">${category.name}</span>
                            <input type="text" id="name-${category.category_id}-input" value="${category.name}" style="display:none; width: 100px;">
                        </td>
                        <td>
                            <span id="phone-${category.category_id}-text">${category.phone}</span>
                            <input type="text" id="phone-${category.category_id}-input" value="${category.phone}" style="display:none; width: 100px;">
                        </td>
                        <td class="action-buttons">
                            <button id="edit-btn-${category.category_id}" class="edit" onclick="enableEditcategory(${category.category_id})">Edit</button>
                            <button id="save-btn-${category.category_id}" class="save" style="display:none;" onclick="saveEditcategory(${category.category_id})">Save</button>
                            <button class="delete" onclick="deletecategory(${category.category_id})">Delete</button>
                        </td>
                    </tr>`;
                tableBody.innerHTML += newRow;
            });

            // Update pagination controls
            document.getElementById('currentPage').innerText = `Page ${data.page}`;
            document.getElementById('prevPage').disabled = data.page === 1;
            document.getElementById('nextPage').disabled = data.page * limit >= data.total_count;
        } else {
            console.error('Error fetching categorys:', data.error);
        }
    } catch (error) {
        console.error('Error fetching categorys:', error);
    }
}

// Add category and refresh the table
function addCategory() {
    const name = document.getElementById('category-name').value;
    const description = document.getElementById('category-description').value;

    // Validate inputs
    if (!name || !description) {
        alert('Please fill in all fields.');
        return;
    }

    // Send data to the server
    fetch('/add_category', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, description }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('category added successfully!');
                closeModal(); // Close the modal
                fetchCategories(currentPage); // Refresh the current page
            } else {
                alert('Error adding Category: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the Category.');
        });
}

// Event Listeners for Pagination
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchCategories(currentPage);
    }
});

document.getElementById('nextPage').addEventListener('click', () => {
    currentPage++;
    fetchCategories(currentPage);
});

// Initial Fetch
fetchCategories(currentPage);


