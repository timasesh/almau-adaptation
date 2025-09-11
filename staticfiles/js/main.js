// Main JavaScript functionality for AlmaU Adaptation app

document.addEventListener('DOMContentLoaded', function() {
    // Dashboard card click handlers
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    dashboardCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add click animation
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Here you can add navigation logic for each card
            const cardTitle = this.querySelector('h3').textContent;
            console.log('Clicked on:', cardTitle);
        });
    });
    
    // Form validation for login
    const loginForm = document.querySelector('.login-form-fields');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = this.querySelector('input[name="login"]');
            const password = this.querySelector('input[name="password"]');
            
            if (!email.value.trim() || !password.value.trim()) {
                e.preventDefault();
                showMessage('Пожалуйста, заполните все поля', 'error');
            }
        });
    }
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Global function for inline onclick handlers
function handleActiveNavClick(event, element) {
    const currentSidebar = document.getElementById('sidebar');
    if (!currentSidebar) return true;
    
    const navItem = element.closest('.nav-item');
    const isActive = navItem && navItem.classList.contains('active');
    const isCollapsed = currentSidebar.classList.contains('collapsed');
    
    if (isActive && isCollapsed) {
        event.preventDefault();
        currentSidebar.classList.remove('collapsed');
        localStorage.setItem('sidebarCollapsed', 'false');
        
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);
        
        return false;
    }
    return true;
}

// Utility function to show messages
function showMessage(text, type = 'info') {
    const messagesContainer = document.querySelector('.messages') || createMessagesContainer();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    messagesContainer.appendChild(messageDiv);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 5000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages';
    document.body.appendChild(container);
    return container;
}
