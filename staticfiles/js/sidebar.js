// Sidebar Management - works on all pages
document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    // --- Helpers ---
    function updateToggleIcon() {
        if (!sidebarToggle || !sidebar) return;
        const icon = sidebarToggle.querySelector('i');
        if (!icon) return;
        icon.className = sidebar.classList.contains('collapsed')
            ? 'fas fa-angle-double-right'
            : 'fas fa-angle-double-left';
    }

    function updateTooltips() {
        if (!sidebar) return;
        const navLinks = sidebar.querySelectorAll('.nav-link, .settings-btn, .logout-btn');
        navLinks.forEach(link => {
            const textElement = link.querySelector('.nav-text');
            if (!textElement) return;
            if (sidebar.classList.contains('collapsed')) {
                link.setAttribute('title', textElement.textContent.trim());
            } else {
                link.removeAttribute('title');
            }
        });
    }

    function collapseSidebar() {
        if (!sidebar) return;
        sidebar.classList.add('collapsed');
        body.classList.add('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', 'true');
        updateToggleIcon();
        updateTooltips();
    }

    function expandSidebar() {
        if (!sidebar) return;
        sidebar.classList.remove('collapsed');
        body.classList.remove('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', 'false');
        updateToggleIcon();
        updateTooltips();
    }

    // --- Load saved state ---
    const savedState = localStorage.getItem('sidebarCollapsed');
    if (savedState === 'true') {
        collapseSidebar();
    } else if (savedState === 'false') {
        expandSidebar();
    }

    // --- Attach toggle ---
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function (e) {
            e.preventDefault();
            sidebar.classList.toggle('collapsed');
            body.classList.toggle('sidebar-collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
            updateToggleIcon();
            updateTooltips();
        });
    }

    // --- Navigation click handlers using event delegation ---
    document.addEventListener('click', function(e) {
        // Check if clicked element is a nav link in sidebar
        const clickedLink = e.target.closest('.sidebar .nav-link');
        if (!clickedLink) return;
        
        // Check if this is an active nav item
        const navItem = clickedLink.closest('.nav-item');
        const isActive = navItem && navItem.classList.contains('active');
        const isCollapsed = sidebar.classList.contains('collapsed');
        
        // If active tab clicked and sidebar is collapsed, open sidebar instead of navigating
        if (isActive && isCollapsed) {
            // Prevent navigation
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            // Open sidebar
            expandSidebar();
            
            // Visual feedback
            clickedLink.style.transform = 'scale(0.95)';
            setTimeout(() => {
                clickedLink.style.transform = '';
            }, 150);
            
            return false;
        }
    }, true); // Use capture phase to intercept early

    // --- Auto-collapse on small screens ---
    function handleResize() {
        if (window.innerWidth <= 768) {
            collapseSidebar();
        }
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Run once on load
    
    // --- Make updateTooltips globally available ---
    window.updateTooltips = updateTooltips;
});
