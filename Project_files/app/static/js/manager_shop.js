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