function initializeCarousel() {
    $('#carousel-related-product').slick({
        infinite: true,
        arrows: false,
        slidesToShow: 4,
        slidesToScroll: 3,
        dots: true,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 3
                }
            }
        ]
    });
}

function toggleCart() {
    const cartContainer = document.getElementById('cartContainer');
    const overlay = document.getElementById('overlay');
    cartContainer.classList.toggle('open'); // Slide the cart in/out
    overlay.classList.toggle('active'); // Show/hide the overlay
}

function showForm(formType) {
            const loginForm = document.getElementById('login-form');
            const signupForm = document.getElementById('signup-form');

            if (formType === 'login') {
                loginForm.style.display = 'block';
                signupForm.style.display = 'none';
            } else {
                loginForm.style.display = 'none';
                signupForm.style.display = 'block';
            }
}

function scrollCategories(direction) {
    const container = document.querySelector('.category-list');
    const scrollAmount = 300;
    container.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth',
    });
}

function showCategory(category) {
  const tabs = document.querySelectorAll('.tab');
  const productList = document.getElementById('product-list');

  // Update the active tab
  tabs.forEach((tab) => tab.classList.remove('active'));
  document.querySelector(`.tab[onclick="showCategory('${category}')"]`).classList.add('active');

  // Example: Change the product list dynamically
  productList.innerHTML = `<p>Showing products for ${category.replace('-', ' ')}</p>`;
}
