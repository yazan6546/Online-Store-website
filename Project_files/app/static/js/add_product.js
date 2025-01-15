let filesToUpload = []; // Keep track of the selected files

// ------------------ DRAG-AND-DROP + BROWSE UPLOAD LOGIC ------------------ //
const uploadArea = $('#upload-area');
const uploadedFilesContainer = $('#uploaded-files');
const fileInput = $('#file-input');

// Highlight #1:
// If you only want a single file, you can still allow multiple selection in the UI.
// But we'll only send the first file to the server.

uploadArea.on('dragover', function (e) {
    e.preventDefault();
    uploadArea.css('border-color', 'blue');
});

uploadArea.on('dragleave', function (e) {
    e.preventDefault();
    uploadArea.css('border-color', '#aaa');
});

uploadArea.on('drop', function (e) {
    e.preventDefault();
    uploadArea.css('border-color', '#aaa');
    handleFiles(e.originalEvent.dataTransfer.files);
});

function browseFile() {
    fileInput.click();
}

fileInput.on('change', function () {
    handleFiles(this.files);
});

function handleFiles(files) {
    $.each(files, function (_, file) {
        filesToUpload.push(file);
        const fileItem = $(`
                <div class="uploaded-file">
                  <span>${file.name} (${Math.round(file.size / 1024)} KB)</span>
                  <button onclick="removeFile('${file.name}')">&#x1F5D1;</button>
                </div>
              `);
        uploadedFilesContainer.append(fileItem);
    });
}

window.removeFile = function (fileName) {
    filesToUpload = filesToUpload.filter(file => file.name !== fileName);
    uploadedFilesContainer.find('.uploaded-file').each(function () {
        if ($(this).text().includes(fileName)) {
            $(this).remove();
        }
    });
};

// ------------------ LOAD CATEGORIES & SUPPLIERS ON PAGE LOAD -------------- //
fetchCategories();
fetchSuppliers();

function fetchCategories() {
    console.log('fetching categories');
    $.ajax({
        url: '/fetch_categories',
        type: 'GET',
        success: function (data) {
            if (data.success) {
                const categorySelect = $('#category_select');
                $.each(data.categories, function (_, cat) {
                    categorySelect.append(`<option value="${cat}">${cat}</option>`);
                });
            } else {
                alert('Error loading categories: ' + data.error);
            }
        },
        error: function (err) {
            console.error(err);
            alert('Error loading categories.');
        }
    });
}

function fetchSuppliers() {
    console.log('fetching suppliers');
    $.ajax({
        url: '/fetch_suppliers', // Flask route
        type: 'GET',             // HTTP method
        success: function (data) {
            if (data.success) {
                const supplierSelect = $('#supplier_select'); // Target dropdown
                supplierSelect.empty(); // Clear any existing options
                supplierSelect.append('<option value="">Select Supplier...</option>'); // Default option

                // Populate dropdown with supplier options
                $.each(data.suppliers, function (_, supplierName) {
                    supplierSelect.append(`<option value="${supplierName}">${supplierName}</option>`);
                });
            } else {
                alert('Error loading suppliers: ' + data.error);
            }
        },
        error: function (err) {
            console.error(err);
            alert('Error loading suppliers.');
        }
    });
}

// ------------------ FORM SUBMIT / SAVE LOGIC ------------------ //
function cancelAdd() {
    window.location.href = "/admin_dashboard/products";
}

function saveProduct() {
    const productName = document.getElementById('product_name').value.trim();
    const categoryId = document.getElementById('category_select').value;
    const brand = document.getElementById('brand').value.trim();
    const supplierId = document.getElementById('supplier_select').value;
    const price = document.getElementById('price').value.trim();
    const stockQuantity = document.getElementById('stock_quantity').value.trim();
    const description = document.getElementById('description').value.trim();

    // Basic validation
    if (!productName) {
        alert('Please enter a product name.');
        return;
    }
    if (!categoryId) {
        alert('Please select a category.');
        return;
    }
    if (!brand) {
        alert('Please enter a brand.');
        return;
    }
    if (!supplierId) {
        alert('Please select a supplier.');
        return;
    }
    if (!price) {
        alert('Please enter price.');
        return;
    }
    if (!stockQuantity) {
        alert('Please enter stock quantity.');
        return;
    }
    if(stockQuantity<0){
        alert('Stock quantity cannot be negative');
        return;
    }
    if(price<0){
        alert('Price cannot be negative');
        return;
    }

    // FormData for files and form fields
    const formData = new FormData();
    formData.append('product_name', productName);
    formData.append('category_id', categoryId);
    formData.append('brand', brand);
    formData.append('supplier_id', supplierId);
    formData.append('price', price);
    formData.append('stock_quantity', stockQuantity);
    formData.append('description', description);

    // Highlight #2: We only want ONE file. So we'll append just the first file if it exists.
    // If you truly want multiple images, you'll need to adapt the backend code for multiple uploads.
    if (filesToUpload.length > 0) {
        // Use key 'image' (singular) to match the Flask code below
        formData.append('image', filesToUpload[0]);
    } else {
        // If no file was uploaded, you could handle that scenario here if needed
        console.warn('No image file selected');
    }

    // POST request to add product (including image)
    // Highlight #3: The route is changed to '/add_product/upload'
    // (Watch out for spelling: "upload" vs "uplode".)
    $.ajax({
        url: '/add_product/upload',   // Ensure it matches the Flask route exactly
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data.success) {
                alert('Product added successfully!');
                window.location.href = '/admin_dashboard/products';
            } else {
                alert('Error adding product: ' + data.error);
            }
        },
        error: function (err) {
            console.error(err);
            alert('An error occurred while adding the product.');
        }
    });
}
