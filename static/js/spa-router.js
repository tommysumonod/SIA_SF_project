
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.profile-menu li');
    const pages = document.querySelectorAll('.tab-page');

    // ✅ Helper function to safely update URL hash without auto-scrolling
    function safeSetHash(hash) {
        const y = window.scrollY; // remember scroll position
        history.replaceState(null, null, `#${hash}`); // update hash silently
        window.scrollTo(0, y); // restore scroll position
    }

    // ✅ Function to show the active tab
    function showTab(tabId) {
        // Hide all pages
        pages.forEach(page => page.style.display = 'none');

        // Remove 'active' from all menu items
        tabs.forEach(tab => tab.classList.remove('active'));

        // Show selected page
        const activePage = document.getElementById(tabId);
        if (activePage) {
            activePage.style.display = 'block';
            activePage.classList.add('active');
        }

        // Highlight corresponding tab
        const activeTab = document.querySelector(`.profile-menu li[data-tab="${tabId}"]`);
        if (activeTab) activeTab.classList.add('active');
    }

    // ✅ Load correct tab on page load
    let hash = window.location.hash.substring(1);
    if (!hash) hash = 'profile-card'; // default tab
    showTab(hash);

    // ✅ Add click listeners for all tabs
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;

            // Show selected tab
            showTab(target);

            // Update URL hash without auto-scrolling
            safeSetHash(target);
        });
    });

    // ✅ Handle back/forward browser navigation
    window.addEventListener('hashchange', () => {
        const newHash = window.location.hash.substring(1);
        showTab(newHash || 'profile-card');
    });
});