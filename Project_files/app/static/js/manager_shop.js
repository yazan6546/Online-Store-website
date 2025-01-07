document.addEventListener("DOMContentLoaded", () => {
  // Fetch products from the server
  fetch('/api/products')
    .then(response => response.json())
    .then(products => {
      const productContainer = document.querySelector(".product-container");

      products.forEach(product => {
        const productCard = `
          <div class="product-card" data-id="${product.product_id}">
            <!-- Upper Section -->
            <div class="product-image-section">
              <img src="${product.photo}" alt="${product.product_name}">
              <div class="circle-btn open-modal-btn" data-id="${product.product_id}">
                <i class="bx bx-plus"></i>
              </div>
            </div>
            <!-- Lower Section -->
            <div class="product-info-section">
              <h5>${product.product_name} offer high-fidelity audio, 20-hour battery life, USB-C charging, in fresh green color.</h5>
              <p class="price">$${product.price}</p>
            </div>
          </div>
          <!-- Modal for ${product.product_id} -->
          <div id="modal-${product.product_id}" class="modal" style="display: none;">
            <div class="modal-content">
              <span class="close-btn" data-id="${product.product_id}">&times;</span>
              <h2>Product Details</h2>
              <div class="modal-body">
                <!-- Left Section: Image -->
                <div class="modal-image-section">
                  <img src="${product.photo}" alt="${product.product_name}">
                </div>
                <!-- Right Section: Details -->
                <div class="modal-description-section">
                  <h5>${product.product_name}</h5>
                  <p class="price">Price: $${product.price}</p>
                  <p>Description: ${product.product_description}</p>
                  <div class="quantity-cart-container">
                    <div class="quantity-selector">
                      <button class="quantity-btn decrease-qty" data-id="${product.product_id}">−</button>
                      <span class="quantity-value" data-id="${product.product_id}">1</span>
                      <button class="quantity-btn increase-qty" data-id="${product.product_id}">+</button>
                    </div>
                    <div id="notification-${product.product_id}" class="notification">ADDED TO YOUR CART</div>
                    <button class="add-to-cart" data-id="${product.product_id}">Add to Cart</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
        productContainer.insertAdjacentHTML("beforeend", productCard);

        // Explicitly hide the modal after it's added to the DOM
        const modal = document.getElementById(`modal-${product.product_id}`);
        modal.style.display = "none";
      });

      // Add event listeners for modals and quantity buttons after products are added to the DOM
      addEventListeners();
    })
    .catch(error => console.error('Error fetching products:', error));
});

function addEventListeners() {
  // Open modal for the clicked product
  document.querySelectorAll(".circle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = btn.getAttribute("data-id");
      document.getElementById(`modal-${productId}`).style.display = "flex";
    });
  });

  // Close modal when close button is clicked
  document.querySelectorAll(".close-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = btn.getAttribute("data-id");
      document.getElementById(`modal-${productId}`).style.display = "none";
    });
  });

  // Close modal when clicking outside
  window.addEventListener("click", event => {
    document.querySelectorAll(".modal").forEach(modal => {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });
  });

  // Update quantity dynamically
  document.querySelectorAll(".quantity-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = btn.getAttribute("data-id");
      const quantityValue = document.querySelector(`.quantity-value[data-id="${productId}"]`);
      let currentValue = parseInt(quantityValue.textContent);

      if (btn.classList.contains("decrease-qty") && currentValue > 1) {
        quantityValue.textContent = currentValue - 1;
      } else if (btn.classList.contains("increase-qty")) {
        quantityValue.textContent = currentValue + 1;
      }
    });
  });

  // Handle Add to Cart Notification
  document.querySelectorAll(".add-to-cart").forEach(btn => {
    btn.addEventListener("click", () => {
      const productId = btn.getAttribute("data-id");
      const notification = document.querySelector(`#notification-${productId}`);

      // Show the notification
      notification.classList.add("show");

      // Hide the notification after 3 seconds
      setTimeout(() => {
        notification.classList.remove("show");
      }, 3000);
    });
  });
}
