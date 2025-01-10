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

    // Create a map of product ID to its corresponding modal
    const modals = {};
    products.forEach(product => {
        const productId = product.getAttribute('data-id');
        const productModal = document.querySelector(`#modal-${productId}`);
        if (productModal) {
            modals[productId] = productModal;
        }
    });

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

    // Clear the container
    productContainer.innerHTML = "";

    // Append sorted products and their corresponding modals
    products.forEach(product => {
        const productId = product.getAttribute('data-id');
        productContainer.appendChild(product);
        if (modals[productId]) {
            productContainer.appendChild(modals[productId]);
        }
    });
}


document.querySelectorAll('input[name="category"]').forEach((radio) => {
    radio.addEventListener('change', function () {
        const selectedCategory = this.value; // Selected category ID
        const productContainer = document.querySelector('.product-container');
        const products = Array.from(productContainer.querySelectorAll('.product-card'));

        // Filter products and their modals
        products.forEach((product) => {
            const productCategoryId = product.getAttribute('data-category');
            const productId = product.getAttribute('data-id');
            const productModal = document.querySelector(`#modal-${productId}`);

            if (selectedCategory === 'all' || productCategoryId === selectedCategory) {
                product.style.display = ''; // Show product card
                if (productModal) productModal.style.display = 'none'; // Hide modal until opened
            } else {
                product.style.display = 'none'; // Hide product card
                if (productModal) productModal.style.display = 'none'; // Hide modal
            }
        });
    });
});

/////////////////////////////////////////////////////////////////////////////////////////////////////
document.querySelectorAll('input[name="availability"]').forEach((radio) => {
    radio.addEventListener('change', (event) => {
        const selectedAvailability = event.target.value; // Get selected availability
        filterProductsByAvailability(selectedAvailability);
    });
});

function filterProductsByAvailability(availability) {
    const productCards = document.querySelectorAll('.product-card');

    productCards.forEach((card) => {
        const productAvailability = card.getAttribute('data-availability');

        if (availability === 'all' || availability === productAvailability) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
/////////////////////////////////////////////////////////////////////////////////////////
function updateProductCount() {
    const productCount = document.querySelectorAll(".product-card").length;
    document.getElementById("product-count").innerText = `${productCount} products`;
}

// Call the function initially to set the count
updateProductCount();

// Update the count whenever the products are filtered or sorted
document.querySelectorAll("input[name='availability'], input[name='category']").forEach(input => {
    input.addEventListener("change", updateProductCount);
});

document.getElementById("sort-options").addEventListener("change", updateProductCount);


fetch(`/filter_products?availability=${availability}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const productContainer = document.querySelector(".product-container");
            productContainer.innerHTML = ""; // Clear current products

            // Update product count
            document.getElementById("product-count").innerText = `${data.count} products`;

            // Render products
            data.products.forEach(product => {
                const productCard = `
                    <div class="product-card" data-id="${product.product_id}">
                        <div class="product-image-section">
                            <img src="${product.photo}" alt="${product.product_name}">
                        </div>
                        <div class="product-info-section">
                            <h5>${product.product_name}</h5>
                            <p class="price">$${product.price}</p>
                        </div>
                    </div>
                `;
                productContainer.insertAdjacentHTML("beforeend", productCard);
            });
        }
    });
//////////////////////////////////////////////////////////////////////////////////////
document.addEventListener("DOMContentLoaded", function () {
    const minPriceInput = document.getElementById("minPrice");
    const maxPriceInput = document.getElementById("maxPrice");
    const priceMinDisplay = document.getElementById("priceMin");
    const priceMaxDisplay = document.getElementById("priceMax");
    const productCards = document.querySelectorAll(".product-card");

    // Function to filter products based on price range
    function filterProductsByPrice() {
      const minPrice = parseFloat(minPriceInput.value);
      const maxPrice = parseFloat(maxPriceInput.value);

      priceMinDisplay.textContent = minPrice.toFixed(2);
      priceMaxDisplay.textContent = maxPrice.toFixed(2);

      productCards.forEach((card) => {
        const productPrice = parseFloat(card.getAttribute("data-price"));
        if (productPrice >= minPrice && productPrice <= maxPrice) {
          card.style.display = "block"; // Show the product
        } else {
          card.style.display = "none"; // Hide the product
        }
      });
    }

    // Attach event listeners to the range inputs
    minPriceInput.addEventListener("input", filterProductsByPrice);
    maxPriceInput.addEventListener("input", filterProductsByPrice);

    // Set initial values
    filterProductsByPrice();
});
