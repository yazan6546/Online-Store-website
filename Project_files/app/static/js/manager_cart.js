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
