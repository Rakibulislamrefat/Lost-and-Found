/* ====================================
   Lost & Found Portal — Main JavaScript
   ==================================== */

document.addEventListener('DOMContentLoaded', () => {
    initHamburgerMenu();
    initImagePreview();
    initAutoHideAlerts();
    initSearchShortcut();
});

/* ---------- Hamburger Mobile Menu ---------- */
function initHamburgerMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.navbar-links');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
        });
    }
}

/* ---------- Image Preview on Upload ---------- */
function initImagePreview() {
    const imageInput = document.querySelector('input[type="file"][accept="image/*"]');
    if (!imageInput) return;

    // Create preview container if it doesn't exist
    let previewContainer = document.querySelector('.image-preview');
    if (!previewContainer) {
        previewContainer = document.createElement('div');
        previewContainer.className = 'image-preview';
        previewContainer.style.display = 'none';
        previewContainer.innerHTML = '<img id="preview-img" src="" alt="Image preview">';
        imageInput.parentElement.appendChild(previewContainer);
    }

    const previewImg = previewContainer.querySelector('img');

    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (event) => {
                previewImg.src = event.target.result;
                previewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.style.display = 'none';
            previewImg.src = '';
        }
    });
}

/* ---------- Auto-hide Django Messages ---------- */
function initAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s, transform 0.5s';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
}

/* ---------- Search Shortcut (Ctrl+K) ---------- */
function initSearchShortcut() {
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('.hero-search input, .search-input');
            if (searchInput) {
                searchInput.focus();
                searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
}
