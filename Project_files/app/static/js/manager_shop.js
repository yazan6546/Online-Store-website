document.addEventListener("DOMContentLoaded", () => {
  // Hide all modals on page load
  document.querySelectorAll(".modal").forEach(modal => {
    modal.style.display = "none";
  });

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
});


////////////////////////////////////////////////////////
const products = [
  {
    id: "product1",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },
  {
    id: "product2",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },
  {
    id: "product3",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },
  {
    id: "product4",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },

    {
    id: "product4",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },

    {
    id: "product4",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },

    {
    id: "product4",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },

    {
    id: "product4",
    name: "AirPods Max",
    price: 220,
    description: `The ultimate over-ear personal listening experience — now in fresh new colors. AirPods Max deliver stunningly detailed, high-fidelity audio. Personalized Spatial Audio with dynamic head tracking for sound that surrounds you. Pro-level Active Noise Cancellation to remove unwanted sound. Transparency mode to comfortably hear the world around you. Up to 20 hours of battery life on a single charge. Effortless setup and on-head detection for a magical listening experience. Now with USB-C for easy charging.`,
    image: "../static/img/p9-d-removebg-preview.png",
  },

];

const productContainer = document.querySelector(".product-container");

products.forEach((product) => {
  const productCard = `
    <div class="product-card" data-id="${product.id}">
      <!-- Upper Section -->
      <div class="product-image-section">
        <img src="${product.image}" alt="${product.name}">
        <div class="circle-btn open-modal-btn" data-id="${product.id}">
          <i class="bx bx-plus"></i>
        </div>
      </div>
      <!-- Lower Section -->
      <div class="product-info-section">
        <h5>${product.name} offer high-fidelity audio, 20-hour battery life, USB-C charging, in fresh green color.</h5>
        <p class="price">$${product.price}</p>
      </div>
    </div>
    <!-- Modal for ${product.id} -->
    <div id="modal-${product.id}" class="modal">
      <div class="modal-content">
        <span class="close-btn" data-id="${product.id}">&times;</span>
        <h2>Product Details</h2>
        <div class="modal-body">
          <!-- Left Section: Image -->
          <div class="modal-image-section">
            <img src="${product.image}" alt="${product.name}">
          </div>
          <!-- Right Section: Details -->
          <div class="modal-description-section">
            <h5>${product.name} offer high-fidelity audio, 20-hour battery life, USB-C charging, in fresh green color.</h5>
            <p class="price">Price: $${product.price}</p>
            <p>Description: ${product.description}</p>
            <div class="quantity-cart-container">
              <div class="quantity-selector">
                <button class="quantity-btn decrease-qty" data-id="${product.id}">−</button>
                <span class="quantity-value" data-id="${product.id}">1</span>
                <button class="quantity-btn increase-qty" data-id="${product.id}">+</button>
              </div>
              <div id="notification-${product.id}" class="notification">ADDED TO YOUR CART</div>
              <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  productContainer.insertAdjacentHTML("beforeend", productCard);
});
