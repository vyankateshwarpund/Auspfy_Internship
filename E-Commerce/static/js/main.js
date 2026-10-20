/**
 * Auspify Shop - Main ES6+ Client Integration Scripts
 * Manages Fetch API interactions for Cart, Notifications, and CSRF protection.
 */

// Helper to extract CSRF token from HTML meta or cookies
function getCSRFToken() {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag && metaTag.content) {
        return metaTag.content;
    }
    // Fallback to cookie
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Display Bootstrap 5 Toast Notification
function showToast(message, type = 'success') {
    const toastEl = document.getElementById('appToast');
    const toastMsg = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');

    if (!toastEl) {
        alert(message);
        return;
    }

    // Set styling based on type
    toastEl.className = 'toast align-items-center text-white border-0 shadow';
    if (type === 'success') {
        toastEl.classList.add('bg-success');
        toastIcon.className = 'bi bi-check-circle-fill fs-5 me-2';
    } else if (type === 'danger' || type === 'error') {
        toastEl.classList.add('bg-danger');
        toastIcon.className = 'bi bi-exclamation-triangle-fill fs-5 me-2';
    } else if (type === 'warning') {
        toastEl.classList.add('bg-warning', 'text-dark');
        toastIcon.className = 'bi bi-exclamation-circle-fill fs-5 me-2 text-dark';
    } else {
        toastEl.classList.add('bg-primary');
        toastIcon.className = 'bi bi-info-circle-fill fs-5 me-2';
    }

    toastMsg.textContent = message;
    const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
    toast.show();
}

// Update the global navbar cart counter badge
function updateNavbarCartBadge(count) {
    const badge = document.getElementById('nav-cart-badge');
    if (badge) {
        badge.textContent = count;
        if (count > 0) {
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    }
}

// Add Product to Cart via Fetch API
async function addToCart(productId, quantity = 1, buttonElement = null) {
    let originalButtonHtml = '';
    if (buttonElement) {
        originalButtonHtml = buttonElement.innerHTML;
        buttonElement.disabled = true;
        buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Adding...';
    }

    try {
        const response = await fetch('/api/cart/items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: parseInt(quantity, 10) || 1,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            showToast(data.message || 'Product added to cart!', 'success');
            if (data.cart && typeof data.cart.total_items !== 'undefined') {
                updateNavbarCartBadge(data.cart.total_items);
            }
        } else if (response.status === 401 || response.status === 403) {
            showToast('Please sign in to add items to your cart.', 'warning');
            setTimeout(() => {
                window.location.href = '/users/login/?next=' + encodeURIComponent(window.location.pathname);
            }, 1200);
        } else {
            const errorMsg = data.error || (data.errors ? Object.values(data.errors).flat().join(' ') : 'Could not add product to cart.');
            showToast(errorMsg, 'danger');
        }
    } catch (err) {
        console.error('Add to cart error:', err);
        showToast('Network error while adding to cart. Please try again.', 'danger');
    } finally {
        if (buttonElement) {
            buttonElement.disabled = false;
            buttonElement.innerHTML = originalButtonHtml;
        }
    }
}

// Global click event delegation for data-add-to-cart buttons
document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-add-to-cart]');
        if (btn) {
            e.preventDefault();
            const productId = btn.getAttribute('data-product-id');
            const qtyInput = document.getElementById('product-quantity-input');
            const quantity = qtyInput ? qtyInput.value : 1;
            addToCart(productId, quantity, btn);
        }
    });
});
