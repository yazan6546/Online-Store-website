const modal = document.getElementById("blank-modal");
const openModalBtn = document.getElementById("open-modal-btn");
const closeModalBtn = document.querySelector(".close-btn");

// Ensure modal is hidden on page load
document.addEventListener("DOMContentLoaded", function () {
  modal.style.display = "none";
});

// Open modal on button click
openModalBtn.addEventListener("click", function () {
  modal.style.display = "flex";
});

// Close modal on close button click
closeModalBtn.addEventListener("click", function () {
  modal.style.display = "none";
});

// Close modal when clicking outside
window.addEventListener("click", function (e) {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});


const decreaseBtn = document.getElementById('decrease-qty');
const increaseBtn = document.getElementById('increase-qty');
const quantityValue = document.querySelector('.quantity-value');

decreaseBtn.addEventListener('click', () => {
  let currentValue = parseInt(quantityValue.textContent);
  if (currentValue > 1) {
    quantityValue.textContent = currentValue - 1;
  }
});

increaseBtn.addEventListener('click', () => {
  let currentValue = parseInt(quantityValue.textContent);
  quantityValue.textContent = currentValue + 1;
});



// Add event listener for the "Add to Cart" button
document.querySelector('.add-to-cart').addEventListener('click', function () {
    // Get the notification element
    const notification = document.getElementById('notification');

    // Show the notification by adding the "show" class
    notification.classList.add('show');

    // Hide the notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
});
