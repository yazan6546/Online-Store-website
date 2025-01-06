/////////////////////////////////QUANTITY SELECTION//////////////////////////////////////////
document.querySelectorAll('.quantity-selector').forEach(selector => {
  const decreaseBtn = selector.querySelector('.quantity-btn.decrease-qty');
  const increaseBtn = selector.querySelector('.quantity-btn.increase-qty');
  const quantityValue = selector.querySelector('.quantity-value');

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
});

/////////////////////////////////DELIVERY SERVICE//////////////////////////////////////
// Dummy delivery services data
const deliveryServices = [
  {
    id: 1,
    name: "Standard Delivery",
    phone: "+1-800-555-1234"
  },
  {
    id: 2,
    name: "Express Delivery",
    phone: "+1-800-555-5678"
  },
  {
    id: 3,
    name: "Same Day Delivery",
    phone: "+1-800-555-9101"
  }
];

// Populate the dropdown dynamically
const deliveryDropdown = document.getElementById("delivery-dropdown");

deliveryServices.forEach(service => {
  const option = document.createElement("option");
  option.value = service.id;
  option.textContent = `${service.name} (${service.phone})`;
  deliveryDropdown.appendChild(option);
});
