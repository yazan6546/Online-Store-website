function openModal(productId) {
  document.getElementById(`modal-${productId}`).style.display = "flex";
}

function closeModal(productId) {
  document.getElementById(`modal-${productId}`).style.display = "none";
}

function updateQuantity(productId, action) {
  const quantityValue = document.querySelector(`.quantity-value[data-id="${productId}"]`);
  let currentValue = parseInt(quantityValue.textContent);

  if (action === 'decrease' && currentValue > 1) {
    quantityValue.textContent = currentValue - 1;
  } else if (action === 'increase') {
    quantityValue.textContent = currentValue + 1;
  }
}

function addToCart(productId) {
  const notification = document.querySelector(`#notification-${productId}`);
  const quantity = document.querySelector(`.quantity-value[data-id="${productId}"]`).textContent;
  const price = document.querySelector(`.product-card[data-id="${productId}"] .price`).textContent.replace('$', '');

  console.log('Product ID:', productId);
  console.log('Quantity:', quantity);
  console.log('Price:', price)

  // Send request to the server to add the product to the cart
  fetch(`/api/cart/add/${productId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      quantity: parseInt(quantity),
      price: parseFloat(price),
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Product added to cart:', data);
  })
  .catch(error => {
    console.error('Error adding product to cart:', error);
  });

  // Show the notification
  notification.classList.add("show");

  // Hide the notification after 3 seconds
  setTimeout(() => {
    notification.classList.remove("show");
  }, 3000);
}

/////////////////////////////////////////////////////////////
// Handle the sort functionality
const sortSelect = document.getElementById("sort-options");

// Event listener for sorting
sortSelect.addEventListener("change", function () {
    const selectedOption = this.value;
    sortProducts(selectedOption);
});

function sortProducts(criteria) {
    const productContainer = document.querySelector(".product-container");
    const products = Array.from(productContainer.querySelectorAll(".product-card"));

    // Sorting logic based on criteria
    products.sort((a, b) => {
        switch (criteria) {
            case "best-selling":
                return 0;
            case "a-z":
                return a.querySelector(".product-info-section h5").innerText.localeCompare(
                    b.querySelector(".product-info-section h5").innerText
                );
            case "z-a":
                return b.querySelector(".product-info-section h5").innerText.localeCompare(
                    a.querySelector(".product-info-section h5").innerText
                );
            case "low-high":
                return parseFloat(a.querySelector(".price").innerText.replace("$", "")) -
                       parseFloat(b.querySelector(".price").innerText.replace("$", ""));
            case "high-low":
                return parseFloat(b.querySelector(".price").innerText.replace("$", "")) -
                       parseFloat(a.querySelector(".price").innerText.replace("$", ""));
            default:
                return 0;
        }
    });

    // Clear the container and append sorted products
    productContainer.innerHTML = "";
    products.forEach(product => productContainer.appendChild(product));
}


//////////////////////////////////////////////////////////////////////
document.querySelectorAll('input[name="category"]').forEach((radio) => {
    radio.addEventListener('change', function () {
        const selectedCategory = this.value;

        // Fetch filtered products via AJAX
        fetch(`/filter_products?category=${encodeURIComponent(selectedCategory)}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    const productContainer = document.querySelector('.product-container');
                    productContainer.innerHTML = ''; // Clear current products

                    // Populate filtered products
                    data.products.forEach((product) => {
                        const productCard = `
                            <div class="product-card">
                                <div class="product-image-section">
                                    <img src="${product.photo}" alt="${product.product_name}">
                                </div>
                                <div class="product-info-section">
                                    <h5>${product.product_name}</h5>
                                    <p class="price">$${product.price}</p>
                                </div>
                            </div>`;
                        productContainer.insertAdjacentHTML('beforeend', productCard);
                    });
                } else {
                    alert('No products found for this category.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});
