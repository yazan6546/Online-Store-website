// Keep track of sort order
let currentSortOrder = 'asc';


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
        if (['product_id','price','stock_quantity','category_id','supplier_id']
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
        case 'product_id':     return 1;
        case 'product_name':   return 2;
        case 'category_id':    return 3;
        case 'supplier_id':    return 4;
        case 'brand':          return 5;
        case 'price':          return 6;
        case 'stock_quantity': return 7;
        // description = 8, actions = 9
        default: return 1;
    }
}

// ------------------- ENABLE EDIT ------------------- //
function enableEditProduct(product_id) {
    console.log('Enabling edit for product ID:', product_id);

    // Hide the 3-dots dropdown
    document.getElementById(`three-dots-${product_id}`).style.display = 'none';
    // Show the Save button
    document.getElementById(`save-btn-${product_id}`).style.display = 'inline';

    // Name
    document.getElementById(`name-${product_id}-text`).style.display = 'none';
    document.getElementById(`name-${product_id}-input`).style.display = 'inline';

    // Category
    document.getElementById(`category-${product_id}-text`).style.display = 'none';
    document.getElementById(`category-${product_id}-input`).style.display = 'inline';

    // Supplier
    document.getElementById(`supplier-${product_id}-text`).style.display = 'none';
    document.getElementById(`supplier-${product_id}-input`).style.display = 'inline';

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
function enableDescriptionEdit(product_id) {
    console.log('Enabling description edit for product ID:', product_id);
    // Hide the static text
    document.getElementById(`description-${product_id}-text`).style.display = 'none';
    // Hide the pencil
    document.getElementById(`desc-edit-icon-${product_id}`).style.display = 'none';
    // Show the textarea
    document.getElementById(`description-edit-container-${product_id}`).style.display = 'block';

    // Pre-fill the textarea with existing text
    const descValue = document.getElementById(`description-${product_id}-text`).innerText;
    document.getElementById(`description-${product_id}-input`).value = descValue;

    // Also hide the 3-dots & show Save button if not in "edit" mode
    document.getElementById(`three-dots-${product_id}`).style.display = 'none';
    document.getElementById(`save-btn-${product_id}`).style.display = 'inline';
}

// ------------------- SAVE EDIT ------------------- //
function saveEditProduct(product_id) {
    console.log('Saving edit for product ID:', product_id);

    // Gather new values
    const product_name   = document.getElementById(`name-${product_id}-input`).value;
    const category_id    = document.getElementById(`category-${product_id}-input`).value;
    const supplier_id    = document.getElementById(`supplier-${product_id}-input`).value;
    const brand          = document.getElementById(`brand-${product_id}-input`).value;
    const price          = document.getElementById(`price-${product_id}-input`).value;
    const stock_quantity = document.getElementById(`stock-${product_id}-input`).value;

    // For description
    let newDescription = null;
    const descContainer = document.getElementById(`description-edit-container-${product_id}`);
    if (descContainer.style.display === 'block') {
        newDescription = document.getElementById(`description-${product_id}-input`).value;
    }

    // Example: Make an AJAX call to update on the server
    // (Using fetch as an example)
    fetch(`/update_product/${product_id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            product_name,
            category_id,
            supplier_id,
            brand,
            price,
            stock_quantity,
            product_description: newDescription // only if changed
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

            if (newDescription !== null) {
                document.getElementById(`description-${product_id}-text`).innerText = newDescription;
            }

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

            // Hide the description-edit container if it was open
            if (descContainer.style.display === 'block') {
                descContainer.style.display = 'none';
                document.getElementById(`desc-edit-icon-${product_id}`).style.display = 'inline';
                document.getElementById(`description-${product_id}-text`).style.display = 'inline';
            }

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
        success: function(response) {
            if (response.success) {
                document.getElementById(`row-${product_id}`).remove();
            } else {
                alert('Error deleting product: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error deleting product: ' + xhr.responseText);
        }
    });
}

// ------------------- SEARCH ------------------- //
function searchProducts() {
    console.log('Searching products');
    var query = $('#search-query').val(); // Use jQuery to get the query value
    $.ajax({
        url: '/search_product',
        type: 'GET',
        data: { query: query },
        success: function(response) {
            if (response.success) {
                var tableBody = $('#table tbody'); // Use jQuery to select the table body
                tableBody.empty(); // Clear the current table rows

                // Iterate over the response products and append each as a new row
                response.products.forEach(function(product) {
                    var row = `
                        <tr id="row-${product.product_id}">
                            <td>${product.product_id}</td>
                            <td>
                                <div class="product-name-photo">
                                    <img src="${product.photo}" alt="Product Image">
                                    <div class="product-name">
                                        <span id="name-${product.product_id}-text">${product.product_name}</span>
                                        <input type="text" id="name-${product.product_id}-input" value="${product.product_name}" style="display:none; width: 100px;">
                                    </div>
                                </div>
                            </td>
                            <td>
                                <span id="category-${product.product_id}-text">${product.category_id}</span>
                                <input type="number" id="category-${product.product_id}-input" value="${product.category_id}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="supplier-${product.product_id}-text">${product.supplier_id}</span>
                                <input type="number" id="supplier-${product.product_id}-input" value="${product.supplier_id}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="brand-${product.product_id}-text">${product.brand}</span>
                                <input type="text" id="brand-${product.product_id}-input" value="${product.brand}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="price-${product.product_id}-text">${product.price}</span>
                                <input type="number" step="0.01" id="price-${product.product_id}-input" value="${product.price}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <span id="stock-${product.product_id}-text">${product.stock_quantity}</span>
                                <input type="number" id="stock-${product.product_id}-input" value="${product.stock_quantity}" style="display:none; width: 100px;">
                            </td>
                            <td>
                                <div>
                                    <span id="description-${product.product_id}-text">${product.product_description}</span>
                                    <span class="pencil-icon" id="desc-edit-icon-${product.product_id}" onclick="enableDescriptionEdit(${product.product_id})">✏️</span>
                                </div>
                                <div class="description-edit-container" id="description-edit-container-${product.product_id}" style="display:none; margin-top: 8px;">
                                    <textarea id="description-${product.product_id}-input" placeholder="Write your new description here..."></textarea>
                                </div>
                            </td>
                            <td class="action-buttons">
                                <button id="edit-btn-${product.product_id}" class="edit" onclick="enableEditProduct(${product.product_id})">Edit</button>
                                <button id="save-btn-${product.product_id}" class="save" style="display:none;" onclick="saveEditProduct(${product.product_id})">Save</button>
                                <button class="delete" onclick="deleteProduct(${product.product_id})">Delete</button>
                            </td>
                        </tr>`;
                    tableBody.append(row); // Append the new row to the table body
                });
            } else {
                alert('Error searching products: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error searching products: ' + xhr.responseText);
        }
    });
}
// function searchProducts() {
//     const query = $('#search-query').val(); // Get the search query
//     console.log('Searching products with query:', query);
//
//     // If query is empty, avoid making unnecessary AJAX calls and keep the current table content
//     if (!query.trim()) {
//         console.log('Empty search query. No action performed.');
//         return;
//     }
//
//     // Perform AJAX search when there is a query
//     $.ajax({
//         url: '/search_product',
//         type: 'GET',
//         data: { query: query },
//         success: function (response) {
//             if (response.success) {
//                 const tableBody = $('#table tbody');
//                 tableBody.empty(); // Clear existing rows
//                 response.products.forEach(function (product) {
//                     const row = `
//                         <tr id="row-${product.product_id}">
//                             <td>${product.product_id}</td>
//                             <td>
//                                 <div class="product-name-photo">
//                                     <img src="${product.photo}" alt="Product Image">
//                                     <div class="product-name">
//                                         <span id="name-${product.product_id}-text">${product.product_name}</span>
//                                     </div>
//                                 </div>
//                             </td>
//                             <td>${product.category_id}</td>
//                             <td>${product.supplier_id}</td>
//                             <td>${product.brand}</td>
//                             <td>${product.price}</td>
//                             <td>${product.stock_quantity}</td>
//                             <td>${product.product_description}</td>
//                             <td class="action-buttons">
//                                 <button onclick="enableEditProduct(${product.product_id})">Edit</button>
//                                 <button onclick="deleteProduct(${product.product_id})">Delete</button>
//                             </td>
//                         </tr>`;
//                     tableBody.append(row);
//                 });
//             } else {
//                 alert('Error searching products: ' + response.error);
//             }
//         },
//         error: function (xhr, status, error) {
//             alert('Error searching products: ' + xhr.responseText);
//         },
//     });
// }


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
        headers: { 'Content-Type': 'application/json' },
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

async function fetchProducts(page = 1) {
    try {
        const response = await fetch(`/get_products?page=${page}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            const tableBody = document.querySelector('#table tbody');
            tableBody.innerHTML = '';

            data.products.forEach(product => {
                const rowHTML = createTableRow(product);
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
function openAddModal() {
    document.getElementById('add-product-modal').classList.add('show');
}
function closeAddModal() {
    document.getElementById('add-product-modal').classList.remove('show');
    // Clear the form if desired
    document.getElementById('add-product-form').reset();
}


