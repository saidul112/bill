// Main JavaScript functionality

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Help Modal functions
function openHelpModal() {
    const modal = document.getElementById('helpModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeHelpModal() {
    const modal = document.getElementById('helpModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

// Language Menu Toggle
function toggleLanguageMenu() {
    const menu = document.getElementById('languageMenu');
    if (menu) {
        menu.classList.toggle('show');
    }
}

// Close language menu when clicking outside
document.addEventListener('click', function(event) {
    const languageSelector = document.querySelector('.language-selector');
    const menu = document.getElementById('languageMenu');
    
    if (languageSelector && menu && !languageSelector.contains(event.target)) {
        menu.classList.remove('show');
    }
});

// Google Translate function using web interface
function translatePage(targetLang) {
    // Close the language menu
    const menu = document.getElementById('languageMenu');
    if (menu) {
        menu.classList.remove('show');
    }

    // Store language preference
    localStorage.setItem('preferredLanguage', targetLang);

    if (targetLang === 'en') {
        // Reset to English by removing cookies and reloading
        clearTranslationCookies();
        window.location.reload();
        return;
    }

    // Set the Google Translate cookie to trigger translation
    // Cookie format: googtrans=/en/TARGET_LANG
    const cookieValue = `/en/${targetLang}`;
    document.cookie = `googtrans=${cookieValue}; path=/; max-age=31536000`; // 1 year
    document.cookie = `googtrans=${cookieValue}; path=/; domain=${window.location.hostname}; max-age=31536000`;
    
    // Initialize Google Translate if not already loaded
    if (!window.googleTranslateLoaded) {
        loadGoogleTranslate();
    } else {
        // If already loaded, just reload the page with the new cookie
        window.location.reload();
    }
}

function clearTranslationCookies() {
    // Remove all Google Translate cookies
    const cookies = ['googtrans', 'googtrans'];
    cookies.forEach(name => {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname};`;
    });
}

function loadGoogleTranslate() {
    // Create the Google Translate element container (hidden)
    if (!document.getElementById('google_translate_element')) {
        const translateDiv = document.createElement('div');
        translateDiv.id = 'google_translate_element';
        translateDiv.style.display = 'none';
        document.body.appendChild(translateDiv);
    }

    // Define the initialization callback
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,zh-CN,zh-TW,ja,bn,es,fr,de,hi,ko,ar,pt,ru,it,nl,pl,tr,vi,id,th,sv,cs,da,fi,no,uk,ro,hu,el,he,ms,sk,hr',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
        
        window.googleTranslateLoaded = true;
    };

    // Load the Google Translate script
    if (!document.getElementById('google-translate-script')) {
        const script = document.createElement('script');
        script.id = 'google-translate-script';
        script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        script.async = true;
        document.body.appendChild(script);
    }
}

// Check for saved language preference on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load Google Translate on every page
    loadGoogleTranslate();
    
    // Check if there's a saved preference
    const preferredLang = localStorage.getItem('preferredLanguage');
    if (preferredLang && preferredLang !== 'en') {
        // Ensure the cookie is set for the preferred language
        const cookieValue = `/en/${preferredLang}`;
        document.cookie = `googtrans=${cookieValue}; path=/; max-age=31536000`;
        document.cookie = `googtrans=${cookieValue}; path=/; domain=${window.location.hostname}; max-age=31536000`;
    }
});

// Close modals on outside click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                if (modal.id === 'helpModal') {
                    document.body.style.overflow = 'auto';
                }
            }
        });
    });
});

// Close help modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const helpModal = document.getElementById('helpModal');
        if (helpModal && helpModal.style.display === 'flex') {
            closeHelpModal();
        }
    }
});
