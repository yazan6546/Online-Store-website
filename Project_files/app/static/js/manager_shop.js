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


const decreaseQtyBtn = document.getElementById('decrease-qty');
const increaseQtyBtn = document.getElementById('increase-qty');
const quantityDisplay = document.getElementById('quantity');

let quantity = 1;

decreaseQtyBtn.addEventListener('click', () => {
  if (quantity > 1) {
    quantity--;
    quantityDisplay.textContent = quantity;
  }
});

increaseQtyBtn.addEventListener('click', () => {
  quantity++;
  quantityDisplay.textContent = quantity;
});
