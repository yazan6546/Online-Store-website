// Toggle dropdown menu and close other dropdowns
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

// Add functionality for "Show Addresses"
// function showAddresses(personId) {
//     // Replace with your actual logic to fetch and display addresses
//     alert(`Show addresses for customer ID: ${personId}`);
// }


// Get references to the modal and close button
const addressModal = document.getElementById('address-modal');

const closeModalBtn = addressModal.querySelector('.close-btn');

// Function to show addresses in the modal
async function showAddresses(personId) {
    // Fetch addresses dynamically (you can replace this with an AJAX call if needed)
    const customerAddresses = await mockGetAddresses(personId); // Replace with backend call
    console.log(customerAddresses)
    currentCustomerID = personId;
    const addressTableBody = document.getElementById('address-table-body');
    addressTableBody.innerHTML = ''; // Clear existing rows

    customerAddresses.forEach((address) => {
        const row = `
            <tr id="address-row-${address.address_id}">
                <td>
                    <span id="street_address-${address.address_id}-text">${address.street}</span>
                    <input type="text" id="street_address-${address.address_id}-input" value="${address.street}" style="display:none; width: 300px;">
                </td>
                <td>
                    <span id="city-${address.address_id}-text">${address.city}</span>
                    <input type="text" id="city-${address.address_id}-input" value="${address.city}" style="display:none; width: 100px;">
                </td>
                <td>
                    <span id="zip_code-${address.address_id}-text">${address.zip_code}</span>
                    <input type="text" id="zip_code-${address.address_id}-input" value="${address.zip_code}" style="display:none; width: 100px;">
                </td>
                <td class="action-buttons">
                    <button id="edit-address-btn-${address.address_id}" class="edit" onclick="enableEditAddress(${address.address_id})">Edit</button>
                    <button id="save-address-btn-${address.address_id}" class="save" style="display:none;" onclick="saveEditAddress(${address.address_id})">Save</button>
                    <button class="delete" onclick="deleteAddress(${address.address_id})">Delete</button>
                </td>
            </tr>
        `;
        addressTableBody.innerHTML += row;
    });

    // Show the modal
    addressModal.style.display = 'flex';
}


async function showAddress(address_id) {
    try {
        const response = await fetch(`/api/get_address/${address_id}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const address = await response.json();

        const addressTableBody = document.getElementById('address-table-body');
        addressTableBody.innerHTML = ''; // Clear existing rows

        const row = `
            <tr id="address-row-${address.address_id}">
                <td>
                    <span id="street_address-${address.address_id}-text">${address.street}</span>
                </td>
                <td>
                    <span id="city-${address.address_id}-text">${address.city}</span>
                </td>
                <td>
                    <span id="zip_code-${address.address_id}-text">${address.zip_code}</span>
                </td>
                
            </tr>
        `;
        addressTableBody.innerHTML += row;

        // Show the modal
        addressModal.style.display = 'flex';
    } catch (error) {
        console.error('Error fetching address:', error);
    }
}

async function showManagerOrder(OrderId) {
    // Fetch addresses dynamically (you can replace this with an AJAX call if needed)
    const OrderDetails = await mockGetOrder(OrderId); // Replace with backend call
    console.log(OrderDetails)
    currentOrderID = OrderId;
    const orderTableBody = document.getElementById('order-table-body');
    orderTableBody.innerHTML = ''; // Clear existing rows

    OrderDetails.forEach((order) => {
        const row = `
            <tr id="order-row-${order.order_id}">
                <td>
                    <span id="order_id-${order.order_id}-text">${order.order_id}</span>
                    <input type="text" id="order_id-${order.order_id}-input" value="${order.order_id}" style="display:none; width: 300px;">
                </td>
                <td>
                    <span id="order_date-${order.order_id}-text">${order.order_date}</span>
                    <input type="text" id="order_date-${order.order_id}-input" value="${order.order_date}" style="display:none; width: 100px;">
                </td>
                <td>
                    <span id="order_total-${order.order_id}-text">${order.order_total}</span>
                    <input type="text" id="order_total-${order.order_id}-input" value="${order.order_total}" style="display:none; width: 100px;">
                </td>
                <td class="action-buttons">
                    <button id="edit-order-btn-${order.order_id}" class="edit" onclick="enableEditOrder(${order.order_id})">Edit</button>
                    <button id="save-order-btn-${order.order_id}" class="save" style="display:none;" onclick="saveEditOrder(${order.order_id})">Save</button>
                    <button class="delete" onclick="deleteOrder(${order.order_id})">Delete</button>
                </td>
            </tr>
        `;
        orderTableBody.innerHTML += row;
    });

    // Show the modal
    addressModal.style.display = 'flex';
}



// Close the modal
closeModalBtn.addEventListener('click', () => {
    addressModal.style.display = 'none';
});

// Close the modal when clicking outside of it
window.addEventListener('click', (e) => {
    if (e.target === addressModal) {
        addressModal.style.display = 'none';
    }
});

// Function to fetch address data from the server
async function mockGetAddresses(personId) {
    try {
        const response = await fetch(`/api/get_addresses/${personId}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching addresses:', error);
        return [];
    }
}






async function mockGetOrder(OrderId) {
    try {
        const response = await fetch(`/api/get_order/${OrderId}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching addresses:', error);
        return [];
    }
}

///////////////////////////////////////////////////////////