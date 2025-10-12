document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

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
        updateTooltips();
    }

    function expandSidebar() {
        if (!sidebar) return;
        sidebar.classList.remove('collapsed');
        body.classList.remove('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', 'false');
        updateTooltips();
    }

    const savedState = localStorage.getItem('sidebarCollapsed');
    if (savedState === 'true') {
        collapseSidebar();
    } else if (savedState === 'false') {
        expandSidebar();
    }

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function (e) {
            e.preventDefault();
            sidebar.classList.toggle('collapsed');
            body.classList.toggle('sidebar-collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
            updateTooltips();
        });
    }

    document.addEventListener('click', function(e) {
        if (!sidebar) return;
        
        const clickedLink = e.target.closest('.sidebar .nav-link');
        if (!clickedLink) return;
        
        const navItem = clickedLink.closest('.nav-item');
        const isActive = navItem && navItem.classList.contains('active');
        const isCollapsed = sidebar.classList.contains('collapsed');
        
        if (isActive && isCollapsed) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            expandSidebar();
            
            clickedLink.style.transform = 'scale(0.95)';
            setTimeout(() => {
                clickedLink.style.transform = '';
            }, 150);
            
            return false;
        }
    }, true); 

    function handleResize() {
        if (!sidebar) return; 
        
        if (window.innerWidth <= 768) {
            sidebar.style.transform = 'translateX(-100%)';
            body.classList.add('sidebar-collapsed');
        } else {
            sidebar.style.transform = '';
            const savedState = localStorage.getItem('sidebarCollapsed');
            if (savedState === 'true') {
                collapseSidebar();
            } else {
                expandSidebar();
            }
        }
    }

    window.addEventListener('resize', handleResize);
    handleResize(); 
    
    function toggleMobileSidebar() {
        if (!sidebar) return;
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle('mobile-open');
        }
    }
    
    document.addEventListener('click', function(e) {
        if (!sidebar) return; 
        if (window.innerWidth <= 768 && e.target.closest('.sidebar-toggle')) {
            toggleMobileSidebar();
        }
    });
    
    window.updateTooltips = updateTooltips;
});
