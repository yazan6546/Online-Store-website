// Keep track of sort order
let currentSortOrder = 'asc';
let products = []; // Global list of products


// $(document).ready(function () {
//     // Trigger searchProducts() with an empty query on page load
//     searchProducts('');
// });



// ------------------- SORTING ------------------- //
function sortProducts(column) {
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
        if (['product_id', 'price', 'stock_quantity', 'category_id', 'supplier_id']
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
        case 'category_id':
            return 3;
        case 'supplier_id':
            return 4;
        case 'brand':
            return 5;
        case 'price':
            return 6;
        case 'stock_quantity':
            return 7;
        // description = 8, actions = 9
        default:
            return 1;
    }
}

// ------------------- ENABLE EDIT ------------------- //
function enableEditProduct(product_id) {
    console.log('Enabling edit for product ID:', product_id);

    // Hide the 3-dots dropdown
    document.getElementById(`three-dots-${product_id}`).style.display = 'none';
    // Show the Save button
    document.getElementById(`save-btn-${product_id}`).style.display = 'inline-block';

    // Name
    document.getElementById(`name-${product_id}-text`).style.display = 'none';
    document.getElementById(`name-${product_id}-input`).style.display = 'inline';

    // Category
    document.getElementById(`category-${product_id}-text`).style.display = 'none';
    document.getElementById(`category-${product_id}-input`).style.display = 'inline-block';

    // Supplier
    document.getElementById(`supplier-${product_id}-text`).style.display = 'none';
    document.getElementById(`supplier-${product_id}-input`).style.display = 'inline-block';

    // Brand
    document.getElementById(`brand-${product_id}-text`).style.display = 'none';
    document.getElementById(`brand-${product_id}-input`).style.display = 'inline';

    // Price
    document.getElementById(`price-${product_id}-text`).style.display = 'none';
    document.getElementById(`price-${product_id}-input`).style.display = 'inline';

    // Stock
    document.getElementById(`stock-${product_id}-text`).style.display = 'none';
    document.getElementById(`stock-${product_id}-input`).style.display = 'inline';

    // Also enable the description pencil if it’s not already
    // (the pencil is always there, but maybe we want to ensure it’s visible or something).
}

// ------------------- ENABLE DESCRIPTION EDIT ONLY ------------------- //
// function enableDescriptionEdit(product_id) {
//     console.log('Enabling description edit for product ID:', product_id);
//     // Hide the static text
//     document.getElementById(`description-${product_id}-text`).style.display = 'none';
//     // Hide the pencil
//     document.getElementById(`desc-edit-icon-${product_id}`).style.display = 'none';
//     // Show the textarea
//     document.getElementById(`description-edit-container-${product_id}`).style.display = 'block';
//
//     // Pre-fill the textarea with existing text
//     const descValue = document.getElementById(`description-${product_id}-text`).innerText;
//     document.getElementById(`description-${product_id}-input`).value = descValue;
//
//     // Also hide the 3-dots & show Save button if not in "edit" mode
//     document.getElementById(`three-dots-${product_id}`).style.display = 'none';
//     document.getElementById(`save-btn-${product_id}`).style.display = 'inline';
// }

// ------------------- SAVE EDIT ------------------- //
function saveEditProduct(product_id) {
    console.log('Saving edit for product ID:', product_id);

    // Gather new values
    //const product_name = document.getElementById(`name-${product_id}-input`).value;
    const product_name = document.getElementById(`name-${product_id}-input`).value;
    const category_id = document.getElementById(`category-${product_id}-input`).value;
    const supplier_id = document.getElementById(`supplier-${product_id}-input`).value;
    const brand = document.getElementById(`brand-${product_id}-input`).value;
    const price = document.getElementById(`price-${product_id}-input`).value;
    const stock_quantity = document.getElementById(`stock-${product_id}-input`).value;
    //const descContainer = document.getElementById(`description-edit-container-${product_id}`);

    // For description
    // let newDescription = null;
    if (descContainer.style.display === 'block') {
        newDescription = document.getElementById(`description-${product_id}-input`).value;
    }

    // Example: Make an AJAX call to update on the server
    // (Using fetch as an example)
    fetch(`/update_product/${product_id}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            product_name,
            category_id,
            supplier_id,
            brand,
            price,
            stock_quantity,
        }),
    })
        .then(res => res.json())
        .then(response => {
            if (response.success) {
                // Update text spans
                document.getElementById(`name-${product_id}-text`).innerText = product_name;
                document.getElementById(`category-${product_id}-text`).innerText = category_id;
                document.getElementById(`supplier-${product_id}-text`).innerText = supplier_id;
                document.getElementById(`brand-${product_id}-text`).innerText = brand;
                document.getElementById(`price-${product_id}-text`).innerText = price;
                document.getElementById(`stock-${product_id}-text`).innerText = stock_quantity;



                // Hide input fields, show text
                document.getElementById(`name-${product_id}-input`).style.display = 'none';
                document.getElementById(`category-${product_id}-input`).style.display = 'none';
                document.getElementById(`supplier-${product_id}-input`).style.display = 'none';
                document.getElementById(`brand-${product_id}-input`).style.display = 'none';
                document.getElementById(`price-${product_id}-input`).style.display = 'none';
                document.getElementById(`stock-${product_id}-input`).style.display = 'none';

                document.getElementById(`name-${product_id}-text`).style.display = 'inline';
                document.getElementById(`category-${product_id}-text`).style.display = 'inline';
                document.getElementById(`supplier-${product_id}-text`).style.display = 'inline';
                document.getElementById(`brand-${product_id}-text`).style.display = 'inline';
                document.getElementById(`price-${product_id}-text`).style.display = 'inline';
                document.getElementById(`stock-${product_id}-text`).style.display = 'inline';



                // Show the 3-dots again, hide the Save button
                document.getElementById(`three-dots-${product_id}`).style.display = 'inline-block';
                document.getElementById(`save-btn-${product_id}`).style.display = 'none';
            } else {
                alert('Error updating product: ' + response.error);
            }
        })
        .catch(error => {
            alert('Error updating product: ' + error);
        });
}

// ------------------- TOGGLE 3-DOTS DROPDOWN ------------------- //
function toggleDropdown(product_id) {
    const dropdown = document.getElementById(`three-dots-${product_id}`);
    dropdown.classList.toggle('show');
    // You may want to close it when user clicks outside, etc.
}


// ------------------- DELETE ------------------- //
function deleteProduct(product_id) {
    console.log('Deleting product ID:', product_id);

    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    $.ajax({
        url: `/delete_product/${product_id}`,
        type: 'POST',
        success: function (response) {
            if (response.success) {
                document.getElementById(`row-${product_id}`).remove();
            } else {
                alert('Error deleting product: ' + response.error);
            }
        },
        error: function (xhr, status, error) {
            alert('Error deleting product: ' + xhr.responseText);
        }
    });
}

//------------------- SEARCH ------------------- //
function searchProducts() {
    console.log('Searching products');
    var query = $('#search-query').val(); // Use jQuery to get the query value
    $.ajax({
        url: '/search_product',
        type: 'GET',
        data: {query: query},
        success: function (response) {
            if (response.success) {
                var tableBody = $('#table tbody'); // Use jQuery to select the table body
                tableBody.empty(); // Clear the current table rows

                // console.log(response.suppliers);
                // console.log(response.categories);

                // Iterate over the response products and append each as a new row
                response.products.forEach(function (product) {
                    // console.log(product);
                    // console.log(response.suppliers);
                    // console.log(response.categories);
                    var row = generateRow(product, response.categories, response.suppliers);
                    tableBody.append(row); // Append the new row to the table body
                });
            } else {
                alert('Error searching products: ' + response.error);
            }
        },
        error: function (xhr, status, error) {
            alert('Error searching products: ' + xhr.responseText);
        }
    });
}

// ------------------- ADD PRODUCT ------------------- //
function addProduct() {
    const product_name = document.getElementById('product_name').value;
    const product_brand = document.getElementById('product_brand').value;
    const product_price = document.getElementById('product_price').value;
    const product_stock = document.getElementById('product_stock').value;
    const product_photo = document.getElementById('product_photo').value;
    const product_category = document.getElementById('product_category').value;
    const product_supplier = document.getElementById('product_supplier').value;
    const product_description = document.getElementById('product_description').value;

    // Basic validation
    if (!product_name || !product_brand || !product_price || !product_stock
        || !product_category || !product_supplier || !product_description) {
        alert('Please fill in all required fields.');
        return;
    }

    // Send data to server
    fetch('/add_product', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            product_name,
            product_brand,
            product_price,
            product_stock,
            product_photo,
            product_category,
            product_supplier,
            product_description
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Product added successfully!');
                closeAddModal();
                // Refresh the table
                fetchProducts(currentPage);
            } else {
                alert('Error adding product: ' + data.error);
            }
        })
        .catch(error => {
            console.error(error);
            alert('An error occurred while adding the product.');
        });
}

// ------------------- PAGINATION ------------------- //
let currentPage = 1;
const limit = 10; // rows per page

function generateRow(product, categories, suppliers) {
    // console.log(product);
    // console.log(categories);
    // console.log(suppliers);
    return `
        <tr id="row-${product.product_id}">
        <!-- Product ID -->
        <td>${product.product_id}</td>
        
        <!-- Name + Photo in same cell -->
        <td>
            <div class="product-name-photo">
                <img src="${product.photo}" alt="Product Image">
                <div class="product-name">
                    <span id="name-${product.product_id}-text">${product.product_name}</span>
                    <input type="text" id="name-${product.product_id}-input"
                           value="${product.product_name}" style="display:none; width: 100px;">
                </div>
            </div>
        </td>

       <!-- Category ID -->
      <td>
        <!-- Non-edit mode text -->
        <span id="category-${product['product_id']}-text">
          ${product['category_id']}
        </span>

        <!-- Dropdown for edit mode -->
        <select
          id="category-${product['product_id']}-input"
          style="display: none; width: 150px;"
        >
          ${categories.map(cat => `
            <option
              value="${cat['category_id']}"
              ${cat['category_name'] === product['category_id'] ? 'selected' : ''}
            >
              ${cat['category_name']}
            </option>
          `).join('')}
        </select>
      </td>

      <!-- Supplier ID -->
      <td>
        <!-- Non-edit mode text -->
        <span id="supplier-${product['product_id']}-text">
          ${product.supplier_id}
        </span>

        <!-- Dropdown for edit mode -->
        <select
          id="supplier-${product['product_id']}-input"
          style="display: none; width: 150px;"
        >
          ${suppliers.map(sup => `
            <option
              value="${sup['supplier_id']}"
              ${sup['name'] === product['supplier_id'] ? 'selected' : ''}
            >
              ${sup['name']}
            </option>
          `).join('')}
        </select>
      </td>
        
        <!-- Brand -->
        <td>
            <span id="brand-${product.product_id}-text">${product.brand}</span>
            <input type="text" id="brand-${product.product_id}-input" value="${product.brand}"
                   style="display:none; width: 100px;">
        </td>

        <!-- Price -->
        <td>
            <span id="price-${product.product_id}-text">${product.price}</span>
            <input type="number" step="0.01" id="price-${product.product_id}-input"
                   value="${product.price}" style="display:none; width: 100px;">
        </td>

        <!-- Stock -->
        <td>
            <span id="stock-${product.product_id}-text">${product.stock_quantity}</span>
            <input type="number" id="stock-${product.product_id}-input"
                   value="${product.stock_quantity}" style="display:none; width: 100px;">
        </td>

        <!-- Description with pencil icon to trigger edit -->
        
       
        <td>
            <button class="btn"
                    data-product='${JSON.stringify(product)}'
                    onclick="openDescriptionModal(this)">
                Show Description
            </button>
                </td>
        
         
         
       

        <!-- Actions: 3 vertical dots dropdown + Save button -->
        <td class="action-buttons">
            <!-- Three-dots dropdown -->
            <div class="dropdown" id="three-dots-${product.product_id}">
                <!-- Replace "..." with the vertical ellipsis character -->
                <button class="three-dots-btn" onclick="toggleDropdown(${product.product_id})">
                    ⋮
                </button>
                <div class="dropdown-content">
                    <a onclick="enableEditProduct(${product.product_id})">Edit</a>
                    <a onclick="deleteProduct(${product.product_id})">Make Unavailable</a>
                </div>
            </div>
        
            <!-- Save button (hidden by default) -->
            <button id="save-btn-${product.product_id}"
                    class="save"
                    style="display: none;"
                    onclick="saveEditProduct(${product.product_id})">
                Save
            </button>
        </td>
    </tr>`;
}


async function fetchProducts(page = 1) {
    try {
        const response = await fetch(`/get_products?page=${page}&limit=${limit}`);
        const data = await response.json();
        // console.log(data.categories);
        // console.log(data.suppliers);

        if (data.success) {
            const tableBody = document.querySelector('#table tbody');
            tableBody.innerHTML = '';

            data.products.forEach(product => {
                const rowHTML = generateRow(product, data.categories, data.suppliers);
                tableBody.insertAdjacentHTML('beforeend', rowHTML);
            });

            document.getElementById('currentPage').innerText = `Page ${data.page}`;
            document.getElementById('prevPage').disabled = data.page === 1;
            document.getElementById('nextPage').disabled = data.page * limit >= data.total_count;
        } else {
            console.error('Error fetching products:', data.error);
        }
    } catch (err) {
        console.error('Error fetching products:', err);
    }
}

// Pagination buttons
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchProducts(currentPage);
    }
});
document.getElementById('nextPage').addEventListener('click', () => {
    currentPage++;
    fetchProducts(currentPage);
});

// Initial fetch
fetchProducts(currentPage);

// ------------------- MODALS ------------------- //
function openDescriptionModal(button) {
    // Set the description in the modal's <p>
    const product = JSON.parse(button.getAttribute('data-product'));

    products=[product]
    console.log(products);

    console.log(product.product_id);
    console.log(product.product_description);
    document.getElementById('description-modal-text').innerText = product.product_description;

    // Store the product in the Save button's data-product attribute
    const saveButton = document.getElementById('save-description-btn');
    saveButton.setAttribute('data-product', JSON.stringify(product));

    // Reset the textarea in case it was used before
    document.getElementById('description-textarea').value = '';

    // Ensure the edit area is hidden and the default buttons are visible
    document.getElementById('edit-description-area').style.display = 'none';
    document.getElementById('edit-description-btn').style.display = 'inline-block';

    // Show the modal
    document.getElementById('description-modal').style.display = 'block';
}

function closeDescriptionModal() {

        // Hide the modal
    document.getElementById('description-modal').style.display = 'none';

    // Clear the textarea and other fields in the modal
    document.getElementById('description-textarea').value = '';
    document.getElementById('description-modal-text').innerText = '';
}


function enableEditDescription() {
    // Hide the <p> and "Edit Description" button
    document.getElementById('description-modal-text').style.display = 'none';
    document.getElementById('edit-description-btn').style.display = 'none';
    document.getElementById('save-description-btn').style.display = 'block';

    // Populate the textarea with the current description
    const currentDesc = document.getElementById('description-modal-text').innerText;
    document.getElementById('description-textarea').value = currentDesc;


    // Show the textarea and Save button
    document.getElementById('edit-description-area').style.display = 'block';
}

function saveDescriptionEdit() {
    // Parse the product data from the Save button's data-product attribute

    // Get the updated description from the textarea
    const updatedDescription = document.getElementById('description-textarea').value;

    // Update the product object with the new description
    //products[0].product_description = updatedDescription;
    products[0].product_description = updatedDescription;

    // Send the updated product to the server
    fetch(`/update_description/${products[0].product_id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(products[0]),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Description updated successfully!');

                // Update the table row with the new description
                document.getElementById(`row-${products[0].product_id}`)
                    .querySelector('.btn[data-product]')
                    .setAttribute('data-product', JSON.stringify(products[0]));

                // Close the modal
                closeDescriptionModal();
            } else {
                alert('Error updating description: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the description.');
        });
}




function openAddModal() {
    document.getElementById('add-product-modal').classList.add('show');
}

function closeAddModal() {
    document.getElementById('add-product-modal').classList.remove('show');
    // Clear the form if desired
    document.getElementById('add-product-form').reset();
}


