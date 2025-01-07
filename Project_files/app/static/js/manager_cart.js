// /////////////////////////////////QUANTITY SELECTION//////////////////////////////////////////
// document.querySelectorAll('.quantity-selector').forEach(selector => {
//   const decreaseBtn = selector.querySelector('.quantity-btn.decrease-qty');
//   const increaseBtn = selector.querySelector('.quantity-btn.increase-qty');
//   const quantityValue = selector.querySelector('.quantity-value');
//
//   decreaseBtn.addEventListener('click', () => {
//     let currentValue = parseInt(quantityValue.textContent);
//     if (currentValue > 1) {
//       quantityValue.textContent = currentValue - 1;
//     }
//   });
//
//   increaseBtn.addEventListener('click', () => {
//     let currentValue = parseInt(quantityValue.textContent);
//     quantityValue.textContent = currentValue + 1;
//   });
// });



// const deliveryServices = [
//   {
//     id: 1,
//     name: "Standard Delivery",
//     phone: "+1-800-555-1234"
//   },
//   {
//     id: 2,
//     name: "Express Delivery",
//     phone: "+1-800-555-5678"
//   },
//   {
//     id: 3,
//     name: "Same Day Delivery",
//     phone: "+1-800-555-9101"
//   }
// ];
function removeProduct(productId) {
    fetch(`/api/cart/remove/${productId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the cart item element from the DOM
            const cartItem = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
            if (cartItem) {
                // Get the quantity and price of the item that was deleted
                const quantityValue = cartItem.querySelector('.quantity-value');
                const quantity = parseInt(quantityValue.textContent);
                const priceElement = cartItem.querySelector('.item-price');
                const price = parseFloat(priceElement.textContent.replace('$', '')) / quantity;
                cartItem.remove();

                // Optionally, update the cart summary
                updateCartSummary(price*quantity);
            }

        } else {
            console.error('Failed to remove product:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateCartSummary(amountToSubtract) {
    // Update the total element
    const totalElement = document.getElementById('total');
    if (totalElement) {
        let total = parseFloat(totalElement.textContent.replace('$', ''));
        total -= amountToSubtract;
        totalElement.textContent = `$${total.toFixed(2)}`;
    }

    // Optionally, update the sub-total element if necessary
    const subTotalElement = document.getElementById('sub-total');
    if (subTotalElement) {
        let subTotal = parseFloat(subTotalElement.textContent.replace('$', ''));
        subTotal -= amountToSubtract;
        subTotalElement.textContent = `$${subTotal.toFixed(2)}`;
    }
}


function updateQuantityCart(productId, action) {
  const quantityValue = document.querySelector(`.quantity-value[data-id="${productId}"]`);
  const priceElement = document.querySelector(`.item-price[data-id="${productId}"]`);
  let currentValue = parseInt(quantityValue.textContent);
  const unitPrice = parseFloat(priceElement.getAttribute('data-unit-price'));

  if (action === 'decrease' && currentValue > 1) {
      console.log("ok")
    currentValue -= 1;
      updateCartSummaryQuantity("decrement");
  } else if (action === 'increase') {
    currentValue += 1;
        updateCartSummaryQuantity("increment");
  } else {
    return; // Exit if no valid action
  }

  quantityValue.textContent = currentValue;
  const newPrice = unitPrice * currentValue;
  priceElement.textContent = `$${newPrice.toFixed(2)}`;

  // Send request to the server with the updated quantity
  fetch(`/api/cart/update_quantity/${productId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ quantity: currentValue })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Quantity updated:', data);
  })
  .catch(error => {
    console.error('Error updating quantity:', error);
  });
}


function updateCartSummaryQuantity(option) {
  const totalElement = document.getElementById('total');
  const subTotalElement = document.getElementById('sub-total');
  let total = 0;
  let subTotal = 0;

  if (option === "increment"){  // Increment the total and sub-total
      document.querySelectorAll('.item-price').forEach(priceElement => {
          const price = parseFloat(priceElement.textContent.replace('$', ''));
          console.log(price)
          total += price;
          subTotal += price; // Adjust this if sub-total calculation differs
      });
  }

  else if (option === "decrement") { // Decrement the total and sub-total
        document.querySelectorAll('.item-price').forEach(priceElement => {
            const price = parseFloat(priceElement.textContent.replace('$', ''));
            total -= price;
            subTotal -= price; // Adjust this if sub-total calculation differs
        });
    }

  else {
      console.error('Invalid option:', option);
      return;
  }

  totalElement.textContent = `$${total.toFixed(2)}`;
  subTotalElement.textContent = `$${subTotal.toFixed(2)}`;
}